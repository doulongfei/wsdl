# GitHub Actions 工作流教程

## 目录
- [什么是 GitHub Actions？](#什么是-github-actions)
- [基础概念](#基础概念)
- [工作流语法](#工作流语法)
- [本项目的工作流配置](#本项目的工作流配置)
- [如何使用](#如何使用)
- [常见问题和解决方案](#常见问题和解决方案)
- [最佳实践](#最佳实践)

## 什么是 GitHub Actions？

GitHub Actions 是 GitHub 提供的持续集成和持续部署 (CI/CD) 平台，允许您在 GitHub 仓库中自动化构建、测试和部署流程。

### 主要特点：
- **事件驱动**：基于仓库事件（如推送、拉取请求、发布等）自动触发
- **多平台支持**：支持 Linux、macOS、Windows 和容器化环境
- **预构建动作**：丰富的社区和官方预构建动作库
- **并行执行**：支持多任务并行运行，提高效率
- **免费额度**：公开仓库免费使用，私有仓库有免费额度

## 基础概念

### 1. 工作流 (Workflow)
工作流是定义在 `.github/workflows/` 目录下的 YAML 文件，包含一个或多个任务。

### 2. 事件 (Events)
触发工作流运行的仓库活动，如：
- `push`：代码推送
- `pull_request`：拉取请求
- `release`：发布
- `schedule`：定时执行
- `workflow_dispatch`：手动触发

### 3. 任务 (Jobs)
工作流中的执行单元，可以并行或按依赖顺序运行。

### 4. 步骤 (Steps)
任务中的具体执行操作，可以是运行命令或使用动作。

### 5. 动作 (Actions)
可重用的代码单元，可以是自定义脚本或社区/官方提供的预构建动作。

### 6. 运行器 (Runners)
执行工作流的服务器，GitHub 提供托管运行器，也可使用自托管运行器。

## 工作流语法

### 基本结构
```yaml
name: 工作流名称

on:
  # 触发事件
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: 步骤名称
        uses: actions/checkout@v4
      - name: 运行命令
        run: echo "Hello World"
```

### 常用语法元素

#### 1. 触发条件 (`on`)
```yaml
on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # 每天午夜运行
  workflow_dispatch:      # 手动触发
```

#### 2. 任务配置 (`jobs`)
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
```

#### 3. 权限配置 (`permissions`)
```yaml
permissions:
  contents: write    # 写入仓库内容
  pull-requests: read # 读取 PR
  pages: write       # 写入 GitHub Pages
  id-token: write    # OIDC token
```

#### 4. 环境变量和密钥
```yaml
env:
  NODE_VERSION: 16

jobs:
  deploy:
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: echo "Deploying with API key"
```

## 本项目的工作流配置

我们的项目包含两个主要工作流：

### 1. 自动发布工作流 (`release-builder.yml`)

**功能**：当推送新版本标签时，自动构建多平台二进制文件并创建 GitHub Release。

**触发条件**：
```yaml
on:
  push:
    tags:
      - 'v*'  # 任何以 'v' 开头的标签
```

**主要任务**：

#### a) 创建发布 (`create_release`)
- 使用 `softprops/action-gh-release@v2` 创建 GitHub Release
- 输出 `upload_url` 供其他任务使用

#### b) 多架构构建 (`build`)
- 使用矩阵策略并行构建 x86_64 和 aarch64 架构
- 使用 PyInstaller 将 Python 脚本打包为独立可执行文件
- 自动上传构建产物到 Release

#### c) 中科方德 ARM 特别构建 (`build_fedora_arm`)
- 专门为中科方德 ARM 系统优化的构建
- 创建包含文档的 tar.gz 包
- 包含中文说明文档

#### d) ARM 环境测试 (`test_on_arm`, `test_zhongke_fangde_arm`)
- 在 ARM 环境中测试兼容性
- 生成兼容性报告

### 2. GitHub Pages 部署工作流 (`deploy-pages.yml`)

**功能**：当推送到 master 分支时，自动部署项目到 GitHub Pages。

**触发条件**：
```yaml
on:
  push:
    branches:
      - master
```

**部署流程**：
1. 检出代码
2. 配置 Pages
3. 上传整个仓库作为站点内容
4. 部署到 GitHub Pages

## 如何使用

### 1. 创建新发布

要触发自动发布流程：

```bash
# 1. 确保代码已提交并推送
git add .
git commit -m "feat: 新功能描述"
git push origin master

# 2. 创建版本标签
git tag v1.2.3

# 3. 推送标签触发发布
git push origin v1.2.3
```

### 2. 监控工作流运行

```bash
# 使用 GitHub CLI 查看工作流状态
gh run list

# 查看特定工作流运行详情
gh run view [run-id]

# 查看实时日志
gh run watch
```

### 3. 手动触发工作流

对于支持手动触发的工作流：

```bash
# 通过 GitHub CLI 手动触发
gh workflow run "workflow-name"

# 或在 GitHub 网页界面的 Actions 标签页点击 "Run workflow"
```

### 4. 查看发布结果

```bash
# 列出所有发布
gh release list

# 查看特定发布详情
gh release view v1.2.3

# 下载发布资产
gh release download v1.2.3
```

## 常见问题和解决方案

### 1. 权限问题

**问题**：工作流因权限不足失败
```
Error: Resource not accessible by integration
```

**解决方案**：
```yaml
permissions:
  contents: write  # 添加必要权限
```

### 2. 密钥配置问题

**问题**：无法访问机密变量
```
Error: Secret "API_KEY" not found
```

**解决方案**：
1. 在仓库设置 → Secrets and variables → Actions 中添加密钥
2. 确保在工作流中正确引用：`${{ secrets.API_KEY }}`

### 3. 构建失败

**问题**：依赖安装或构建失败

**解决方案**：
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    # 添加重试机制
  retry: 3
```

### 4. 并发问题

**问题**：多个工作流同时运行导致冲突

**解决方案**：
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 5. 大文件处理

**问题**：构建产物过大导致上传失败

**解决方案**：
```yaml
- name: Compress artifacts
  run: |
    tar -czf dist.tar.gz dist/
    # GitHub Release 单文件限制 2GB
```

## 最佳实践

### 1. 工作流组织

```
.github/
└── workflows/
    ├── ci.yml           # 持续集成（测试、检查）
    ├── release.yml      # 发布流程
    ├── deploy.yml       # 部署流程
    └── cleanup.yml      # 清理任务
```

### 2. 使用矩阵策略进行多环境测试

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: [3.8, 3.9, 3.10, 3.11]
  fail-fast: false  # 一个失败不影响其他
```

### 3. 缓存依赖以提高性能

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### 4. 使用条件执行

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy.sh
```

### 5. 工作流模板化

创建可重用的工作流：

```yaml
# .github/workflows/reusable-build.yml
on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ inputs.python-version }}
```

调用可重用工作流：

```yaml
# .github/workflows/main.yml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      python-version: '3.9'
```

### 6. 安全最佳实践

```yaml
# 限制权限到最小必需
permissions:
  contents: read
  
# 验证第三方动作
- name: Verify action
  uses: actions/checkout@v4  # 使用固定版本
  
# 敏感操作使用环境保护
environment: production
```

### 7. 监控和通知

```yaml
- name: Notify on failure
  if: failure()
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Workflow failed',
        body: 'Workflow ${{ github.workflow }} failed'
      })
```

### 8. 文档和版本管理

- 在 `CLAUDE.md` 或 `README.md` 中记录工作流说明
- 使用语义化版本标签
- 为复杂工作流添加内联注释
- 定期更新动作版本

## 高级功能

### 1. 条件矩阵

```yaml
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        arch: x86_64
        platform: linux/amd64
      - os: ubuntu-latest  
        arch: aarch64
        platform: linux/arm64
    exclude:
      - os: windows-latest
        arch: aarch64
```

### 2. 动态矩阵

```yaml
jobs:
  generate-matrix:
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: echo "matrix={\"version\":[\"3.8\",\"3.9\"]}" >> $GITHUB_OUTPUT
        
  test:
    needs: generate-matrix
    strategy:
      matrix: ${{ fromJson(needs.generate-matrix.outputs.matrix) }}
```

### 3. 复合动作

创建自定义复合动作：

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Setup Python environment and install dependencies'
inputs:
  python-version:
    description: 'Python version'
    required: false
    default: '3.9'
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ inputs.python-version }}
    - run: pip install -r requirements.txt
      shell: bash
```

使用自定义动作：

```yaml
- name: Setup project
  uses: ./.github/actions/setup-project
  with:
    python-version: '3.10'
```

## 故障排查

### 1. 查看详细日志

```bash
# 查看失败的工作流日志
gh run view --log-failed

# 下载日志文件
gh run download [run-id]
```

### 2. 本地调试

使用 `act` 工具在本地运行 GitHub Actions：

```bash
# 安装 act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# 本地运行工作流
act push

# 运行特定任务
act -j build
```

### 3. 启用调试日志

在仓库设置中添加密钥：
- `ACTIONS_STEP_DEBUG`: `true`
- `ACTIONS_RUNNER_DEBUG`: `true`

### 4. 使用 tmate 进行远程调试

```yaml
- name: Setup tmate session
  if: failure()
  uses: mxschmitt/action-tmate@v3
```

## 总结

GitHub Actions 是一个强大的 CI/CD 平台，通过本教程你应该能够：

1. 理解 GitHub Actions 的基本概念和工作原理
2. 掌握工作流的配置语法和最佳实践
3. 了解本项目的具体工作流配置
4. 能够创建、修改和调试自己的工作流
5. 解决常见的工作流问题

继续探索 GitHub Actions 的高级功能，并根据项目需求优化你的 CI/CD 流程！

---

> 本教程基于本项目的实际配置编写，更多详细信息请参考 [GitHub Actions 官方文档](https://docs.github.com/en/actions)。