# Started by Cursor 10351260 20260409153303845
"""
读取 data/西安 目录下的所有 *_uid.csv，批量抓取 AOI 围栏（经纬度）并输出：
- 结果 JSON 到指定结果目录
- 展示 HTML 到指定 HTML 目录

每个 CSV 会生成 3 个文件：
- <stem>.json            成功围栏列表（含 fence 点列）
- <stem>.errors.json     失败列表（含 uid/name/error）
- <stem>.html            百度地图前端展示（可勾选切换围栏）

另生成一个 index.html，汇总所有区县的展示页面入口。
"""
# Ended by Cursor 10351260 20260409153303845

from __future__ import annotations

# Started by Cursor 10351260 20260409153303845
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from batch_uid_csv_to_html import (
    DEFAULT_BMAP_AK,
    fetch_fences_from_rows,
    generate_multi_fence_html,
    load_uid_rows,
)
# Ended by Cursor 10351260 20260409153303845


# Started by Cursor 10351260 20260409153622412
# 默认输入目录（可通过 CLI 覆盖）
DEFAULT_INPUT_DIR = Path("data") / "西安"
# 输出目录按省份名自动构建：
# outputs/<省份名>/aoi_json
# outputs/<省份名>/aoi_html
DEFAULT_OUT_ROOT_DIR = Path("outputs_aoi/train")
# Ended by Cursor 10351260 20260409153622412


# Started by Cursor 10351260 20260409153303845
def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)
# Ended by Cursor 10351260 20260409153303845


# Started by Cursor 10351260 20260409195807901
def _extract_city_name_from_csv_stem(stem: str) -> str:
    """
    从 CSV 文件 stem 推断“城市名”，用于进度打印。
    约定：常见文件名形如「西安市长安区_医院_uid」或「榆林市_医院_uid」。
    - 优先取第一个 "_" 之前的片段
    - 再从中截取到第一个「市」为止（含「市」）
    - 若找不到「市」，则直接返回该片段
    """
    head = (stem.split("_", 1)[0] or "").strip()
    if not head:
        return "未知城市"
    if "市" in head:
        return head.split("市", 1)[0] + "市"
    return head
# Ended by Cursor 10351260 20260409195807901


# Started by Cursor 10351260 20260409153303845
def process_one_csv(
    csv_path: Path,
    out_data_dir: Path,
    out_html_dir: Path,
    ak: str,
    timeout: float,
    sleep_s: float,
    limit: int,
) -> Tuple[Path, Path, Path]:
    """
    返回：(json_path, errors_json_path, html_path)
    """
    rows = load_uid_rows(str(csv_path))
    items, errors = fetch_fences_from_rows(rows, timeout=timeout, sleep_s=sleep_s, limit=limit)

    stem = csv_path.stem
    json_path = out_data_dir / f"{stem}.json"
    errors_json_path = out_data_dir / f"{stem}.errors.json"
    html_path = out_html_dir / f"{stem}.html"

    json_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    errors_json_path.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")

    # 标题用文件名（如：西安市长安区_医院_uid）
    title = stem.replace("_uid", "").replace("_", " ")
    generate_multi_fence_html(items, out_html=str(html_path), ak=ak, title=title)

    return json_path, errors_json_path, html_path
# Ended by Cursor 10351260 20260409153303845


# Started by Cursor 10351260 20260409195023180
def _make_safe_stem(in_dir: Path, csv_path: Path) -> str:
    """
    生成稳定且不冲突的输出文件 stem。
    - 若目录内存在子目录：用相对路径拼成 stem，并把分隔符替换为 "__"
    - 否则：用 csv_path.stem
    """
    try:
        rel = csv_path.relative_to(in_dir).with_suffix("")
        rel_str = rel.as_posix().strip().replace("/", "__")
        return rel_str if rel_str else csv_path.stem
    except Exception:
        return csv_path.stem
# Ended by Cursor 10351260 20260409195023180


