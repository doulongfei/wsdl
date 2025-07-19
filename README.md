# SOAP Client Tool

This repository contains a SOAP client tool with the following key components:
1. `cli_caller.py`: The main CLI interface for interacting with SOAP services.
2. `soap_utility.py`: Core SOAP functionality using the `zeep` library.
3. WSDL files (`calculator.wsdl`, `test.wsdl`): Example WSDL files for testing.

## Key Commands

- **Run the CLI tool**:
  ```bash
  python cli_caller.py <WSDL_SOURCE> <COMMAND> [ARGS]
  ```
  Example commands:
  - List methods: `python cli_caller.py test.wsdl list`
  - Inspect method: `python cli_caller.py test.wsdl inspect <METHOD_NAME>`
  - Call method: `python cli_caller.py test.wsdl call <METHOD_NAME> [ARGS]`

- **Debug mode**: Add `-d` flag for detailed logging.

## Architecture

- The CLI (`cli_caller.py`) handles user input and delegates to `soap_utility.py`.
- `soap_utility.py` uses the `zeep` library for SOAP operations and direct XML parsing for method signatures.
- Supports both file-based and URL-based WSDL sources.
- Implements smart parameter type conversion (string to int/float/file content).