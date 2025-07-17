# cli_caller.py (最终版 - 含debug功能)
import argparse
import logging
from soap_utility import (
    list_soap_methods,
    get_method_signature,
    call_soap_method
)

def main():
    # --- 1. 设置解析器 ---
    parser = argparse.ArgumentParser(
        description="一个通用的SOAP客户端命令行工具。采用 '源 -> 命令 -> 参数' 的结构。",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # 全局可选参数，必须在位置参数之前定义
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="启用调试模式，输出详细的执行过程日志。"
    )

    # 位置参数
    parser.add_argument("wsdl_source", help="WSDL文件的路径或URL。")

    # 子命令解析器
    subparsers = parser.add_subparsers(dest="command", required=True, help="可执行的命令")

    # 'list' 命令
    subparsers.add_parser("list", help="列出所有可用的SOAP方法。")

    # 'inspect' 命令
    parser_inspect = subparsers.add_parser("inspect", help="检查并显示指定方法的签名。")
    parser_inspect.add_argument("method_name", help="要检查的方法名。")

    # 'call' 命令
    parser_call = subparsers.add_parser("call", help="调用指定的SOAP方法。")
    parser_call.add_argument("method_name", help="要调用的方法名。")
    parser_call.add_argument(
        "method_args",
        nargs='*',
        help="传递给方法的参数。格式: value1 value2 key=value3 ..."
    )

    args = parser.parse_args()

    # --- 2. 根据 --debug 参数配置日志系统 ---
    # 如果开启debug，日志级别设为INFO，可以看到所有执行步骤
    # 如果关闭debug，日志级别设为WARNING，所有INFO级别的日志都将被忽略
    log_level = logging.INFO if args.debug else logging.WARNING
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=log_format)


    # --- 3. 根据命令执行操作 ---

    if args.command == "list":
        logging.info(f"开始执行 'list' 命令，WSDL源: {args.wsdl_source}")
        methods_list = list_soap_methods(args.wsdl_source)
        if methods_list:
            # “结果”总是使用 print 输出
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

        # 参数处理
        pos_args = [arg for arg in args.method_args if '=' not in arg]
        kw_args = dict(arg.split('=', 1) for arg in args.method_args if '=' in arg)
        logging.info(f"原始参数: 位置参数={pos_args}, 关键字参数={kw_args}")

        processed_pos_args = []
        for arg in pos_args:
            try:
                processed_pos_args.append(int(arg))
            except ValueError:
                try:
                    processed_pos_args.append(float(arg))
                except ValueError:
                    processed_pos_args.append(arg)
        logging.info(f"处理后参数: 位置参数={processed_pos_args}, 关键字参数={kw_args}")

        # 方法调用
        logging.info("正在通过SOAP请求...")
        result = call_soap_method(args.wsdl_source, args.method_name, *processed_pos_args, **kw_args)
        logging.info("SOAP响应已收到。")

        # 结果输出
        # print("\n--- 响应结果 ---")
        if result is not None:
            print(result)
        else:
            print("调用失败或没有返回结果。")
        logging.info("'call' 命令执行完毕。")


if __name__ == "__main__":
    main()
