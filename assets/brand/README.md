# Longjin 品牌资产

GitHub 发布前，把维护者提供的微信二维码原图放到本目录并命名为：

```text
wechat-qr.png
```

然后在 `README.md` 的“维护者”章节加入：

```markdown
![Longjin 微信二维码](assets/brand/wechat-qr.png)
```

在正式报告中需要展示联系方式时，将 `assets/report-template.html` 的 `[[LONGJIN_QR_PATH]]` 替换为报告相对路径，并移除 `#longjin-contact` 元素的 `hidden` 属性。

不得使用模型生成二维码，也不要把微信号、二维码或其他个人联系方式复制到虚构示例报告。
