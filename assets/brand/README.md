# Longjin 品牌资产

本目录保存由维护者本人提供的品牌资产：

```text
wechat-qr.png
```

GitHub 首页在 `README.md` 的“维护者”章节直接引用这张原图：

```markdown
<img src="assets/brand/wechat-qr.png" alt="Longjin 微信二维码" width="220">
```

在正式报告中需要展示联系方式时，把 `wechat-qr.png` 复制到报告的本地资源目录，将 `assets/report-template.html` 的 `[[LONGJIN_QR_PATH]]` 替换为报告相对路径，并移除 `#longjin-contact` 元素的 `hidden` 属性。默认保持隐藏，避免在客户报告或虚构示例中强制加入维护者推广信息。

不得重绘、裁切、解析或使用模型生成二维码，也不要把微信号、二维码或其他个人联系方式复制到虚构示例报告。
