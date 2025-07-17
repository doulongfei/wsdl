# ==============================================================================
# cli_caller.py (最终完整版)
#
# 一个通用的SOAP客户端命令行工具。
#
# 功能:
# 1. 列出 (list) WSDL中所有可用的SOAP方法。
# 2. 检查 (inspect) 特定方法的签名（参数）。
# 3. 调用 (call) 特定方法，支持位置参数和关键字参数。
# 4. 调试模式 (--debug) 可输出详细的执行日志。
# 5. 智能参数类型转换 (str -> int/float)。
# 6. 支持从文件读取参数内容 (使用 'file:' 前缀)。
# ==============================================================================

import argparse
import logging
import os

from soap_utility import (
    list_soap_methods,
    get_method_signature,
    call_soap_method
)


def auto_convert_type(value_str):
    """
    智能转换参数值的类型。
    1. 如果值以 "file:" 开头，则读取文件内容作为字符串。
    2. 尝试将值转换为整数。
    3. 如果失败，尝试将值转换为浮点数。
    4. 如果全部失败，则保持为原始字符串。
    """
    # 1. 检查是否为文件协议
    if isinstance(value_str, str) and value_str.startswith('file:'):
        filepath = value_str[5:]  # 去掉 "file:" 前缀
        logging.info(f"检测到文件参数，尝试读取文件: {filepath}")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    logging.info(f"文件读取成功，内容长度: {len(content)}")
                    return content
            except Exception as e:
                logging.error(f"读取文件 '{filepath}' 时出错: {e}")
                return value_str  # 读取失败，返回原始值以供调试
        else:
            logging.warning(f"指定的文件不存在: {filepath}")
            return value_str  # 文件不存在，返回原始值

    # 2. 尝试转换为整数
    try:
        return int(value_str)
    except (ValueError, TypeError):
        # 3. 尝试转换为浮点数
        try:
            return float(value_str)
        except (ValueError, TypeError):
            # 4. 保持为原始字符串
            return value_str

def main():
    # --- 1. 设置命令行参数解析器 ---
    parser = argparse.ArgumentParser(
        description="一个通用的SOAP客户端命令行工具。采用 '源 -> 命令 -> 参数' 的结构。",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="启用调试模式，输出详细的执行过程日志。"
    )
    parser.add_argument("wsdl_source", help="WSDL文件的路径或URL。")

    subparsers = parser.add_subparsers(dest="command", required=True, help="可执行的命令")

    subparsers.add_parser("list", help="列出所有可用的SOAP方法。")

    parser_inspect = subparsers.add_parser("inspect", help="检查并显示指定方法的签名。")
    parser_inspect.add_argument("method_name", help="要检查的方法名。")

    parser_call = subparsers.add_parser("call", help="调用指定的SOAP方法。")
    parser_call.add_argument("method_name", help="要调用的方法名。")
    parser_call.add_argument(
        "method_args",
        nargs='*',
        help="""传递给方法的参数。支持格式:
  - 位置参数: value1 value2 ...
  - 关键字参数: key=value3 ...
  - 文件参数: key=file:/path/to/data.xml"""
    )

    args = parser.parse_args()

    # --- 2. 根据 --debug 参数配置日志系统 ---
    log_level = logging.INFO if args.debug else logging.WARNING
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=log_format)

    # --- 3. 根据命令执行相应操作 ---
    try:
        if args.command == "list":
            logging.info(f"开始执行 'list' 命令，WSDL源: {args.wsdl_source}")
            methods_list = list_soap_methods(args.wsdl_source)
            if methods_list:
                print("\n--- ✅ 可用方法 ---")
                for method in methods_list:
                    print(f"- {method}")
            else:
                print("\n--- ❌ 未找到任何方法或加载WSDL时出错 ---")
            logging.info("'list' 命令执行完毕。")

        elif args.command == "inspect":
            logging.info(f"开始执行 'inspect' 命令，检查方法: '{args.method_name}'")
            signature = get_method_signature(args.wsdl_source, args.method_name)
            if signature:
                print("\n--- ✅ 方法签名 ---")
                print(signature)
            else:
                print(f"\n--- ❌ 无法获取 '{args.method_name}' 的签名 ---")
            logging.info("'inspect' 命令执行完毕。")

        elif args.command == "call":
            logging.info(f"开始执行 'call' 命令，调用方法: '{args.method_name}'")

            # 将 `method_args` 分割为位置参数和关键字参数
            pos_args_raw = [arg for arg in args.method_args if '=' not in arg]
            kw_args_raw = dict(arg.split('=', 1) for arg in args.method_args if '=' in arg)

            # 使用 auto_convert_type 函数统一处理所有参数
            processed_pos_args = [auto_convert_type(arg) for arg in pos_args_raw]
            processed_kw_args = {key: auto_convert_type(value) for key, value in kw_args_raw.items()}

            logging.info(f"处理后参数: 位置参数={processed_pos_args}, 关键字参数={processed_kw_args}")

            # 调用SOAP方法
            logging.info("正在发送SOAP请求...")
            result = call_soap_method(args.wsdl_source, args.method_name, *processed_pos_args, **processed_kw_args)
            logging.info("SOAP响应已收到。")

            # 输出结果
            if result is not None:
                print(result)
            else:
                # 区分是调用失败还是正常无返回
                logging.info("SOAP方法调用成功，但没有返回内容。")
            logging.info("'call' 命令执行完毕。")

    except Exception as e:
        # 捕获未知错误，提供用户友好的提示
        logging.error(f"执行过程中发生意外错误: {e}", exc_info=args.debug)
        print(f"\n--- ❌ 操作失败 ---")
        print(f"错误: {e}")
        if not args.debug:
            print("提示: 使用 -d 或 --debug 选项可以查看更详细的错误信息。")


if __name__ == "__main__":
    main()
