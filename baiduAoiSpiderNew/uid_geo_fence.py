# Started by Cursor 10351260 20260409115951224
"""
根据百度地图 web 接口 uid 拉取 qt=ext 的 content.geo，解析 bd09mc 多边形环并转为经纬度围栏点列。
转换链路与 aoi_view.convert_raw_bd09mc_str_to_wgs84_points 一致：bd09mc -> WGS84 -> BD09 经纬度（便于在百度地图上叠加）。
"""
# Ended by Cursor 10351260 20260409115951224

from __future__ import annotations

# Started by Cursor 10351260 20260409115951224
import argparse
import json
import sys
import threading
from typing import List, Tuple

import requests
from requests.adapters import HTTPAdapter

from coords import bd09mc_to_wgs84, wgs84_to_bd09ll
# Ended by Cursor 10351260 20260409115951224

# Started by Cursor 10351260 20260409115951224
BAIDU_MAP_EXT_URL = "https://map.baidu.com/"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
# Ended by Cursor 10351260 20260409115951224


# Started by Cursor 10351260 20260409115951224
# Started by Cursor 10351260 20260409202843500
_TLS = threading.local()


def _get_thread_session() -> requests.Session:
    """
    线程内复用 Session 以提升并发抓取速度：
    - 复用 TCP/TLS 连接，减少握手耗时
    - 提供连接池，避免并发下频繁建连
    """
    sess = getattr(_TLS, "session", None)
    if sess is None:
        sess = requests.Session()
        adapter = HTTPAdapter(pool_connections=64, pool_maxsize=64, max_retries=0)
        sess.mount("https://", adapter)
        sess.mount("http://", adapter)
        sess.headers.update(DEFAULT_HEADERS)
        _TLS.session = sess
    return sess
# Ended by Cursor 10351260 20260409202843500


def fetch_ext_json(uid: str, timeout: float = 20.0, session: requests.Session | None = None) -> dict:
    """请求 map.baidu.com qt=ext，返回解析后的 JSON 对象。"""
    params = {
        "newmap": "1",
        "qt": "ext",
        "uid": uid.strip(),
        "ext_ver": "new",
        "ie": "utf-8",
        "l": "11",
    }
    # Started by Cursor 10351260 20260409202843500
    sess = session or _get_thread_session()
    resp = sess.get(
        BAIDU_MAP_EXT_URL,
        params=params,
        timeout=timeout,
    )
    # Ended by Cursor 10351260 20260409202843500
    resp.raise_for_status()
    text = resp.text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    return json.loads(text)
# Ended by Cursor 10351260 20260409115951224


# Started by Cursor 10351260 20260409115951224
def extract_polygon_xy_tail(geo: str) -> str:
    """
    从 content.geo 中取出多边形环的「x,y,x,y,...」串。

    常见格式：
    - 「4|bbox|1-x1,y1,...」：多边形在带前缀 1- 的段中（与线上 ext 返回一致）
    - 「bbox|1-x1,y1,...」：与 aoi_view.py 中 raw_str 一致，多边形在第二段
    """
    if not geo or not geo.strip():
        raise ValueError("geo 为空")

    parts = geo.split("|")
    tail_segment = None
    for p in parts:
        if p.startswith("1-"):
            tail_segment = p[2:]
            break

    if tail_segment is None:
        raise ValueError("geo 中未找到以 1- 开头的多边形段，请检查原始 geo 格式")

    if tail_segment.endswith(";"):
        tail_segment = tail_segment[:-1]

    return tail_segment
# Ended by Cursor 10351260 20260409115951224


# Started by Cursor 10351260 20260409135921491
def bd09mc_xy_to_bd09ll(x: float, y: float) -> Tuple[float, float]:
    """
    单点 bd09mc -> bd09 经纬度，与 aoi_view.convert_raw_bd09mc_str_to_wgs84_points 中循环体一致。
    """
    lng, lat = bd09mc_to_wgs84(x, y)
    lng, lat = wgs84_to_bd09ll(lng, lat)
    return lng, lat
# Ended by Cursor 10351260 20260409135921491


# Started by Cursor 10351260 20260409135921491
def geo_string_to_bd09ll_fence(geo: str) -> List[Tuple[float, float]]:
    """
    传入接口返回的 content.geo 整串，解析多边形环并转为 bd09 经纬度点列 [(lng, lat), ...]。
    """
    tail = extract_polygon_xy_tail(geo)
    tokens = tail.split(",")
    if len(tokens) % 2 != 0:
        raise ValueError("坐标个数为奇数，期望成对的 x,y")
    out: List[Tuple[float, float]] = []
    for i in range(0, len(tokens), 2):
        x = float(tokens[i])
        y = float(tokens[i + 1])
        out.append(bd09mc_xy_to_bd09ll(x, y))
    return out
# Ended by Cursor 10351260 20260409135921491


# Started by Cursor 10351260 20260409135921491
def get_bd09ll_fence_by_uid(
    uid: str, timeout: float = 20.0, session: requests.Session | None = None
) -> Tuple[str, List[Tuple[float, float]]]:
    """
    传参：百度 POI uid。
    返回：(geo 原文, bd09 经纬度围栏 [(lng, lat), ...])，转换步骤与 aoi_view 相同。
    """
    # Started by Cursor 10351260 20260409202843500
    data = fetch_ext_json(uid.strip(), timeout=timeout, session=session)
    # Ended by Cursor 10351260 20260409202843500
    content = data.get("content") or {}
    geo = content.get("geo")
    if not geo:
        raise KeyError("响应中无 content.geo，uid 可能无效或未返回边界")
    points = geo_string_to_bd09ll_fence(geo)
    return geo, points
