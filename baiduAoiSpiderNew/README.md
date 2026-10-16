# 百度地图 AOI 爬取项目使用说明

通用脚本 `baidu_aoi_spider.py`：**一条命令**完成「行政区划 → POI 检索 → AOI 围栏解析 → 落盘」全流程。

支持的建筑类别：内置别名 **学校、医院、加油站、公园、银行、超市、餐厅、地铁站**；
也支持**任意百度行业分类**（如 美食、酒店、购物、中餐厅）、**自由关键词**，以及
**「检索词:行业分类」** 组合（如 `咖啡馆:美食`）。

---

## 1. 环境准备

```bash
pip install requests
```

- Python 3.8+（Windows / Linux / macOS 均可）
- 需要百度地图开放平台的**服务端 AK**（Web服务API），申请地址：<https://lbsyun.baidu.com/apiconsole/key>
- 脚本需在项目目录下运行（依赖同目录的 `uid_geo_fence.py`、`coords.py`、`batch_uid_csv_to_html.py`、`batch_data_xian_to_outputs.py`）

## 2. 基本用法

```bash
python baidu_aoi_spider.py --ak 你的AK --province 陕西省
```

> 运行时显示**整体进度条（0-100%，按数量比例推进）**，
> 如 `[总进度] ████████░░░░ 28.4%  检索 320/1140 | 围栏 0/0  学校 | 南京市 检索 2/3`。
> 每个类别爬取前先**预统计**（逐区域读首屏 total，汇总出可获取的 POI 总数作为固定分母），
> 之后每入库 1 条 POI 计 1 格；围栏任务数爬完一个城市后计入；百分比只增不减，全部汇总完成后 100%。

**三个核心参数：**

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `--ak` | 百度地图服务端 AK（必填） | `--ak XXXXXXXXXXXXXXXXXXXX` |
| `--province` | 省份名或城市名（必填） | `--province 陕西省`、`--province 西安市`、`--province 北京市` |
| `--categories` | 类别，可传多个（不传默认全部 8 个内置别名） | `--categories 学校 医院`、`--categories 美食 中餐厅`、`--categories 咖啡馆:美食` |

## 3. 类别映射

内置别名（检索词与行业分类不一致的类别）：

| 类别 | 检索词 query | 百度行业分类 type |
| --- | --- | --- |
| 学校 | 学校 | 教育培训 |
| 医院 | 医院 | 医疗 |
| 加油站 | 加油站 | 加油站 |
| 公园 | 公园 | 旅游景点 |
| 银行 | 银行 | 金融 |
| 超市 | 超市 | 购物 |
| 餐厅 | 餐厅 | 美食 |
| 地铁站 | 地铁站 | 交通设施 |

除内置别名外，`--categories` 直接传任意值即可，无需改代码：

| 写法 | 含义 | 示例 |
| --- | --- | --- |
| 行业分类名 | 检索词与行业分类同值（一级/二级均可） | `--categories 美食 中餐厅` |
| 自由关键词 | 直接按词检索 | `--categories 健身房` |
| `检索词:行业分类` | 自定义组合（冒号后留空 = 不限分类） | `--categories 咖啡馆:美食 健身房:` |

**名称后缀过滤**：部分类别检索词召回范围过宽，会自动只保留名称以指定后缀结尾的 POI
（`baidu_aoi_spider.py` 顶部 `NAME_SUFFIX_RULES` 可扩展）：

| 类别 | 过滤规则 |
| --- | --- |
| 高铁站 | 名称须以「站」结尾（过滤公交站/汽车站/售票点等） |
| 机场 | 名称须以「机场」结尾（过滤航空公司/售票处/停车场等） |

如需修改内置别名的映射，编辑 `baidu_aoi_spider.py` 顶部的 `CATEGORY_MAP` 即可。

## 4. 常用参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--region-mode` | `city_county` | `city_county`：整市 + 县/县级市检索（请求少）；`district`：按每个区/县拆分（结果更全，请求更多） |
| `--out-root` | `outputs_aoi` | 输出根目录 |
| `--crs` | `bd09` | 围栏坐标系：`bd09`（百度坐标，适合百度地图叠加）/ `wgs84`（GPS 坐标，适合 GIS 叠加） |
| `--skip-fence` | 关 | 只产出 POI uid CSV，不拉围栏 |
| `--skip-crawl` | 关 | 跳过 POI 检索，仅用已有 CSV 做围栏/汇总 |
| `--no-html` | 关 | 不生成 HTML 可视化页面 |
| `--overwrite` | 关 | 忽略已有结果，强制重新抓取 |
| `--max-workers` | `8` | 围栏抓取并发线程数 |
| `--timeout` / `--sleep` | `15` / `0.2` | place 接口超时（秒）/ 翻页间隔（秒） |
| `--fence-timeout` | `20` | qt=ext 单 uid 请求超时（秒） |
| `--page-size` | `20` | place 接口每页条数（最大 20） |
| `--html-ak` | 同 `--ak` | HTML 展示用的 JS API ak |

## 5. 使用示例

