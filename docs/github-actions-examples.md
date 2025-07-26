# GitHub Actions 工作流示例

本目录包含可复用的 GitHub Actions 工作流模板和示例。

## 🚀 快速开始模板

### 1. Python 项目 CI/CD 模板

创建 `.github/workflows/python-ci.yml`：

```yaml
name: Python CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Test with pytest
      run: |
        pytest --cov=./ --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install build dependencies
      run: |
        pip install pyinstaller
        pip install -r requirements.txt
    
    - name: Build executable
      run: |
        pyinstaller --onefile main.py
    
    - name: Upload to release
      uses: softprops/action-gh-release@v2
      with:
        files: dist/*
```

### 2. 多平台构建模板

创建 `.github/workflows/multi-platform-build.yml`：

```yaml
name: Multi-Platform Build

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            platform: linux
            arch: amd64
          - os: ubuntu-latest
            platform: linux
            arch: arm64
          - os: windows-latest
            platform: windows
            arch: amd64
          - os: macos-latest
            platform: darwin
            arch: amd64

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up QEMU (for ARM builds)
      if: matrix.arch == 'arm64'
      uses: docker/setup-qemu-action@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install pyinstaller
        pip install -r requirements.txt
    
    - name: Build for ${{ matrix.platform }}-${{ matrix.arch }}
      run: |
        pyinstaller --onefile --name=myapp-${{ matrix.platform }}-${{ matrix.arch }} main.py
    
    - name: Upload release assets
      uses: softprops/action-gh-release@v2
      with:
        files: dist/*
```

### 3. Docker 构建和发布模板

创建 `.github/workflows/docker-build.yml`：

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### 4. 自动化测试矩阵模板

创建 `.github/workflows/comprehensive-test.yml`：

```yaml
name: Comprehensive Testing

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, 3.10, 3.11]
        exclude:
          - os: macos-latest
            python-version: 3.8

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-xdist

    - name: Run tests
      run: |
        pytest -n auto --tb=short

    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: test-results-${{ matrix.os }}-${{ matrix.python-version }}
        path: test-results/
```

## 🔧 常用组件模板

### 缓存配置

```yaml
# Python 依赖缓存
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# Node.js 依赖缓存
- name: Cache Node modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 安全扫描

```yaml
# 依赖安全扫描
- name: Run security scan
  uses: pypa/gh-action-pip-audit@v1.0.8
  with:
    inputs: requirements.txt

# 代码安全扫描
- name: Run CodeQL Analysis
  uses: github/codeql-action/analyze@v2
  with:
    languages: python
```

### 通知配置

```yaml
# Slack 通知
- name: Slack Notification
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}

# 邮件通知
- name: Send mail
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.MAIL_USERNAME }}
    password: ${{ secrets.MAIL_PASSWORD }}
    subject: Build failed
    body: Build failed on ${{ github.ref }}
    to: admin@example.com
```

## 📚 最佳实践

### 1. 工作流组织

```
.github/
└── workflows/
    ├── ci.yml              # 持续集成
    ├── cd.yml              # 持续部署
    ├── security.yml        # 安全扫描
    ├── dependencies.yml    # 依赖更新
    └── cleanup.yml         # 清理任务
```

### 2. 环境变量管理

```yaml
env:
  # 全局环境变量
  PYTHON_VERSION: 3.9
  NODE_VERSION: 16

jobs:
  build:
    env:
      # 任务级环境变量
      BUILD_ENV: production
    steps:
      - name: Deploy
        env:
          # 步骤级环境变量
          API_KEY: ${{ secrets.API_KEY }}
        run: echo "Deploying..."
```

### 3. 条件执行

```yaml
# 基于分支条件
- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  run: ./deploy-staging.sh

# 基于事件类型条件
- name: Deploy to production
  if: github.event_name == 'release'
  run: ./deploy-production.sh

# 基于文件变更条件
- name: Check for changes
  id: changes
  uses: dorny/paths-filter@v2
  with:
    filters: |
      src:
        - 'src/**'
      docs:
        - 'docs/**'

- name: Build if source changed
  if: steps.changes.outputs.src == 'true'
  run: npm run build
```

### 4. 错误处理

```yaml
- name: Build with retry
  uses: nick-invision/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: npm run build

- name: Cleanup on failure
  if: failure()
  run: |
    echo "Build failed, cleaning up..."
    rm -rf build/
```

## 🎯 使用建议

1. **从简单开始**：先实现基本的 CI，再逐步添加功能
2. **使用矩阵测试**：确保跨平台兼容性
3. **合理使用缓存**：减少构建时间
4. **安全第一**：正确管理密钥和权限
5. **监控和通知**：及时了解构建状态
6. **文档化**：为复杂工作流添加说明

## 📖 延伸阅读

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [Action Marketplace](https://github.com/marketplace?type=actions)

---

💡 **提示**：这些模板可以根据项目需求进行修改和组合使用。