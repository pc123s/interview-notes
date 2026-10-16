# Started by Cursor 10351260 20260409142357842
"""
读取「西安市长安区_医院_uid.csv」，批量按 uid 拉取围栏并生成前端 HTML 展示（多围栏可切换）。

CSV 期望字段（任意一种即可）：
- uid,name
- uid,uidname
- 或至少包含 uid 列
"""
# Ended by Cursor 10351260 20260409142357842

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
# Started by Cursor 10351260 20260409142357842
import argparse
import csv
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from uid_geo_fence import get_bd09ll_fence_by_uid
import os
# Ended by Cursor 10351260 20260409142357842


# Started by Cursor 10351260 20260409142357842
DEFAULT_BMAP_AK = "ArKblRbibgjnUw4BqetR6CZEw1Jmur9O"
DEFAULT_CSV = "西安市长安区_医院_uid.csv"
# Ended by Cursor 10351260 20260409142357842


# Started by Cursor 10351260 20260409142357842
def _pick_first(row: Dict[str, Any], keys: List[str]) -> Optional[str]:
    for k in keys:
        v = row.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return None
# Ended by Cursor 10351260 20260409142357842


# Started by Cursor 10351260 20260409142357842
def load_uid_rows(csv_path: str) -> List[Dict[str, str]]:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV 不存在：{csv_path}")

    # 常见：utf-8-sig（Excel 导出带 BOM）
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV 表头为空")

        out: List[Dict[str, str]] = []
        for row in reader:
            uid = _pick_first(row, ["uid", "UID", "Uid"])
            if not uid:
                continue
            name = _pick_first(row, ["name", "uidname", "名称", "医院", "医院名称"]) or uid
            out.append({"uid": uid, "name": name})
        return out
# Ended by Cursor 10351260 20260409142357842

