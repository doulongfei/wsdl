# 📖 项目文档

欢迎来到 WSDL SOAP 客户端工具的文档中心！

## 🚀 快速开始

- [README.md](../README.md) - 项目概述和基本使用 (English)
- [README.zh-CN.md](../README.zh-CN.md) - 项目概述和基本使用 (中文)

## 📚 GitHub Actions 自动化

### 🎯 快速上手
- [⚡ GitHub Actions 快速指南](github-actions-quick-guide.md) - 5分钟掌握基本操作

### 📖 深入学习  
- [📚 GitHub Actions 工作流教程](github-actions-tutorial.md) - 全面的工作流指南
- [🔧 GitHub Actions 示例模板](github-actions-examples.md) - 可复用的工作流模板

## 🏗️ 当前工作流

我们的项目包含以下自动化流程：

### 1. 自动发布流程 (`release-builder.yml`)
- **触发**: 推送版本标签 (如 `v1.0.0`)
- **功能**: 
  - ✅ 多平台构建 (x86_64, ARM64)
  - ✅ 中科方德 ARM 优化版本
  - ✅ 自动创建 GitHub Release
  - ✅ 兼容性测试报告

### 2. 文档部署流程 (`deploy-pages.yml`)
- **触发**: 推送到 `master` 分支
- **功能**: 
  - ✅ 自动部署到 GitHub Pages
  - ✅ 在线文档更新

## 🎯 使用场景

### 开发者
```bash
# 日常开发流程
git add .
git commit -m "feat: 新功能"
git push origin master

# 发布新版本
git tag v1.2.3
git push origin v1.2.3
```

### 运维人员
```bash
# 监控构建状态
gh run list

# 查看失败详情
gh run view --log-failed

# 管理发布
gh release list
```

### 用户
```bash
# 下载最新版本
gh release download --latest

# 查看所有可用版本
gh release list
```

## 🔍 故障排查

常见问题和解决方案：

1. **权限错误** → 检查仓库 Actions 权限设置
2. **构建失败** → 查看 `requirements.txt` 和代码语法
3. **发布失败** → 确认标签格式 (`v*`) 和权限配置
4. **部署失败** → 检查 GitHub Pages 设置

详细故障排查请参考 [GitHub Actions 教程](github-actions-tutorial.md#故障排查)。

## 📋 检查清单

### 首次设置
- [ ] 启用仓库 Actions 权限
- [ ] 配置 GitHub Pages (如需要)
- [ ] 测试工作流 (创建测试标签)
- [ ] 验证权限配置

### 日常维护
- [ ] 定期更新 Actions 版本
- [ ] 监控构建状态
- [ ] 检查安全扫描结果
- [ ] 维护文档同步

## 🌟 贡献指南

欢迎贡献改进建议：

1. 发现问题请创建 [Issue](https://github.com/doulongfei/wsdl/issues)
2. 改进建议请提交 [Pull Request](https://github.com/doulongfei/wsdl/pulls)
3. 文档改进也很欢迎！

## 📞 获取帮助

- 📖 查看 [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- 💬 在 GitHub Issues 中提问
- 🔍 搜索 [Stack Overflow](https://stackoverflow.com/questions/tagged/github-actions)

---

💡 **提示**: 建议按照 "快速指南 → 详细教程 → 示例模板" 的顺序学习，循序渐进掌握 GitHub Actions。