```bash
# ① 陕西省，默认全部 8 类
python baidu_aoi_spider.py --ak 你的AK --province 陕西省

# ② 只爬 学校 + 医院
python baidu_aoi_spider.py --ak 你的AK --province 陕西省 --categories 学校 医院

# ③ 只爬西安市餐厅，按区县拆分（更全）
python baidu_aoi_spider.py --ak 你的AK --province 西安市 --categories 餐厅 --region-mode district

# ④ 只产出 POI 清单，不拉围栏（最快）
python baidu_aoi_spider.py --ak 你的AK --province 陕西省 --categories 银行 --skip-fence

# ⑤ 围栏输出 WGS84 坐标（供 GIS 使用）
python baidu_aoi_spider.py --ak 你的AK --province 陕西省 --categories 公园 --crs wgs84 --no-html

# ⑥ 任意百度行业分类 / 自由关键词 / 「检索词:行业分类」组合
python baidu_aoi_spider.py --ak 你的AK --province 西安市 --categories 美食 中餐厅
python baidu_aoi_spider.py --ak 你的AK --province 西安市 --categories 咖啡馆:美食 健身房:
```

## 6. 输出结构

```
outputs_aoi/
└── 陕西省/
    └── 学校/
        ├── uid_csv/
        │   └── 西安市_学校_uid.csv          # 每城市 POI 清单（uid/名称/地址/坐标）
        ├── aoi_json/
        │   ├── 西安市_学校.json             # 围栏成功列表（含 fence 点列）
        │   └── 西安市_学校.errors.json      # 围栏失败列表（含失败原因）
        ├── aoi_html/
        │   ├── 西安市_学校.html             # 百度地图可视化（可勾选切换围栏）
        │   └── index.html                   # 类别索引页
        ├── 学校_all.csv                     # 全省 POI 汇总
        ├── 学校_all.json                    # 全省围栏汇总（每条含 city 字段）
        ├── 学校_all.errors.json             # 全省失败汇总
        └── _summary.json                    # 类别统计（POI 数 / 成功 / 失败）
```

围栏 JSON 单条格式：

```json
{
  "uid": "ddfd7c2d8db36cf39ee3219e",
  "name": "西安交通大学",
  "point_count": 128,
  "fence": [{"lng": 108.958, "lat": 34.247}, "..."]
}
```

## 7. 断点续跑

- 直接**重复执行同一命令**即可：已存在的城市 CSV、围栏 JSON 会自动跳过，只补抓缺失部分。
- 行政区划缓存在 `admin_cache/` 目录，重复运行不再请求。
- `--overwrite` 强制全部重抓；`--refresh-admin` 强制刷新行政区划。

## 8. 常见问题

**Q1：为什么有些 POI 没有围栏？**
`qt=ext` 接口只对有大边界数据的 POI 返回 `content.geo`（学校、医院、公园等一般有；连锁小店铺通常没有）。失败项及原因见 `*.errors.json`。

**Q2：大城市的餐厅/银行数量明显偏少？**
`place/v3/region` 单个区域最多返回 **400 条**（20 页 × 20 条），`city_county` 模式下整市检索会被截断。改用 `--region-mode district` 按区县拆分可显著补全（请求数也相应增加）。

**Q3：报 status=302/401 或配额相关错误？**
place 区域检索按请求次数计**每日配额**（以百度控制台显示为准）；行政区划接口和 qt=ext 围栏接口不消耗该配额。可缩小类别/区域，或等次日配额重置。全省 8 类爬取请求量较大，建议先小范围试跑。

**Q4：HTML 打开地图空白？**
HTML 页面使用**JS API（浏览器端）ak**，需要你的 ak 开通浏览器端权限。不影响 CSV/JSON 数据，可用 `--html-ak` 单独指定 JS ak，或 `--no-html` 跳过。

**Q5：坐标是什么坐标系？**
默认 **BD09**（百度坐标，与百度地图叠加无偏移）；`--crs wgs84` 输出 WGS84（GPS/GIS 常用）。围栏原始数据来自接口的 bd09mc 米制坐标，脚本内已做转换。

**Q6：直辖市 / 只爬某个市怎么传？**
`--province` 直接传城市名即可（如 `北京市`、`西安市`），脚本会自动识别并给 region 加前缀，检索粒度自动落到区县。

---

## 附：目录内其他脚本（历史版本）

| 脚本 | 用途 |
| --- | --- |
| `crawl_xian_hospitals_uid.py` | 早期：陕西医院 uid 检索（需预先生成行政区 JSON） |
| `crawl_xian_high-speed-rail_uid.py` | 火车站 uid 检索（`--place-type`/`--region-mode` 可配） |
| `district_search_to_json.py` | 生成 `省_下三级行政区_整理版.json`（新脚本已内置此步骤） |
| `uid_geo_fence.py` | 单 uid 拉围栏（qt=ext），`coords.py` 为坐标转换 |
| `batch_uid_csv_to_html.py` | uid CSV → 围栏 JSON + HTML 展示 |
| `batch_data_xian_to_outputs.py` | 目录内所有 CSV 批量拉围栏 |
| `pipeline_crawl_place_then_batch_aoi.py` | 上述两阶段的 subprocess 串联（针对火车站/医院） |

新脚本 `baidu_aoi_spider.py` 已把上述能力整合为通用单文件流程，一般情况下无需再使用旧脚本。