def fetch_fences_from_rows_fast(
    rows: List[Dict[str, str]],
    timeout: float = 20.0,
    sleep_s: float = 0.0,
    limit: int = 0,
    max_workers: int = 8,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    返回：(success_items, error_items)

    success_items: [{uid,name,point_count,fence:[{lng,lat}...]}...]

    说明：
    - 改为线程池并发抓取
    - 返回结果默认按输入顺序还原
    - sleep_s 表示“提交任务前的节流间隔”，并发模式下建议设为 0
    """
    success: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    total = len(rows) if limit <= 0 else min(len(rows), limit)
    if total <= 0:
        return success, errors

    max_workers = max(1, int(max_workers))
    lock = threading.Lock()

    success_buffer: Dict[int, Dict[str, Any]] = {}
    error_buffer: Dict[int, Dict[str, Any]] = {}

    def _worker(idx: int, r: Dict[str, str]) -> Tuple[int, bool, Dict[str, Any]]:
        uid = r["uid"]
        name = r["name"]
        try:
            _geo_raw, points = get_bd09ll_fence_by_uid(uid, timeout=timeout)
            fence = [{"lng": lng, "lat": lat} for (lng, lat) in points]
            item = {
                "uid": uid,
                "name": name,
                "point_count": len(fence),
                "fence": fence,
            }
            return idx, True, item
        except Exception as e:
            return idx, False, {"uid": uid, "name": name, "error": str(e)}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for idx, r in enumerate(rows[:total], start=1):
            if sleep_s > 0 and idx > 1:
                time.sleep(sleep_s)
            futures.append(executor.submit(_worker, idx, r))

        for done_count, future in enumerate(as_completed(futures), start=1):
            idx, ok, item = future.result()

            with lock:
                if ok:
                    success_buffer[idx] = item
                else:
                    error_buffer[idx] = item

                if done_count % 50 == 0 or done_count == total:
                    print(f"处理到第{done_count}/{total}个了")

    # 按输入顺序还原
    for idx in range(1, total + 1):
        if idx in success_buffer:
            success.append(success_buffer[idx])
        elif idx in error_buffer:
            errors.append(error_buffer[idx])

    return success, errors

# Started by Cursor 10351260 20260409142357842
def fetch_fences_from_rows(
    rows: List[Dict[str, str]],
    timeout: float = 20.0,
    sleep_s: float = 0.2,
    limit: int = 0,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    返回：(success_items, error_items)

    success_items: [{uid,name,point_count,fence:[{lng,lat}...]}...]
    """
    success: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    total = len(rows) if limit <= 0 else min(len(rows), limit)
    for i, r in enumerate(rows[:total], start=1):
        uid = r["uid"]
        name = r["name"]
        if i%50==0:
            print(f"处理到第{i}个了")
        try:
            _geo_raw, points = get_bd09ll_fence_by_uid(uid, timeout=timeout)
            fence = [{"lng": lng, "lat": lat} for (lng, lat) in points]
            success.append(
                {
                    "uid": uid,
                    "name": name,
                    "point_count": len(fence),
                    "fence": fence,
                }
            )
        except Exception as e:
            errors.append({"uid": uid, "name": name, "error": str(e)})

        if sleep_s > 0 and i < total:
            time.sleep(sleep_s)

    return success, errors
# Ended by Cursor 10351260 20260409142357842


# Started by Cursor 10351260 20260409142357842
def generate_multi_fence_html(
    items: List[Dict[str, Any]],
    out_html: str,
    ak: str = DEFAULT_BMAP_AK,
    title: str = "长安区医院围栏",
) -> str:
    if not items:
        raise ValueError("没有可展示的围栏数据（items 为空）")

    js_items = json.dumps(items, ensure_ascii=False)

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <style>
    html, body {{ width:100%; height:100%; margin:0; padding:0; }}
    #map {{ width:100%; height:100%; }}
    .panel {{
      position:absolute; left:12px; top:12px; background:rgba(255,255,255,0.92);
      padding:10px 12px; border-radius:10px; font-size:13px; max-width:420px; z-index:999;
      box-shadow: 0 6px 20px rgba(0,0,0,.12);
    }}
    .list {{
      margin-top:8px;
      max-height: 60vh;
      overflow:auto;
      padding-right: 6px;
    }}
    .row {{
      display:flex;
      align-items:center;
      gap:8px;
      padding:6px 0;
      border-bottom: 1px dashed rgba(0,0,0,.08);
    }}
    .name {{
      flex: 1;
      overflow:hidden;
      text-overflow:ellipsis;
      white-space:nowrap;
    }}
    button {{
      border: 1px solid rgba(0,0,0,.15);
      background: #fff;
      border-radius: 8px;
      padding: 6px 10px;
      cursor:pointer;
    }}
    button:hover {{ background: #f5f7ff; }}
  </style>
</head>
<body>
  <div class="panel">
    <div style="font-weight:700;">{title}</div>
    <div style="margin-top:6px;color:#555;">共 {len(items)} 条（勾选显示围栏）</div>
    <div style="margin-top:8px; display:flex; gap:8px;">
      <button id="btnAll">全选</button>
      <button id="btnNone">全不选</button>
      <button id="btnFit">适配视野</button>
    </div>
    <div class="list" id="list"></div>
  </div>

  <div id="map"></div>
  <script type="text/javascript" src="https://api.map.baidu.com/api?v=3.0&ak={ak}"></script>
  <script>
    const items = {js_items};
    const map = new BMap.Map("map");
    map.centerAndZoom(new BMap.Point(116.404, 39.915), 12);
    map.enableScrollWheelZoom(true);

    const overlays = new Map(); // uid -> polygon

    function buildPolygon(item) {{
      const pts = item.fence.map(p => new BMap.Point(p.lng, p.lat));
      const poly = new BMap.Polygon(pts, {{
        strokeColor: "#1e90ff",
        strokeWeight: 2,
        strokeOpacity: 0.9,
        fillColor: "#1e90ff",
        fillOpacity: 0.25
      }});
      return poly;
    }}

    function ensureOverlay(item) {{
      if (overlays.has(item.uid)) return overlays.get(item.uid);
      const poly = buildPolygon(item);
      overlays.set(item.uid, poly);
      return poly;
    }}

    function setVisible(item, visible) {{
      const poly = ensureOverlay(item);
      if (visible) {{
        map.addOverlay(poly);
      }} else {{
        map.removeOverlay(poly);
      }}
    }}

    function fitViewport() {{
      const polys = [];
      overlays.forEach((poly) => {{
        // 仅对当前在地图上的 overlay 生效
        // 百度 Map API 无直接判断是否已 addOverlay，这里用 getMap() 规避
        if (poly.getMap && poly.getMap()) polys.push(poly);
      }});
      if (polys.length === 0) return;
      const bounds = polys[0].getBounds();
      for (let i = 1; i < polys.length; i++) {{
        bounds.extend(polys[i].getBounds().getSouthWest());
        bounds.extend(polys[i].getBounds().getNorthEast());
      }}
      map.setViewport(bounds);
    }}

    const listEl = document.getElementById("list");
    items.forEach((item, idx) => {{
      const row = document.createElement("div");
      row.className = "row";

      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = false;
      cb.addEventListener("change", () => {{
        setVisible(item, cb.checked);
      }});

      const name = document.createElement("div");
      name.className = "name";
      name.title = item.name + " (" + item.uid + ")";
      name.textContent = (idx+1) + ". " + item.name + "  [" + item.point_count + "点]";
      name.addEventListener("click", () => {{
        const poly = ensureOverlay(item);
        map.addOverlay(poly);
        cb.checked = true;
        map.setViewport(poly.getBounds());
      }});

      row.appendChild(cb);
      row.appendChild(name);
      listEl.appendChild(row);
    }});

    document.getElementById("btnAll").addEventListener("click", () => {{
      listEl.querySelectorAll("input[type=checkbox]").forEach((cb, i) => {{
        if (!cb.checked) {{
          cb.checked = true;
          setVisible(items[i], true);
        }}
      }});
      fitViewport();
    }});

    document.getElementById("btnNone").addEventListener("click", () => {{
      listEl.querySelectorAll("input[type=checkbox]").forEach((cb, i) => {{
        if (cb.checked) {{
          cb.checked = false;
          setVisible(items[i], false);
        }}
      }});
    }});

    document.getElementById("btnFit").addEventListener("click", () => {{
      fitViewport();
    }});
  </script>
</body>
</html>
"""

    Path(out_html).write_text(html, encoding="utf-8")
    return out_html
# Ended by Cursor 10351260 20260409142357842


# Started by Cursor 10351260 20260409142357842
def main(
    csv_path: str = DEFAULT_CSV,
    out_html: str = "changan_hospitals_fences.html",
    ak: str = DEFAULT_BMAP_AK,
    title: str = "长安区医院围栏",
    timeout: float = 20.0,
    sleep_s: float = 0.2,
    limit: int = 0,
    out_json: str | None = "changan_hospitals_fences.json",
    out_errors_json: str | None = "changan_hospitals_fences.errors.json",
) -> str:
    rows = load_uid_rows(csv_path)
    items, errors = fetch_fences_from_rows(rows, timeout=timeout, sleep_s=sleep_s, limit=limit)

    if out_json:
        Path(out_json).write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    if out_errors_json:
        Path(out_errors_json).write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")

    return generate_multi_fence_html(items, out_html=out_html, ak=ak, title=title)
# Ended by Cursor 10351260 20260409142357842


# Started by Cursor 10351260 20260409142357842
def cli() -> None:
    parser = argparse.ArgumentParser(description="从 uid CSV 批量抓围栏，生成百度地图 HTML 展示")
    parser.add_argument("csv", nargs="?", default=DEFAULT_CSV, help="CSV 路径（默认：西安市长安区_医院_uid.csv）")
    parser.add_argument("-o", "--out", default="changan_hospitals_fences.html", help="输出 HTML 文件名")
    parser.add_argument("--ak", default=DEFAULT_BMAP_AK, help="百度地图 JS API ak")
    parser.add_argument("--title", default="长安区医院围栏", help="页面标题")
    parser.add_argument("--timeout", type=float, default=20.0, help="单个 uid 请求超时（秒）")
    parser.add_argument("--sleep", type=float, default=0.2, help="每次请求间隔（秒）")
    parser.add_argument("--limit", type=int, default=0, help="限制处理前 N 条（0=不限制）")
    parser.add_argument("--out-json", default="changan_hospitals_fences.json", help="输出围栏聚合 JSON（可为空）")
    parser.add_argument("--out-errors-json", default="changan_hospitals_fences.errors.json", help="输出失败列表 JSON（可为空）")
    args = parser.parse_args()

    out = main(
        csv_path=args.csv,
        out_html=args.out,
        ak=args.ak,
        title=args.title,
        timeout=args.timeout,
        sleep_s=args.sleep,
        limit=args.limit,
        out_json=args.out_json if args.out_json else None,
        out_errors_json=args.out_errors_json if args.out_errors_json else None,
    )
    print(f"已生成：{out}")
    print("用浏览器打开该 html 查看多医院围栏。")
# Ended by Cursor 10351260 20260409142357842


# Started by Cursor 10351260 20260409142357842
if __name__ == "__main__":
    cli()
# Ended by Cursor 10351260 20260409142357842

