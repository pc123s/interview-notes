# -*- coding: utf-8 -*-
"""
百度地图 AOI（兴趣面）通用爬取脚本

全流程（默认一步到位）：
  1. 行政区划  ：调用百度行政区划接口，获取目标省份/城市下的市、区县列表
                （本地缓存于 admin_cache/，该接口不消耗 place 检索配额）
  2. POI 检索 ：按「建筑类别」调用 place/v3/region 区域检索，逐市/区县翻页抓取
                POI 的 uid / 名称 / 地址 / 坐标等
  3. 围栏解析 ：按 uid 请求 map.baidu.com 的 qt=ext 接口，解析 content.geo 多边形环
                （bd09mc 米制坐标 -> 经纬度；默认输出 BD09，可用 --crs wgs84）
                该接口不消耗 ak 配额，支持多线程并发
  4. 落盘输出 ：每城市 uid CSV、围栏 JSON、失败清单 JSON、百度地图 HTML 可视化，
                以及每个类别的全省汇总文件

运行时会显示整体进度条（0-100%，只增不减），按数量比例推进：
  每个类别爬取前先「预统计」——逐区域请求首屏读取百度上报的 total，汇总出本类别
  可获取的 POI 总数作为固定分母；此后每入库 1 条 POI 计 1 格进度，围栏同理，
  全部汇总完成后到 100%：
    [总进度] ████████░░░░░░░░░░░░░░░░░░░░ 28.4%  检索 320/1140 | 围栏 0/0  学校 | 南京市 检索 2/3

依赖项目内模块（同目录）：
  - uid_geo_fence              围栏解析（map.baidu.com qt=ext）
  - coords                     坐标转换
  - batch_uid_csv_to_html      HTML 可视化生成
  - batch_data_xian_to_outputs 类别索引页生成
外部依赖：requests（pip install requests）

用法示例：
  # 默认 AK 已内置，直接传省份即可；陕西省默认全部 8 个内置类别
  python baidu_aoi_spider.py --province 陕西省

  # 只爬 学校 / 医院
  python baidu_aoi_spider.py --province 陕西省 --categories 学校 医院

  # 任意百度行业分类（一级/二级均可）：美食、酒店、中餐厅…
  python baidu_aoi_spider.py --province 西安市 --categories 美食 酒店

  # 自由关键词，或「检索词:行业分类」组合（冒号后留空 = 不限分类）
  python baidu_aoi_spider.py --province 西安市 --categories 咖啡馆:美食 健身房:

  # 只爬西安市，按区县拆分检索（结果更全，请求数更多）
  python baidu_aoi_spider.py --province 西安市 --categories 餐厅 --region-mode district

  # 只产出 uid 清单，不拉围栏
  python baidu_aoi_spider.py --province 陕西省 --categories 银行 --skip-fence
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple

import requests

from batch_data_xian_to_outputs import generate_index_html
from batch_uid_csv_to_html import DEFAULT_BMAP_AK, generate_multi_fence_html
from uid_geo_fence import uid_to_fence

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
BAIDU_PLACE_REGION_API = "https://api.map.baidu.com/place/v3/region"
BAIDU_ADMIN_API = "https://api.map.baidu.com/api_region_search/v1/"

# place/v3/region 单个 region 单次区域检索最多 20 页（20 条/页 = 400 条），是接口硬上限
MAX_PAGES = 20

# 建筑类别 -> (检索词 query, 百度行业分类 type)
CATEGORY_MAP: Dict[str, Tuple[str, str]] = {
    "学校": ("学校", "教育培训"),
    "医院": ("医院", "医疗"),
    "加油站": ("加油站", "加油站"),
    "公园": ("公园", "旅游景点"),
    "银行": ("银行", "金融"),
    "超市": ("超市", "购物"),
    "餐厅": ("餐厅", "美食"),
    "地铁站": ("地铁站", "交通设施"),
}

DEFAULT_CATEGORIES = list(CATEGORY_MAP.keys())

# 名称后缀过滤：检索词召回范围过宽时，只保留名称以指定后缀结尾的 POI
# （如「高铁站」会混入公交站/汽车站/售票点，「机场」会混入航空公司/售票处/停车场等）
NAME_SUFFIX_RULES: Dict[str, str] = {
    "高铁站": "站",
    "机场": "机场",
}

# 百度地图行业分类（一级）——type 参数常见取值，供 --categories 参考。
# 实测 place API 对任意 type 值均容错（无效值仅被忽略、不报错），因此无需严格白名单，
# 一级/二级分类名、自由关键词均可直接传入。
BAIDU_TYPE_LEVEL1 = [
    "美食", "酒店", "购物", "生活服务", "丽人", "旅游景点", "休闲娱乐",
    "运动健身", "教育培训", "文化传媒", "医疗", "汽车服务", "交通设施",
    "金融", "房地产", "公司企业", "政府机构", "出入口", "自然地物",
    "行政地标", "门址",
]

# 默认 AK（命令行 --ak 不传时使用；如需更换请改这里或用 --ak 覆盖）
DEFAULT_AK = "XRXtH0H65JrHtW9VUq5R2zSRbKSRPe4w"

ADMIN_CACHE_DIR = Path("admin_cache")

CSV_FIELDS = ["uid", "name", "province", "city", "area", "address", "lng", "lat"]


# ---------------------------------------------------------------------------
# 整体进度条（0-100%）
# ---------------------------------------------------------------------------
class ProgressBar:
    """
    终端单行整体进度条（按数量比例推进）：
    - 分母 = 预统计的 POI 总数（每类别爬取前逐区域读首屏 total 汇总，固定不变）
             + 围栏任务数（爬完一个城市才知道该城市 uid 数）
    - 百分比只增不减（围栏分母变大时进度显示不会回退）
    - log() 打印日志前先清除进度行、打印后再重绘，保证与日志互不干扰
    """

    BAR_LEN = 30

    def __init__(self, crawl_total: int) -> None:
        self.crawl_total = max(0, int(crawl_total))
        self.crawl_done = 0
        self.fence_total = 0  # 已发现的围栏任务数（爬完一个城市才知道该城市 uid 数）
        self.fence_done = 0
        self._pct = 0.0
        self._status = ""
        self._active = False

    # ---- 供抓取流程调用 ----
    def set_status(self, status: str) -> None:
        self._status = status

    def add_crawl_done(self, n: int = 1) -> None:
        self.crawl_done += n
        if self.crawl_done > self.crawl_total:
            # 实际获取超出预统计（接口 total 波动/预扫描失败），同步分母避免比例失真
            self.crawl_total = self.crawl_done
        self._render()

    def add_crawl_total(self, n: int) -> None:
        """检索阶段新发现的分母：百度上报的区域 POI 总数（单区域封顶 400 条）。"""
        self.crawl_total += max(0, int(n))

    def add_fence_total(self, n: int) -> None:
        self.fence_total += max(0, int(n))

    def add_fence_done(self, n: int = 1) -> None:
        self.fence_done += n
        self._render()

    def log(self, msg: str) -> None:
        """打印普通日志：先清除进度行，打印日志，再重绘进度行。"""
        if self._active:
            print("\r" + " " * 120 + "\r", end="", flush=True)
            self._active = False
        print(msg)
        if self._pct > 0:
            self._render()

    def finish(self) -> None:
        """收尾：强制显示 100% 并换行。"""
        if self.crawl_total + self.fence_total > 0:
            self._pct = 0.0  # 放开单调限制，强制 100%
            self.crawl_done = self.crawl_total
            self.fence_done = self.fence_total
            self._status = "全部完成"
            self._render()
        if self._active:
            print()
            self._active = False

    # ---- 内部 ----
    def _render(self) -> None:
        denom = self.crawl_total + self.fence_total
        if denom <= 0:
            return
        pct = (self.crawl_done + self.fence_done) * 100.0 / denom
        pct = min(100.0, max(self._pct, pct))  # 单调不减
        self._pct = pct
        filled = int(round(pct / 100.0 * self.BAR_LEN))
        bar = "█" * filled + "░" * (self.BAR_LEN - filled)
        counts = f"检索 {self.crawl_done}/{self.crawl_total} | 围栏 {self.fence_done}/{self.fence_total}"
        line = f"[总进度] {bar} {pct:5.1f}%  {counts}  {self._status}"
        try:
            print("\r" + line + " " * 10, end="", flush=True)
        except UnicodeEncodeError:
            # 终端不支持 Unicode 方块字符时退化为 ASCII
            ascii_bar = "#" * filled + "-" * (self.BAR_LEN - filled)
            print("\r" + f"[总进度] {ascii_bar} {pct:5.1f}%  {counts}  {self._status}" + " " * 10, end="", flush=True)
        self._active = True


_PROGRESS: Optional[ProgressBar] = None


def log_msg(msg: str) -> None:
    """统一日志入口：有进度条时经进度条打印（避免互相覆盖），否则直接 print。"""
    if _PROGRESS is not None:
        _PROGRESS.log(msg)
    else:
        print(msg)


# ---------------------------------------------------------------------------
# 行政区划
# ---------------------------------------------------------------------------
def fetch_admin_divisions(province: str, ak: str, timeout: float = 20.0) -> Dict[str, Any]:
    """
    调用百度行政区划接口（不消耗 place 检索配额），返回：
    {province, cities: [{name, districts: [{name, towns: [{name}]}]}]}
    """
    params = {"keyword": province, "sub_admin": "3", "ak": ak}
    resp = requests.get(BAIDU_ADMIN_API, params=params, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != 0:
        raise RuntimeError(f"行政区划接口失败：status={data.get('status')}, message={data.get('message')}")

    top = data.get("districts") or []
    if not top or not isinstance(top[0], dict):
        raise RuntimeError("行政区划接口未返回有效 districts")

    province_node = top[0]
    cities: List[Dict[str, Any]] = []
    for city in (province_node.get("districts") or []):
        city_item: Dict[str, Any] = {"name": city.get("name"), "districts": []}
        for district in (city.get("districts") or []):
            district_item: Dict[str, Any] = {"name": district.get("name"), "towns": []}
            for town in (district.get("districts") or []):
                district_item["towns"].append({"name": town.get("name")})
            city_item["districts"].append(district_item)
        cities.append(city_item)

    return {"province": province, "cities": cities}


def _is_county_level(name: str, parent_city: str) -> bool:
    """
    city_county 模式用：判断是否按「县」级单独检索（不拆「区」）。
    - 以「区」结尾的跳过（已包含在整市检索中）
    - 县/自治县/林区/特区/旗/自治旗 单独检索
    - 县级市（以「市」结尾且不等于父级城市，如 韩城市 隶属于 渭南市）
    """
    n = (name or "").strip()
    if not n:
        return False
    if n.endswith("区"):
        return False
    if n.endswith(("县", "自治县", "林区", "特区", "旗", "自治旗")):
        return True
    if n.endswith("市") and n != (parent_city or "").strip():
        return True
    return False


def _is_county_or_higher(name: str) -> bool:
    """district 模式用：区县级及以上（区/县/市/旗…），排除 街道/镇/乡 等乡镇级。"""
    n = (name or "").strip()
    if not n:
        return False
    if n.endswith(("街道", "镇", "乡", "苏木")):
        return False
    return True


def iter_region_combos(
    city_item: Dict[str, Any],
    region_mode: str,
    prefix: str = "",
) -> Iterable[Tuple[str, str]]:
    """
    产出 (region, label)，供 place/v3/region 使用：
    - city_county：整市 + 下属县/县级市（不按区拆，请求数少，大城市热门类别可能被 400 条上限截断）
    - district   ：按每个区县级下属拆分（结果更全，请求数更多）
    prefix：直辖市或直接按「市」查询时给 region 加的前缀（如 北京市, / 西安市,）
    """
    city_name = str(city_item.get("name") or "").strip()
    if not city_name:
        return

    if region_mode == "city_county":
        yield f"{prefix}{city_name}", city_name
        for d in city_item.get("districts") or []:
            if not isinstance(d, dict):
                continue
            dn = str(d.get("name") or "").strip()
            if not dn or not _is_county_level(dn, city_name):
                continue
            yield f"{prefix}{city_name},{dn}", f"{city_name}-{dn}"
    else:  # district
        subs = [
            str(d.get("name") or "").strip()
            for d in (city_item.get("districts") or [])
            if isinstance(d, dict) and _is_county_or_higher(str(d.get("name") or ""))
        ]
        if not subs:
            # 直辖市/单市查询时下属已是街道级，直接整区检索
            yield f"{prefix}{city_name}", city_name
            return
        for dn in subs:
            yield f"{prefix}{city_name},{dn}", f"{city_name}-{dn}"


# ---------------------------------------------------------------------------
# POI 检索（place/v3/region）
# ---------------------------------------------------------------------------
def _request_json(url: str, params: Dict[str, Any], timeout_s: float, tries: int = 3) -> Dict[str, Any]:
    last: Optional[Exception] = None
    for attempt in range(1, tries + 1):
        try:
            resp = requests.get(url, params=params, timeout=timeout_s)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            last = e
            if attempt < tries:
                time.sleep(1.0 * attempt)
    raise last if last is not None else RuntimeError("未知请求错误")


def search_pois_in_region(
    ak: str,
    region: str,
    query: str,
    place_type: Optional[str],
    page_size: int = 20,
    timeout_s: float = 15.0,
    sleep_s: float = 0.2,
    on_total: Optional[Callable[[int], None]] = None,
    max_pages: int = MAX_PAGES,
) -> List[Dict[str, str]]:
    """
    place/v3/region 区域检索，翻页拉全（受单区域 400 条接口上限约束）。
    on_total：首屏获知百度上报 total 时回调一次（传封顶后实际可获取的条数）。
    max_pages：最多翻页数（预扫描时传 1，只取首屏 total）。
    """
    page_size = min(int(page_size), 20)
    items: List[Dict[str, str]] = []
    seen: Set[str] = set()
    total: Optional[int] = None

    for page_num in range(max_pages):
        params = {
            "query": query,
            "region": region,
            "ak": ak,
            "output": "json",
            "page_num": page_num,
            "page_size": page_size,
            "scope": 1,
            "region_limit": "true",
        }
        if place_type:
            params["type"] = place_type
        data = _request_json(BAIDU_PLACE_REGION_API, params, timeout_s)

        status = data.get("status")
        if status != 0:
            message = data.get("message", "")
            if status in (302, 401):
                message += "（可能是 AK 配额用尽或无权限，请检查百度控制台）"
            raise RuntimeError(f"百度API请求失败: region={region}, status={status}, message={message}")

        if total is None:
            total = int(data.get("total", 0) or 0)
            if on_total is not None:
                on_total(min(total, MAX_PAGES * page_size))

        results = data.get("results") or []
        if not results:
            break

        for it in results:
            if not isinstance(it, dict):
                continue
            uid = str(it.get("uid") or "").strip()
            if not uid or uid in seen:
                continue
            seen.add(uid)
            loc = it.get("location") or {}
            items.append(
                {
                    "uid": uid,
                    "name": str(it.get("name") or "").strip(),
                    "province": str(it.get("province") or "").strip(),
                    "city": str(it.get("city") or "").strip(),
                    "area": str(it.get("area") or "").strip(),
                    "address": str(it.get("address") or "").strip(),
                    "lng": str(loc.get("lng") or ""),
                    "lat": str(loc.get("lat") or ""),
                }
            )

        if len(results) < page_size:
            break
        if total is not None and (page_num + 1) * page_size >= total:
            break
        time.sleep(sleep_s)

    if len(items) >= MAX_PAGES * page_size:
        log_msg(
            f"[WARN] region={region} 已取满 400 条（接口单区域上限），实际数量可能更多；"
            f"如需更全请使用 --region-mode district 或缩小检索范围"
        )
    return items


def pre_count_region_total(
    ak: str,
    region: str,
    query: str,
    place_type: Optional[str],
    timeout_s: float,
    page_size: int,
) -> int:
    """
    预统计单个区域可获取的 POI 数（只请求首屏读 total，封顶 400 条）。
    请求失败时返回 0（不阻塞主流程，实际爬取时该区域仍会重试）。
    """
    totals: List[int] = []
    try:
        search_pois_in_region(
            ak,
            region,
            query,
            place_type,
            page_size=page_size,
            timeout_s=timeout_s,
            sleep_s=0.0,
            on_total=totals.append,
            max_pages=1,
        )
    except Exception:
        return 0
    return totals[0] if totals else 0


# ---------------------------------------------------------------------------
# 围栏解析（map.baidu.com qt=ext，不消耗 ak 配额）
# ---------------------------------------------------------------------------
def fetch_fences_for_rows(
    rows: List[Dict[str, str]],
    crs: str = "bd09",
    timeout: float = 20.0,
    max_workers: int = 8,
    attempts: int = 2,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    按 uid 批量拉取 AOI 围栏，返回 (success_items, error_items)，顺序与输入一致。
    success_items: [{uid, name, point_count, fence: [{lng, lat}, ...]}]
    """
    total = len(rows)
    if total == 0:
        return [], []

    success_buf: Dict[int, Dict[str, Any]] = {}
    error_buf: Dict[int, Dict[str, Any]] = {}

    def _worker(idx: int, r: Dict[str, str]) -> Tuple[int, bool, Dict[str, Any]]:
        uid, name = r["uid"], r["name"]
        last: Optional[Exception] = None
        for _ in range(max(1, attempts)):
            try:
                _geo_raw, points = uid_to_fence(uid, output_crs=crs)
                fence = [{"lng": round(lng, 6), "lat": round(lat, 6)} for lng, lat in points]
                return idx, True, {
                    "uid": uid,
                    "name": name,
                    "point_count": len(fence),
                    "fence": fence,
                }
            except Exception as e:
                last = e
                time.sleep(0.3)
        return idx, False, {"uid": uid, "name": name, "error": str(last)}

    bar = _PROGRESS
    with ThreadPoolExecutor(max_workers=max(1, int(max_workers))) as executor:
        futures = [executor.submit(_worker, idx, r) for idx, r in enumerate(rows, start=1)]
        for done, future in enumerate(as_completed(futures), start=1):
            idx, ok, item = future.result()
            (success_buf if ok else error_buf)[idx] = item
            # 整体进度：按围栏数量逐个推进
            if bar is not None:
                bar.add_fence_done()
            if done % 100 == 0 or done == total:
                log_msg(f"[INFO]   围栏进度 {done}/{total}（成功 {len(success_buf)} / 失败 {len(error_buf)}）")

    success = [success_buf[i] for i in sorted(success_buf)]
    errors = [error_buf[i] for i in sorted(error_buf)]
    return success, errors