# Started by Cursor 10351260 20260409153303845
def generate_index_html(entries: List[Dict[str, Any]], out_path: Path, title: str = "西安 AOI 围栏索引") -> Path:
    js_entries = json.dumps(entries, ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Arial,Helvetica,sans-serif; margin: 24px; }}
    .card {{ max-width: 960px; margin: 0 auto; }}
    h1 {{ font-size: 20px; margin: 0 0 12px; }}
    .meta {{ color:#666; margin-bottom: 14px; }}
    .list {{ border: 1px solid rgba(0,0,0,.08); border-radius: 12px; overflow:hidden; }}
    .row {{ display:flex; gap:12px; align-items:center; padding: 10px 12px; border-top: 1px solid rgba(0,0,0,.06); }}
    .row:first-child {{ border-top:0; }}
    a {{ color:#1e60ff; text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .name {{ flex:1; }}
    .count {{ color:#555; }}
    code {{ background: rgba(0,0,0,.04); padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>{title}</h1>
    <div class="meta">点击进入各区县围栏展示页面（HTML）。</div>
    <div class="list" id="list"></div>
    <div class="meta" style="margin-top:16px;">
      输出目录：<code>{out_path.parent.as_posix()}</code>
    </div>
  </div>

  <script>
    const entries = {js_entries};
    const list = document.getElementById('list');
    entries.forEach(e => {{
      const row = document.createElement('div');
      row.className = 'row';
      const name = document.createElement('div');
      name.className = 'name';
      const a = document.createElement('a');
      a.href = e.html;
      a.textContent = e.title;
      a.target = '_blank';
      name.appendChild(a);
      const count = document.createElement('div');
      count.className = 'count';
      count.textContent = `成功: ${'{'}e.success{'}'} / 失败: ${'{'}e.errors{'}'}`;
      row.appendChild(name);
      row.appendChild(count);
      list.appendChild(row);
    }});
  </script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    return out_path
# Ended by Cursor 10351260 20260409153303845


# Started by Cursor 10351260 20260409153303845
def main(
    input_dir: str = str(DEFAULT_INPUT_DIR),
    out_root_dir: str = str(DEFAULT_OUT_ROOT_DIR),
    province_name: str | None = None,
    ak: str = DEFAULT_BMAP_AK,
    timeout: float = 20.0,
    sleep_s: float = 0.2,
    limit: int = 0,
) -> Path:
    # Started by Cursor 10351260 20260409195023180
    print("[INFO] 开始批量处理 AOI 围栏（按省份落盘）")
    # Ended by Cursor 10351260 20260409195023180
    in_dir = Path(input_dir)
    prov = (province_name or in_dir.name).strip()
    if not prov:
        raise ValueError("province_name 为空：请传 --province-name 或保证输入目录名非空")

    root_dir = Path(out_root_dir) / prov
    data_dir = root_dir / "aoi_json"
    html_dir = root_dir / "aoi_html"
    _ensure_dir(data_dir)
    _ensure_dir(html_dir)
    # Started by Cursor 10351260 20260409154111122
    print(f"[INFO] 输入目录: {in_dir.as_posix()}")
    print(f"[INFO] 省份: {prov}")
    print(f"[INFO] 输出 JSON 目录: {data_dir.as_posix()}")
    print(f"[INFO] 输出 HTML 目录: {html_dir.as_posix()}")
    # Ended by Cursor 10351260 20260409154111122

    # Started by Cursor 10351260 20260409195023180
    # 递归扫描：目录内所有 CSV（含子目录）
    csv_files = sorted(in_dir.rglob("*.csv"))
    # Ended by Cursor 10351260 20260409195023180
    if not csv_files:
        raise FileNotFoundError(f"未找到 CSV：{in_dir.as_posix()}/**/*.csv")
    # Started by Cursor 10351260 20260409154111122
    print(f"[INFO] 共发现 CSV: {len(csv_files)}")
    # Ended by Cursor 10351260 20260409154111122

    index_entries: List[Dict[str, Any]] = []
    # Started by Cursor 10351260 20260409195807901
    # city_name -> {"csv": int, "uids": int, "success": int, "errors": int}
    city_stats: Dict[str, Dict[str, int]] = {}
    # Ended by Cursor 10351260 20260409195807901
    for idx, csv_path in enumerate(csv_files, start=1):
        # Started by Cursor 10351260 20260409154111122
        # Started by Cursor 10351260 20260409195023180
        rel = None
        try:
            rel = csv_path.relative_to(in_dir).as_posix()
        except Exception:
            rel = csv_path.name
        print(f"[INFO] ({idx}/{len(csv_files)}) 处理 CSV: {rel}")
        # Ended by Cursor 10351260 20260409195023180
        # Ended by Cursor 10351260 20260409154111122
        rows = load_uid_rows(str(csv_path))
        # Started by Cursor 10351260 20260409154111122
        print(f"[INFO] 读取 uid 行数: {len(rows)}")
        # Ended by Cursor 10351260 20260409154111122
        items, errors = fetch_fences_from_rows(rows, timeout=timeout, sleep_s=sleep_s, limit=limit)
        # Started by Cursor 10351260 20260409154111122
        print(f"[INFO] 围栏抓取完成: 成功 {len(items)} 条 / 失败 {len(errors)} 条")
        # Ended by Cursor 10351260 20260409154111122

        # Started by Cursor 10351260 20260409195807901
        stem_for_city = _make_safe_stem(in_dir, csv_path)
        city_name = _extract_city_name_from_csv_stem(stem_for_city)
        uids_total = len(rows) if limit <= 0 else min(len(rows), limit)
        s = city_stats.setdefault(city_name, {"csv": 0, "uids": 0, "success": 0, "errors": 0})
        s["csv"] += 1
        s["uids"] += int(uids_total)
        s["success"] += int(len(items))
        s["errors"] += int(len(errors))
        print(
            f"[CITY] {city_name} 进度：已处理CSV={s['csv']}，已处理医院(uid行)={s['uids']}，"
            f"围栏成功={s['success']}，失败={s['errors']}"
        )
        # Ended by Cursor 10351260 20260409195807901

        # Started by Cursor 10351260 20260409195023180
        stem = _make_safe_stem(in_dir, csv_path)
        # Ended by Cursor 10351260 20260409195023180
        json_path = data_dir / f"{stem}.json"
        errors_json_path = data_dir / f"{stem}.errors.json"
        html_path = html_dir / f"{stem}.html"

        json_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        errors_json_path.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
        # Started by Cursor 10351260 20260409154111122
        print(f"[INFO] 已写入: {json_path.name}, {errors_json_path.name}")
        # Ended by Cursor 10351260 20260409154111122

        title = stem.replace("_uid", "").replace("_", " ")
        if items:
            generate_multi_fence_html(items, out_html=str(html_path), ak=ak, title=title)
            # Started by Cursor 10351260 20260409154111122
            print(f"[INFO] 已生成 HTML: {html_path.name}")
            # Ended by Cursor 10351260 20260409154111122
        else:
            # 没有任何成功围栏时也生成一个空页，方便统一入口
            # Started by Cursor 10351260 20260409153844339
            empty_html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
</head>
<body style="font-family:Arial;margin:24px;">
  <h3>{title}</h3>
  <p>无可展示围栏（全部失败）。</p>
</body>
</html>
"""
            html_path.write_text(empty_html, encoding="utf-8")
            # Ended by Cursor 10351260 20260409153844339
            # Started by Cursor 10351260 20260409154111122
            print(f"[WARN] 全部失败，生成空 HTML: {html_path.name}")
            # Ended by Cursor 10351260 20260409154111122

        index_entries.append(
            {
                "title": title,
                "csv": csv_path.name,
                "json": json_path.name,
                "errors_json": errors_json_path.name,
                "html": html_path.name,
                "success": len(items),
                "errors": len(errors),
            }
        )

    index_path = html_dir / "index.html"
    # Started by Cursor 10351260 20260409195023180
    generate_index_html(index_entries, index_path, title=f"{prov} 各 CSV 医院 AOI 围栏索引")
    # Ended by Cursor 10351260 20260409195023180
    # Started by Cursor 10351260 20260409154111122
    print(f"[INFO] 已生成索引页: {index_path.as_posix()}")
    # Ended by Cursor 10351260 20260409154111122
    return index_path
# Ended by Cursor 10351260 20260409153303845


# Started by Cursor 10351260 20260409153303845
def cli() -> None:
    # Started by Cursor 10351260 20260409195023180
    parser = argparse.ArgumentParser(description="输入目录内所有 CSV 批量抓取 AOI 围栏，按省份输出 JSON/HTML")
    parser.add_argument("--input-dir", required=True, help="输入目录（会递归扫描其中所有 *.csv）")
    parser.add_argument(
        "--province-name",
        default=None,
        help="省份名（用于输出目录名；默认取 input-dir 的目录名）",
    )
    # Ended by Cursor 10351260 20260409195023180
    # Started by Cursor 10351260 20260409153622412
    parser.add_argument(
        "--out-root-dir",
        default=str(DEFAULT_OUT_ROOT_DIR),
        help="输出根目录（默认 outputs；会在其下自动创建 outputs/<省份名>/aoi_json 与 aoi_html）",
    )
    # Ended by Cursor 10351260 20260409153622412
    parser.add_argument("--ak", default=DEFAULT_BMAP_AK, help="百度地图 JS API ak")
    parser.add_argument("--timeout", type=float, default=20.0, help="单个 uid 请求超时（秒）")
    parser.add_argument("--sleep", type=float, default=0.2, help="每次请求间隔（秒）")
    parser.add_argument("--limit", type=int, default=0, help="每个 CSV 限制处理前 N 条（0=不限制）")
    args = parser.parse_args()


    index_path = main(
        input_dir=args.input_dir,
        out_root_dir=args.out_root_dir,
        province_name=args.province_name,
        ak=args.ak,
        timeout=args.timeout,
        sleep_s=args.sleep,
        limit=args.limit,
    )
    print(f"已生成索引页：{index_path}")
    print("用浏览器打开该 index.html 进入各区县围栏页面。")
# Ended by Cursor 10351260 20260409153303845


# Started by Cursor 10351260 20260409153303845
if __name__ == "__main__":
    cli()
# Ended by Cursor 10351260 20260409153303845

