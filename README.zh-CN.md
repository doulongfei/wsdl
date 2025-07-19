# SOAP 客户端工具

该仓库包含一个 SOAP 客户端工具，其主要组件如下：
1. `cli_caller.py`: 用于与 SOAP 服务交互的主 CLI 接口。
2. `soap_utility.py`: 使用 `zeep` 库实现核心 SOAP 功能。
3. WSDL 文件 (`calculator.wsdl`, `test.wsdl`): 用于测试的 WSDL 示例文件。

## 主要命令

- **运行 CLI 工具**:
  ```bash
  python cli_caller.py <WSDL_SOURCE> <COMMAND> [ARGS]
  ```
  示例命令：
  - 列出方法: `python cli_caller.py test.wsdl list`
  - 检查方法: `python cli_caller.py test.wsdl inspect <METHOD_NAME>`
  - 调用方法: `python cli_caller.py test.wsdl call <METHOD_NAME> [ARGS]`

- **调试模式**: 添加 `-d` 标志以获取详细日志。

## 架构

- CLI (`cli_caller.py`) 处理用户输入并委托给 `soap_utility.py`。
- `soap_utility.py` 使用 `zeep` 库进行 SOAP 操作，并直接解析 XML 以获取方法签名。
- 支持基于文件和基于 URL 的 WSDL 源。
- 实现智能参数类型转换（字符串到整数/浮点数/文件内容）。