# ---------------------------------------------------------------------------
# CSV / HTML 工具
# ---------------------------------------------------------------------------
def save_uid_csv(rows: List[Dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_uid_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(f)
        ]


def _empty_html(title: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"/><title>{title}</title></head>
<body style="font-family:Arial;margin:24px;">
  <h3>{title}</h3>
  <p>无可展示围栏（全部失败或无数据）。</p>
</body>
</html>
"""


def resolve_categories(names: Iterable[str]) -> List[Dict[str, str]]:
    """
    解析 --categories 为 [{name, label, query, type}]：
    - 内置别名（学校/医院/…）：沿用 CATEGORY_MAP 的 query/type 组合
    - 「query:type」：冒号前为检索词、冒号后为百度行业分类（type 留空 = 不限分类）
    - 其他任意值：检索词与行业分类同值（百度 place API 对 type 容错，行业分类名均可直接传）
    name 为输出目录安全名（Windows 非法字符替换为 _），label 为日志/HTML 显示名。
    """
    out: List[Dict[str, str]] = []
    seen: Set[Tuple[str, str]] = set()
    for n in names:
        n = (n or "").strip()
        if not n:
            continue
        if ":" in n:
            query, _, place_type = n.partition(":")
            query, place_type = query.strip(), place_type.strip()
        elif n in CATEGORY_MAP:
            query, place_type = CATEGORY_MAP[n]
        else:
            query, place_type = n, n
        if not query:
            raise ValueError(f"类别「{n}」检索词为空")
        key = (query, place_type)
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "name": n.translate(str.maketrans({"\\": "_", "/": "_", ":": "_"})),
                "label": n,
                "query": query,
                "type": place_type,
            }
        )
    if out:
        return out
    return [
        {"name": n, "label": n, "query": CATEGORY_MAP[n][0], "type": CATEGORY_MAP[n][1]}
        for n in DEFAULT_CATEGORIES
    ]


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="百度地图 AOI 通用爬取：行政区划 -> place 检索 uid -> qt=ext 围栏解析 -> CSV/JSON/HTML 落盘"
    )
    parser.add_argument("--ak", default=DEFAULT_AK, help="百度地图服务端 AK（默认已内置，可不传）")
    parser.add_argument("--province", required=True, help="省份或城市名，如 陕西省 / 西安市 / 北京市（直辖市、单市均支持）")
    parser.add_argument(
        "--categories",
        nargs="+",
        default=DEFAULT_CATEGORIES,
        metavar="CATEGORY",
        help=(
            "类别（可多个，默认全部内置别名）。支持：内置别名（"
            + "、".join(CATEGORY_MAP)
            + "）；百度行业分类名（一级：" + "、".join(BAIDU_TYPE_LEVEL1) + "，二级亦可）；"
            "自由关键词；「检索词:行业分类」组合（如 咖啡馆:美食，冒号后留空表示不限分类）"
        ),
    )
    parser.add_argument(
        "--region-mode",
        choices=("city_county", "district"),
        default="city_county",
        help="检索范围：city_county=整市+县/县级市（请求少，热门类别可能被 400 条上限截断）；"
        "district=按每个区/县拆分（更全，请求多）。默认 city_county",
    )
    parser.add_argument("--out-root", default="outputs_aoi", help="输出根目录，默认 outputs_aoi")
    parser.add_argument(
        "--crs",
        choices=("bd09", "wgs84"),
        default="bd09",
        help="围栏输出坐标系：bd09=百度坐标（适合百度地图叠加）；wgs84=GPS 坐标（适合 GIS 叠加）。默认 bd09",
    )
    parser.add_argument("--page-size", type=int, default=20, help="place/v3/region 每页条数（最大 20）")
    parser.add_argument("--timeout", type=float, default=15.0, help="place/行政区划请求超时（秒）")
    parser.add_argument("--sleep", type=float, default=0.2, help="place 翻页请求间隔（秒）")
    parser.add_argument("--fence-timeout", type=float, default=20.0, help="qt=ext 单 uid 请求超时（秒）")
    parser.add_argument("--max-workers", type=int, default=8, help="围栏抓取并发线程数")
    parser.add_argument("--skip-crawl", action="store_true", help="跳过 POI 检索，仅用已有 CSV 做围栏/汇总")
    parser.add_argument("--skip-fence", action="store_true", help="跳过围栏抓取，只产出 uid CSV")
    parser.add_argument("--no-html", action="store_true", help="不生成 HTML 可视化页面")
    parser.add_argument("--html-ak", default=None, help="HTML 展示用的浏览器端 JS API ak（默认用内置浏览器端 AK；JSON/CSV 不受影响）")
    parser.add_argument("--regen-html", action="store_true", help="不爬取、不拉围栏，仅根据已有 aoi_json 重新生成 HTML（更换 html-ak 后可用）")
    parser.add_argument("--overwrite", action="store_true", help="忽略已有 CSV/JSON，强制重新抓取")
    parser.add_argument("--refresh-admin", action="store_true", help="强制重新获取行政区划（默认使用 admin_cache 缓存）")
    args = parser.parse_args()

    try:
        categories = resolve_categories(args.categories)
    except ValueError as e:
        parser.error(str(e))
    # HTML 地图展示必须用「浏览器端」JS API 的 AK（服务端 AK 没有 JavaScript API
    # 服务，浏览器里会报「APP服务被禁用」），默认取项目内置的浏览器端 AK
    html_ak = (args.html_ak or "").strip() or DEFAULT_BMAP_AK
    if args.regen_html:
        args.skip_crawl = True  # 只重建 HTML：跳过 POI 检索；围栏 JSON 已存在时也不会重拉

    # 1) 行政区划（缓存，不占 place 检索配额）
    ADMIN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    admin_path = ADMIN_CACHE_DIR / f"{args.province}_下三级行政区_整理版.json"
    if args.refresh_admin or not admin_path.exists():
        log_msg(f"[INFO] 获取行政区划：{args.province}")
        admin = fetch_admin_divisions(args.province, args.ak, timeout=args.timeout)
        admin_path.write_text(json.dumps(admin, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        admin = json.loads(admin_path.read_text(encoding="utf-8"))
        log_msg(f"[INFO] 使用缓存行政区划：{admin_path}")
    cities = [c for c in (admin.get("cities") or []) if isinstance(c, dict) and str(c.get("name") or "").strip()]
    if not cities:
        raise ValueError(f"未解析到 {args.province} 的下级行政区，请检查省份/城市名")

    # 直辖市或直接按「市」查询时，顶层已是区县，region 需要带上级前缀（如 北京市,东城区）
    first_city = str(cities[0].get("name") or "").strip()
    prefix = f"{args.province}," if first_city.endswith("区") else ""

    log_msg(
        f"[INFO] 目标：{args.province}，城市/区县数：{len(cities)}，"
        f"类别：{'、'.join(c['label'] for c in categories)}，region-mode={args.region_mode}，crs={args.crs}"
    )

    # 2) 整体进度：分母按「数量」动态累计——检索首屏返回百度上报 total 后计入，
    #    围栏任务数爬完一个城市才知道；百分比只增不减
    global _PROGRESS
    _PROGRESS = ProgressBar(0)
    bar = _PROGRESS

    run_summary: List[Dict[str, Any]] = []

    for cat_info in categories:
        cat, label = cat_info["name"], cat_info["label"]
        query, place_type = cat_info["query"], cat_info["type"]
        name_suffix = NAME_SUFFIX_RULES.get(label) or NAME_SUFFIX_RULES.get(query)
        cat_dir = Path(args.out_root) / args.province / cat
        csv_dir = cat_dir / "uid_csv"
        json_dir = cat_dir / "aoi_json"
        html_dir = cat_dir / "aoi_html"
        for d in (csv_dir, json_dir, html_dir):
            d.mkdir(parents=True, exist_ok=True)

        suffix_note = f"，名称须以「{name_suffix}」结尾" if name_suffix else ""
        log_msg(f"\n===== 类别：{label}（query={query}, type={place_type or '不限'}{suffix_note}）=====")

        # 断点续跑：预扫描已有 CSV，跨城市按 uid 去重
        global_seen: Set[str] = set()
        if not args.overwrite:
            for csv_path in csv_dir.glob("*_uid.csv"):
                for row in load_uid_csv(csv_path):
                    uid = (row.get("uid") or "").strip()
                    if uid:
                        global_seen.add(uid)

        # 预统计：先汇总本类别所有待检索区域的可获取 POI 总数，作为检索进度的固定分母
        # （每个待检索区域 1 次首屏请求读 total，不拉数据；已有 CSV 的城市不重复统计）
        if not args.skip_crawl:
            pre_cat_total = 0
            pre_scan_regions = 0
            bar.set_status(f"{label} | 预统计总数…")
            for city_item in cities:
                city_name = str(city_item.get("name") or "").strip()
                city_csv = csv_dir / f"{city_name}_{cat}_uid.csv"
                if city_csv.exists() and not args.overwrite:
                    continue
                for region, _ in iter_region_combos(city_item, args.region_mode, prefix):
                    n = pre_count_region_total(
                        args.ak, region, query, place_type, args.timeout, args.page_size
                    )
                    if n:
                        bar.add_crawl_total(n)
                        pre_cat_total += n
                        pre_scan_regions += 1
                    time.sleep(args.sleep)
            log_msg(
                f"[INFO] 预统计完成：{pre_scan_regions} 个区域，本类别可获取 {pre_cat_total} 条"
                f"（累计检索分母 {bar.crawl_total}）"
            )

        html_entries: List[Dict[str, Any]] = []

        for ci, city_item in enumerate(cities, start=1):
            combos = list(iter_region_combos(city_item, args.region_mode, prefix))
            city_name = str(city_item.get("name") or "").strip()
            log_msg(f"[INFO] ({ci}/{len(cities)}) 城市/区县：{city_name}，检索区域数：{len(combos)}")

            # ---- POI 检索 ----
            city_csv = csv_dir / f"{city_name}_{cat}_uid.csv"
            if args.skip_crawl or (city_csv.exists() and not args.overwrite):
                city_rows = load_uid_csv(city_csv) if city_csv.exists() else []
                reason = "--skip-crawl" if args.skip_crawl else "已有结果"
                log_msg(f"[INFO]   跳过检索（{reason}）：{city_csv.name}，{len(city_rows)} 条")
            else:
                city_rows = []
                failed = 0
                for rj, (region, region_label) in enumerate(combos, start=1):
                    log_msg(f"[INFO]   ({rj}/{len(combos)}) 检索 region={region}")
                    bar.set_status(f"{label} | {city_name} 检索 {rj}/{len(combos)}")
                    try:
                        items = search_pois_in_region(
                            args.ak,
                            region,
                            query,
                            place_type,
                            page_size=args.page_size,
                            timeout_s=args.timeout,
                            sleep_s=args.sleep,
                        )
                    except Exception as e:
                        failed += 1
                        log_msg(f"[WARN]   region={region} 失败：{e}")
                        continue
                    added = 0
                    filtered = 0
                    for it in items:
                        # 每获取 1 条即推进 1 格（含跨区域重复项，与预统计分母口径一致）
                        bar.add_crawl_done()
                        if name_suffix and not (it.get("name") or "").strip().endswith(name_suffix):
                            filtered += 1
                            continue
                        if it["uid"] in global_seen:
                            continue
                        global_seen.add(it["uid"])
                        city_rows.append(it)
                        added += 1
                    filter_msg = f"，名称过滤 {filtered}" if name_suffix else ""
                    log_msg(f"[INFO]   本次返回 {len(items)}{filter_msg}，新增 {added}，城市累计 {len(city_rows)}")
                if failed and failed == len(combos):
                    log_msg(f"[WARN]   城市 {city_name} 全部检索失败，请检查 AK 配额/权限")
                save_uid_csv(city_rows, city_csv)
                log_msg(f"[DONE] 已写入 {city_csv.name}（{len(city_rows)} 条）")

            # ---- 围栏解析 ----
            json_path = json_dir / f"{city_name}_{cat}.json"
            errors_path = json_dir / f"{city_name}_{cat}.errors.json"
            fences: List[Dict[str, Any]] = []
            errors: List[Dict[str, Any]] = []

            if args.skip_fence:
                log_msg("[INFO]   跳过围栏（--skip-fence）")
            elif json_path.exists() and not args.overwrite:
                try:
                    fences = json.loads(json_path.read_text(encoding="utf-8"))
                except Exception:
                    fences = []
                try:
                    errors = json.loads(errors_path.read_text(encoding="utf-8"))
                except Exception:
                    errors = []
                log_msg(f"[INFO]   围栏 JSON 已存在，跳过：成功 {len(fences)} / 失败 {len(errors)}")
            else:
                log_msg(f"[INFO]   开始抓取围栏，共 {len(city_rows)} 个 uid（crs={args.crs}）")
                bar.add_fence_total(len(city_rows))
                bar.set_status(f"{label} | {city_name} 围栏 0/{len(city_rows)}")
                fences, errors = fetch_fences_for_rows(
                    city_rows,
                    crs=args.crs,
                    timeout=args.fence_timeout,
                    max_workers=args.max_workers,
                )
                json_path.write_text(json.dumps(fences, ensure_ascii=False, indent=2), encoding="utf-8")
                errors_path.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
                log_msg(f"[INFO]   围栏完成：成功 {len(fences)} / 失败 {len(errors)}")

            if not args.skip_fence:
                html_entries.append(
                    {
                        "title": f"{city_name}_{cat}",
                        "html": f"{city_name}_{cat}.html",
                        "success": len(fences),
                        "errors": len(errors),
                    }
                )
                html_path = html_dir / f"{city_name}_{cat}.html"
                if not args.no_html and (args.regen_html or not html_path.exists() or args.overwrite):
                    if fences:
                        generate_multi_fence_html(
                            fences, out_html=str(html_path), ak=html_ak, title=f"{city_name} {label} 围栏"
                        )
                    else:
                        html_path.write_text(_empty_html(f"{city_name} {label}"), encoding="utf-8")

        # ---- 类别汇总 ----
        all_rows: List[Dict[str, str]] = []
        seen_all: Set[str] = set()
        for csv_path in sorted(csv_dir.glob("*_uid.csv")):
            for row in load_uid_csv(csv_path):
                uid = (row.get("uid") or "").strip()
                if not uid or uid in seen_all:
                    continue
                seen_all.add(uid)
                all_rows.append(row)

        all_fences: List[Dict[str, Any]] = []
        for jp in sorted(json_dir.glob("*.json")):
            if jp.name.endswith(".errors.json"):
                continue
            city_of_file = jp.stem.rsplit("_", 1)[0]
            try:
                for it in json.loads(jp.read_text(encoding="utf-8")):
                    it = dict(it)
                    it["city"] = city_of_file
                    all_fences.append(it)
            except Exception:
                continue

        all_errors: List[Dict[str, Any]] = []
        for ep in sorted(json_dir.glob("*.errors.json")):
            try:
                all_errors.extend(json.loads(ep.read_text(encoding="utf-8")))
            except Exception:
                continue

        save_uid_csv(all_rows, cat_dir / f"{cat}_all.csv")
        (cat_dir / f"{cat}_all.json").write_text(
            json.dumps(all_fences, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (cat_dir / f"{cat}_all.errors.json").write_text(
            json.dumps(all_errors, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        summary = {
            "category": label,
            "province": args.province,
            "region_mode": args.region_mode,
            "crs": args.crs,
            "poi_total": len(all_rows),
            "fence_success": len(all_fences),
            "fence_failed": len(all_errors),
        }
        (cat_dir / "_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if html_entries and not args.no_html:
            generate_index_html(html_entries, html_dir / "index.html", title=f"{args.province} {label} AOI 围栏索引")

        run_summary.append(summary)
        log_msg(
            f"[DONE] 类别 {label}：POI={summary['poi_total']}，"
            f"围栏成功={summary['fence_success']}，失败={summary['fence_failed']}"
        )

    bar.finish()
    _PROGRESS = None

    log_msg("\n===== 本次运行汇总 =====")
    for s in run_summary:
        log_msg(f"  {s['category']}: POI {s['poi_total']} / 围栏成功 {s['fence_success']} / 失败 {s['fence_failed']}")
    log_msg(f"输出目录：{(Path(args.out_root) / args.province).resolve()}")
    log_msg("[INFO] 全部完成。")


if __name__ == "__main__":
    main()
