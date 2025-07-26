# GitHub Actions 快速使用指南

## 🚀 快速开始

### 本项目的自动化工作流

我们的项目包含两个主要的自动化流程：

#### 1. 自动发布流程 🏗️
**触发方式**：推送版本标签（如 `v1.0.0`）

```bash
# 创建新版本
git tag v1.2.3
git push origin v1.2.3
```

**自动执行**：
- ✅ 创建 GitHub Release
- ✅ 构建 Linux x86_64 版本
- ✅ 构建 Linux ARM64 版本  
- ✅ 构建中科方德 ARM 优化版
- ✅ 运行兼容性测试
- ✅ 上传所有构建产物

#### 2. 文档网站部署 📚
**触发方式**：推送到 `master` 分支

```bash
git push origin master
```

**自动执行**：
- ✅ 部署项目到 GitHub Pages
- ✅ 更新在线文档

## 📋 常用命令

### 查看工作流状态
```bash
# 查看最近的工作流运行
gh run list

# 查看特定运行的详情
gh run view [run-id]

# 实时监控运行状态
gh run watch
```

### 管理发布
```bash
# 查看所有发布版本
gh release list

# 查看最新发布
gh release view --latest

# 下载发布文件
gh release download v1.2.3
```

## 🔧 工作流文件位置

```
.github/
└── workflows/
    ├── release-builder.yml  # 自动发布流程
    └── deploy-pages.yml     # 文档部署流程
```

## ⚡ 快速故障排查

### 发布失败？
1. 检查标签格式是否正确（必须以 `v` 开头）
2. 确保有 `contents: write` 权限
3. 查看失败日志：`gh run view --log-failed`

### 权限错误？
确保仓库设置中启用了 Actions 权限：
- Settings → Actions → General → Allow all actions

### 构建失败？
1. 检查 `requirements.txt` 是否完整
2. 验证 Python 代码语法
3. 查看具体错误信息

## 📖 更多详细信息

查看完整教程：[GitHub Actions 工作流教程](./github-actions-tutorial.md)

---

💡 **提示**：首次使用时，建议先创建一个测试标签（如 `v0.0.1-test`）来验证工作流是否正常运行。