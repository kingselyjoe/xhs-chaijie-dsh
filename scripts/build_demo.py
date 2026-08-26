#!/usr/bin/env python3
"""Build the fictional, privacy-safe visual demo from the report template."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "report-template.html"
OUTPUT = ROOT / "examples" / "sample_report.html"
XHS = "https://www.xiaohongshu.com/"


VALUES = {
    "ACCOUNT_NAME": "周末小厨房（虚构示例）",
    "ACCOUNT_CATEGORY": "一人食 · 效率做饭",
    "COLLECTED_DATE": "2026-08-27",
    "ACCOUNT_URL": XHS,
    "AVATAR_PATH": "assets/avatar.svg",
    "CORE_ENGINE": "明确的下班场景",
    "REPEAT_ACTION": "复用时间承诺与步骤清单",
    "VISIBLE_RESULT": "形成稳定的效率做饭识别",
    "ONE_MINUTE_SUMMARY": "这是一个仅用于展示报告结构的虚构账号。它把每篇内容都压缩成可验证的时间、预算和步骤，用户无需先认识创作者，也能立即判断内容是否值得保存。",
    "METRIC_1": "24 篇", "METRIC_1_LABEL": "虚构可见样本",
    "METRIC_2": "3 类", "METRIC_2_LABEL": "稳定内容支柱",
    "METRIC_3": "4 张", "METRIC_3_LABEL": "封面视觉样本",
    "METRIC_4": "90 天", "METRIC_4_LABEL": "示例观察窗口",
    "STRATEGY_TITLE": "把做饭变成时间管理", "STRATEGY_TEXT": "同一人群、同一下班场景，只替换菜谱和限制条件。",
    "ADVANTAGE_TITLE": "承诺可被画面证明", "ADVANTAGE_TEXT": "成品、时间与食材数量都在封面或正文交付。",
    "PROBLEM_TITLE": "后期出现机械复刻", "PROBLEM_TEXT": "只换菜名、不增加步骤或选择理由时，信息增量变弱。",
    "HERO_NOTE_URL": XHS, "HERO_COVER_PATH": "assets/cover-1.svg", "HERO_EVIDENCE": "虚构样本中，“明确时长 + 完整成品 + 步骤清单”同时出现，内容承诺最完整。",
    "EVOLUTION_CONCLUSION": "从记录菜谱转向解决下班后时间与预算问题，是可见样本中的关键变化。",
    "PHASE_1_DATE": "2026.01—02", "PHASE_1_TITLE": "记录探索", "PHASE_1_NOTE": "今天吃什么", "PHASE_1_URL": XHS, "PHASE_1_ACTION": "以成品记录为主，标题宽泛。", "PHASE_1_CHANGE": "保留真实成品，放弃无明确对象的日记式标题。",
    "PHASE_2_DATE": "2026.03—04", "PHASE_2_TITLE": "场景聚焦", "PHASE_2_NOTE": "下班 30 分钟晚餐", "PHASE_2_URL": XHS, "PHASE_2_ACTION": "加入时间、预算和一人食限制。", "PHASE_2_CHANGE": "将“好吃”改造成“下班可执行”。",
    "PHASE_3_DATE": "2026.05—06", "PHASE_3_TITLE": "结构复用", "PHASE_3_NOTE": "三菜一汤 45 分钟", "PHASE_3_URL": XHS, "PHASE_3_ACTION": "固定成品图、数字标题和步骤清单。", "PHASE_3_CHANGE": "保留场景与结构，每篇增加菜谱和备菜信息。",
    "EVOLUTION_TURNING_POINT": "首次把“下班后”写进标题并用时间顺序兑现，账号才从个人记录变为稳定解决方案。",
    "DIAGNOSIS_CONCLUSION": "定位、选题和内容价值已形成闭环，下一步不是扩人群，而是增加同一结构里的信息增量。",
    "LEVEL_1": "强", "DIAG_1_EVIDENCE": "主页和近期样本持续指向下班做饭。", "DIAG_1_JUDGEMENT": "人群和场景明确。", "DIAG_1_ACTION": "继续锁定工作日晚餐，不提前扩到所有家庭餐。",
    "LEVEL_2": "强", "DIAG_2_EVIDENCE": "时间、预算、一锅到底反复出现。", "DIAG_2_JUDGEMENT": "需求稳定且可系列化。", "DIAG_2_ACTION": "按限制条件建立栏目，而非随机发菜名。",
    "LEVEL_3": "中", "DIAG_3_EVIDENCE": "数字与成品图稳定，但低效样本标题宽泛。", "DIAG_3_JUDGEMENT": "识别度已建立，承诺强弱仍波动。", "DIAG_3_ACTION": "封面只保留一个主承诺，并增加证据。",
    "LEVEL_4": "强", "DIAG_4_EVIDENCE": "虚构正文包含备菜顺序、预算和替代食材。", "DIAG_4_JUDGEMENT": "内容能直接执行。", "DIAG_4_ACTION": "每篇至少增加一个可带走清单。",
    "LEVEL_5": "中", "DIAG_5_EVIDENCE": "置顶说明人群，但栏目入口不够清楚。", "DIAG_5_JUDGEMENT": "承诺一致，导航较弱。", "DIAG_5_ACTION": "置顶分别承接新手、预算和时间三个入口。",
    "ASSET_CONCLUSION": "这个示例复用的是“下班限制条件 + 完整成品 + 可执行清单”，而不是同一张封面。",
    "CORE_ASSET": "下班场景 × 明确时间/预算 × 成品证据 × 可保存步骤",
    "BAR_1": "100", "BAR_1_VALUE": "基准", "BAR_2": "72", "BAR_2_VALUE": "0.72×", "BAR_3": "24", "BAR_3_VALUE": "0.24×",
    "HIGH_TITLE": "三菜一汤，只花 45 分钟", "HIGH_REASON": "人群、结果、时间和成品证据同时成立，正文再用顺序清单兑现。",
    "LOW_TITLE": "今天吃什么", "LOW_REASON": "只有泛场景和成品，没有对象、限制或新增信息，用户难以预判收益。",
    "TOPIC_FORMULA": "具体人群 + 当下限制 + 一顿饭的完整结果",
    "TITLE_FORMULA": "场景 + 数字限制 + 明确成果",
    "COVER_FORMULA": "单一主标题 + 完整成品 + 一项证据标签",
    "RISK_1_TITLE": "效果承诺", "RISK_1_TEXT": "时间与预算需要展示口径，不能把个例写成人人保证。",
    "RISK_2_TITLE": "食品安全", "RISK_2_TEXT": "隔夜、保存与加热建议需要注明条件和边界。",
    "RISK_3_TITLE": "商业合作", "RISK_3_TEXT": "品牌与食材合作需要按当期规则清晰标识。",
    "RISK_4_TITLE": "素材版权", "RISK_4_TEXT": "菜谱、图片和音乐使用原创或已获授权素材。",
    "LEARN_TITLE": "学限制条件，不抄菜谱", "LEARN_TEXT": "值得迁移的是把内容变成具体场景下的解决方案，以及用结果物兑现承诺。",
    "BUILD_TITLE": "一个稳定厨房场景", "BUILD_TEXT": "先固定人群、拍摄位置、封面信息层级和正文步骤，再扩菜系。",
    "ROUTE_1_GOAL": "建立下班晚餐承诺", "ROUTE_1_TASK": "定义 3 个支柱与固定视觉结构。", "ROUTE_1_KEEP": "人群、场景和主承诺。",
    "ROUTE_2_GOAL": "验证两类限制条件", "ROUTE_2_TASK": "每次只改时间或预算一个变量。", "ROUTE_2_SIGNAL": "同一结构多篇高于自身中位水平。",
    "ROUTE_3_GOAL": "扩展相邻晚餐需求", "ROUTE_3_TASK": "增加合集、替代方案和备餐流程。", "ROUTE_3_SIGNAL": "评论持续提出同类下一步需求。",
    "CONTENT_RATIO": "建议配比：50% 核心效率晚餐 / 25% 预算挑战 / 25% 食材替代与复盘。",
    "TITLE_EXAMPLES": "“加班回家 30 分钟，两菜一汤按这个顺序做” · “20 元工作日晚餐，第二天还能带饭” · “只有一口锅，7 种食材这样安排”",
    "SOURCE_TYPE": "全部为虚构演示数据", "MISSING_FIELDS": "真实账号、真实互动、真实评论与后台数据",
    "LONGJIN_QR_PATH": "assets/avatar.svg",
}

for i in range(1, 5):
    VALUES[f"COVER_{i}_URL"] = XHS
    VALUES[f"COVER_{i}_PATH"] = f"assets/cover-{i}.svg"
    VALUES[f"COVER_{i}_TITLE"] = ["三菜一汤 45 分钟", "一锅到底炖饭", "20 元吃两顿", "今天吃什么"][i - 1]
    VALUES[f"COVER_{i}_DATA"] = ["高热基准", "有效复用", "结构迭代", "低效样本"][i - 1]
    VALUES[f"COVER_{i}_LABEL"] = ["承诺完整", "场景明确", "证据增强", "信息过泛"][i - 1]

VALUES["ASSET_ROWS"] = "".join(
    f'<tr><td><a href="{XHS}" target="_blank" rel="noopener noreferrer">{title}</a></td><td>{date}</td><td>{repeat}</td><td>{change}</td><td>{data}</td><td>{label}</td></tr>'
    for title, date, repeat, change, data, label in [
        ("三菜一汤 45 分钟", "2026-05-08", "时间承诺、完整成品", "三道新菜与顺序", "高热基准", "首个高热"),
        ("一锅到底炖饭", "2026-05-19", "下班场景、数字标题", "烹饪工具", "相对高热", "有效复用"),
        ("20 元吃两顿", "2026-06-02", "限制条件、成品证据", "预算表", "中高段", "结构迭代"),
        ("今天吃什么", "2026-06-12", "成品图", "缺少明确限制", "低段", "低效样本"),
        ("30 分钟备餐", "2026-06-20", "时间承诺、步骤", "两日份结果", "中段", "可继续验证"),
    ]
)
VALUES["SOURCE_ITEMS"] = (
    f'<li><a href="{XHS}" target="_blank" rel="noopener noreferrer">小红书首页（仅作示例链接）</a></li>'
    '<li><a href="https://agree.xiaohongshu.com/h5/terms/ZXXY20221213003/-1" target="_blank" rel="noopener noreferrer">小红书社区规范</a></li>'
    '<li>本报告账号、数据、结论均为虚构演示，不对应真实个人。</li>'
)


def main():
    html = TEMPLATE.read_text(encoding="utf-8")
    for key, value in VALUES.items():
        html = html.replace(f"[[{key}]]", value)
    leftovers = sorted(set(re.findall(r"\[\[[^\[\]]+\]\]", html)))
    if leftovers:
        raise SystemExit("Unresolved demo placeholders: " + ", ".join(leftovers))
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
