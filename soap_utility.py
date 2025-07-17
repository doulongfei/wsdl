# soap_utility.py (最终方案：直接XML解析)

import os
import logging
import xml.etree.ElementTree as ET
from zeep import Client, Transport
from zeep.exceptions import Fault, TransportError, XMLSyntaxError

logger = logging.getLogger(__name__)

# -----------------
# I. SOAP 调用功能 (保持不变)
# -----------------
def call_soap_method(wsdl_source, method_name, *args, **kwargs):
    """使用zeep调用一个SOAP方法。"""
    try:
        client = Client(wsdl_source, transport=Transport(timeout=10, operation_timeout=60))
        service_method = getattr(client.service, method_name)
        result = service_method(*args, **kwargs)
        return result
    except KeyError:
        logger.error(f"方法 '{method_name}' 在WSDL中未找到。")
        return None
    except Fault as e:
        logger.error(f"调用方法 '{method_name}' 时发生SOAP Fault: {e.message} (Code: {e.code})")
        return None
    except Exception as e:
        logger.error(f"调用方法时发生未知错误: {e}", exc_info=True)
        return None

# -----------------
# II. WSDL 检查功能 (全新实现)
# -----------------
def list_soap_methods(wsdl_source):
    """使用zeep列出所有可用的SOAP方法名称。"""
    try:
        client = Client(wsdl_source, transport=Transport(timeout=10))
        # zeep在解析时已经完成了这项工作，这是它最可靠的用途之一
        return list(client.service._operations.keys())
    except Exception as e:
        logger.error(f"无法从 '{wsdl_source}' 加载或列出方法: {e}")
        return []

def get_method_signature(wsdl_source, method_name):
    """
    通过直接解析WSDL XML文件来构建方法的详细签名。
    这个方法是可靠的，因为它直接处理源数据，绕过了zeep内部对象的复杂性。
    """
    try:
        tree = ET.parse(wsdl_source)
        root = tree.getroot()

        # WSDL文件使用大量命名空间，这是解析的关键
        namespaces = {k: v for k, v in dict(root.attrib).items() if 'xmlns' in k}
        if not namespaces: # 如果根元素没有，就手动查找
            namespaces = {
                'soap': 'http://schemas.xmlsoap.org/wsdl/soap/',
                'wsdl': 'http://schemas.xmlsoap.org/wsdl/',
                's': 'http://www.w3.org/2001/XMLSchema',
                'tns': 'http://tempuri.org/' # 需要根据WSDL文件调整
            }

        # 1. 找到操作(operation)对应的输入和输出消息
        op_xpath = f".//wsdl:portType/wsdl:operation[@name='{method_name}']"
        operation = root.find(op_xpath, namespaces)
        if operation is None:
            logger.error(f"在WSDL的portType中找不到操作 '{method_name}'。")
            return None

        input_msg_name = operation.find('wsdl:input', namespaces).get('message').split(':')[-1]
        output_msg_name = operation.find('wsdl:output', namespaces).get('message').split(':')[-1]

        # 2. 根据消息名称，找到消息定义中的部分(part)
        input_part_xpath = f".//wsdl:message[@name='{input_msg_name}']/wsdl:part"
        output_part_xpath = f".//wsdl:message[@name='{output_msg_name}']/wsdl:part"
        input_part = root.find(input_part_xpath, namespaces)
        output_part = root.find(output_part_xpath, namespaces)

        # 3. 消息部分指向一个元素(element)，这个元素定义了具体的参数
        input_element_name = input_part.get('element').split(':')[-1]
        output_element_name = output_part.get('element').split(':')[-1]

        # 4. 在<types>里的<schema>中找到这个元素的定义，并提取其子元素作为参数
        input_params = []
        schema_element_xpath = f".//s:element[@name='{input_element_name}']/s:complexType/s:sequence/s:element"
        param_elements = root.findall(schema_element_xpath, namespaces)
        for param in param_elements:
            p_name = param.get('name')
            p_type = param.get('type').split(':')[-1]
            input_params.append(f"{p_name}: {p_type}")
        params_string = ", ".join(input_params)

        # 5. 同样的方法找到返回值的类型
        return_type_str = "None"
        # 返回值通常被包裹在一个名为 '...Result' 的元素中
        return_element_xpath = f".//s:element[@name='{output_element_name}']/s:complexType/s:sequence/s:element"
        return_element = root.find(return_element_xpath, namespaces)
        if return_element is not None:
            return_type_str = return_element.get('type').split(':')[-1]

        return f"{method_name}({params_string}) -> {return_type_str}"

    except ET.ParseError as e:
        logger.error(f"解析WSDL文件 '{wsdl_source}' 时出错: {e}")
        return None
    except Exception as e:
        logger.error(f"解析方法 '{method_name}' 签名时发生意外错误: {e}", exc_info=True)
        return None
