<div align="center">

# xhs-chaijie-dsh

**把一个小红书账号的增长逻辑，拆成可验证证据与可执行动作。**

DSH 原生 · 真实封面审计 · 爆款资产复用 · 单页可视化报告

[![DSH Skill](https://img.shields.io/badge/DSH-Skill-172026?style=flat-square)](#安装到-dsh)
[![License: MIT](https://img.shields.io/badge/License-MIT-c92845?style=flat-square)](LICENSE)
[![Maintainer](https://img.shields.io/badge/Maintainer-Longjin-8d1830?style=flat-square)](#维护者)

</div>

## 它解决什么

给出 1-5 个小红书账号主页链接，Skill 会读取公开主页、笔记、互动与真实封面，回答账号为什么能做起来、什么内容有效、如何演化、哪些方法能复制，以及下一步应该做什么。正式分析后默认生成一个可直接打开的单页 HTML 报告，不需要再追问“能不能可视化”。

它也能先帮你找对标。定位没有说清前不会凭行业印象编账号；候选会区分“站内已验证”和“外部搜索待验证”。

## 核心能力

| 能力 | 交付内容 |
|---|---|
| 账号定位 | 人群、场景、长期承诺与核心增长策略 |
| 内容诊断 | 定位、选题、标题、封面、内容价值与主页承接 |
| 真实封面审计 | 封面文字、主体、构图、色彩、钩子、证据与可复制点 |
| 账号演化 | 带日期的探索、转折、稳定阶段与关键保留 |
| 爆款资产复用 | 首个高热、后续变体、数据波动和选题/标题/封面公式 |
| 对标与路线 | 学什么、不学什么、起号基建、验证固化、放大扩展 |
| 合规与证据 | 只使用公开或授权材料，明确事实、推断和缺失字段 |
| 可视化报告 | 响应式、自包含、可离线打开的 7 章 HTML 报告 |

## 报告长什么样

仓库附带一份完全虚构、不会复用用户信息的[示例报告](examples/sample_report.html)。报告固定包含：一分钟结论、账号演化、内容诊断、爆款资产复用、合规边界、发展路线、数据说明与来源。

![xhs-chaijie-dsh 报告预览](assets/github/report-preview.png)

正式报告会从真实账号封面提取主题色，不固定套用小红书红。

## 安装到 DSH

DSH 会扫描用户级 `~/.dsh/skills` 和项目级 `.dsh/skills`。仓库根目录本身就是可安装 Skill，不要再多套一层目录。

### 方式一：下载后运行安装脚本

Windows PowerShell：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
```

macOS / Linux：

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

脚本默认安装到 `~/.dsh/skills/xhs-chaijie-dsh`。已有同名目录时会停止，避免静默覆盖；PowerShell 可在检查旧版本后使用 `-Force`，旧目录会先备份。

### 方式二：直接放入项目

把整个仓库复制到：

```text
你的项目/.dsh/skills/xhs-chaijie-dsh/
```

确认最终入口是：

```text
你的项目/.dsh/skills/xhs-chaijie-dsh/SKILL.md
```

安装后重启 DSH 或开启新会话，让它重新扫描 Skills。

## 使用方式

直接拆账号：

```text
拆解这个小红书账号：https://www.xiaohongshu.com/user/profile/...
```

横向对比：

```text
对比这 3 个小红书账号，找出最值得新号复制的内容结构：
<主页链接 1>
<主页链接 2>
<主页链接 3>
```

先找对标：

```text
我要做一个面向一线城市新手爸妈的辅食账号，真人演示，目标是店铺下单。先帮我找 5 个对标。
```

有链接时 Skill 会直接开始，不强制你先填写定位问卷。只有“找对标”模式才补齐必要画像。

## DSH 兼容设计

- 使用 DSH 可发现的根目录 `SKILL.md` 与 kebab-case 名称。
- 默认允许模型自动调用，也支持用户显式调用。
- 不绑定某个浏览器插件或固定本机路径；运行时按真实能力协商。
- 优先使用用户已授权的本地登录会话，不索要密码或完整 Cookie。
- 浏览器、视觉或预览不可用时会继续寻找宿主能力，再提供材料降级方案。
- HTML、CSS 与 JavaScript 自包含，不依赖 CDN、npm 或网络字体。

## 项目结构

```text
xhs-chaijie-dsh/
├─ SKILL.md                       # DSH 入口与完整执行工作流
├─ assets/report-template.html    # Longjin 可视化报告模板
├─ references/                    # 分析、规则、报告与工具路由
├─ scripts/                       # 安装、诊断、示例构建与验证
├─ examples/                      # 虚构数据示例报告
├─ tests/                         # 自动化测试
├─ LICENSE
└─ NOTICE
```

## 自检与开发

```bash
python scripts/doctor.py
python scripts/build_demo.py
python scripts/validate_skill.py
python scripts/validate_report_links.py examples/sample_report.html
```

仓库 CI 会在 Windows 与 Ubuntu 上验证 DSH 元数据、必备资源、七章报告结构、外链安全和本地图片。

## 隐私与合规

- 只分析公开可见内容或用户主动提供的数据。
- 不绕过登录、验证码、权限、频控或平台风控。
- 不编造曝光、点击率、完播率、成交、转化率或涨粉数据。
- 没看见真实封面时不猜视觉元素。
- 示例账号与数据完全虚构，不使用当前用户的履历、公司、城市或历史对话。
- 平台规则会更新，高风险行业与商业合作结论应在执行时核对官方页面。

## 免费版边界与 Pro 路线

当前仓库是完整可用的免费版，账号拆解、对标发现、真实封面审计、爆款归因、发展路线与 HTML 报告均不缩水。未来的 `xhs-chaijie-dsh-pro` 会作为独立付费产品探索更大规模的数据接入、跨账号批量工作流与其他项目能力整合，不会在本仓库放置不可运行的付费占位功能。

## 维护者

**Longjin**

微信二维码会在发布 GitHub 前使用维护者提供的原图加入，本仓库不生成或冒用联系方式。二维码缺失不会影响 Skill 的分析与报告能力。

## 许可证与上游

本项目使用 MIT License。它是 [`acheAIsuiyimen/ache-chaijie-skill`](https://github.com/acheAIsuiyimen/ache-chaijie-skill) 的 DSH 适配与增强版本，由 Longjin 维护。上游版权与许可声明保留在 [LICENSE](LICENSE) 和 [NOTICE](NOTICE) 中。

---

<div align="center">Made for DSH · Maintained by Longjin</div>