# Ended by Cursor 10351260 20260409135921491


# Started by Cursor 10351260 20260409115951224
def bd09mc_tail_to_points(
    tail: str, output_crs: str
) -> List[Tuple[float, float]]:
    """
    tail: 「x1,y1,x2,y2,...」bd09mc 米制坐标。
    output_crs: 「bd09」与 aoi_view 一致（经 WGS84 再转回 bd09ll）；「wgs84」为纯 WGS84。
    """
    tokens = tail.split(",")
    if len(tokens) % 2 != 0:
        raise ValueError("坐标个数为奇数，期望成对的 x,y")

    out: List[Tuple[float, float]] = []
    for i in range(0, len(tokens), 2):
        x = float(tokens[i])
        y = float(tokens[i + 1])
        if output_crs == "wgs84":
            lng_wgs, lat_wgs = bd09mc_to_wgs84(x, y)
            out.append((lng_wgs, lat_wgs))
        elif output_crs == "bd09":
            out.append(bd09mc_xy_to_bd09ll(x, y))
        else:
            raise ValueError("output_crs 仅支持 bd09 或 wgs84")

    return out
# Ended by Cursor 10351260 20260409115951224


# Started by Cursor 10351260 20260409115951224
def uid_to_fence(
    uid: str, output_crs: str = "bd09"
) -> Tuple[str, List[Tuple[float, float]]]:
    if output_crs == "bd09":
        return get_bd09ll_fence_by_uid(uid)
    # Started by Cursor 10351260 20260409202843500
    data = fetch_ext_json(uid)
    # Ended by Cursor 10351260 20260409202843500
    content = data.get("content") or {}
    geo = content.get("geo")
    if not geo:
        raise KeyError("响应中无 content.geo，uid 可能无效或未返回边界")

    tail = extract_polygon_xy_tail(geo)
    points = bd09mc_tail_to_points(tail, output_crs=output_crs)
    return geo, points
# Ended by Cursor 10351260 20260409115951224


# Started by Cursor 10351260 20260409141237778
def main(
    uid: str | None = None,
    output: str | None = None,
    uidname:str|None = None,
    crs: str = "bd09",
    geo_only: bool = False,
    timeout: float = 20.0,
) -> str:
    """
    函数式调用入口（你可以直接 main(uid, crs)）。

    - uid: POI uid；传 None/空串时会在控制台提示输入
    - crs: bd09 / wgs84
    - uidname:uid对应的名称
    - output: 若不为 None，则把 JSON 结果写入该文件
    - geo_only: True 时仅返回 geo 原文（字符串）
    - timeout: 请求超时秒数

    返回：打印同款的 JSON 字符串（或 geo_only 时返回 geo 原文）。
    """
    if not uid:
        uid = input("请输入 uid（回车确认）: ").strip()
    if not uid:
        raise ValueError("uid 不能为空")

    if geo_only:
        data = fetch_ext_json(uid, timeout=timeout)
        geo = (data.get("content") or {}).get("geo", "")
        if not geo:
            raise KeyError("未获取到 geo")
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(geo)
        return geo

    geo, points = uid_to_fence(uid, output_crs=crs)
    payload = {
        "uid": uid,
        "uidname":uidname,
        "crs": crs,
        "point_count": len(points),
        "fence": [{"lng": lng, "lat": lat} for lng, lat in points],
        "geo_raw": geo,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
    return text
# Ended by Cursor 10351260 20260409141237778


# Started by Cursor 10351260 20260409141237778
def cli() -> None:
    parser = argparse.ArgumentParser(
        description="输入百度 POI uid，请求 map.baidu.com qt=ext，解析 geo 为经纬度围栏"
    )
    # Started by Cursor 10351260 20260409141051350
    parser.add_argument(
        "uid",
        nargs="?",
        default=None,
        help="POI uid，如 ddfd7c2d8db36cf39ee3219e（不传参则运行时输入）",
    )
    # Ended by Cursor 10351260 20260409141051350
    parser.add_argument(
        "--crs",
        choices=("bd09", "wgs84"),
        default="bd09",
        help="输出坐标系：bd09 与 aoi_view 一致；wgs84 为 GPS 常用",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="将结果写入 JSON 文件（含 geo 原文与点列）",
    )
    parser.add_argument(
        "--geo-only",
        action="store_true",
        help="仅打印原始 geo 字符串",
    )
    args = parser.parse_args()

    try:
        # Started by Cursor 10351260 20260409141237778
        text = main(
            uid=args.uid,
            crs=args.crs,
            output=args.output,
            geo_only=args.geo_only,
        )
        print(text)
        # Ended by Cursor 10351260 20260409141237778
    except requests.RequestException as e:
        print(f"HTTP 请求失败: {e}", file=sys.stderr)
        sys.exit(2)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(3)
# Ended by Cursor 10351260 20260409141237778


if __name__ == "__main__":
    # Started by Cursor 10351260 20260409141237778
    #cli()
    main("6835e3a7c35f5c4ee3110354","test.json","西安市胸科医院")
    # Ended by Cursor 10351260 20260409141237778
# Ended by Cursor 10351260 20260409115951224
