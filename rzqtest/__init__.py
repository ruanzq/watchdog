import sys
from rzqtest import tools
tools.setStat(sys.argv)
urls = tools.getUrl(tools.G['urlfile'])
result_cert = []
result_addr = []
addr_format_head = "Access"
addr_format_result = "HTTP响应码"
cert_format_head = "Cert"
cert_format_result = "剩余日期天数"
if tools.G['isCert']:
    result_cert = tools.verifyCert(urls)
    result = []
    if tools.G['isPrint'] or tools.G['isR']:
        result = result_cert[0]
        if tools.G['isV']:
            result = result_cert[1]
        tools.G['isPrint'] and print(tools.makeRecords(result,"Cert","剩余天数"))
        tools.G['isR'] and print(result)
if tools.G['isUrl']:
    result_addr = tools.verifyAddress(urls)
    result = []
    if tools.G['isPrint'] or tools.G['isR']:
        result = result_addr[0]
        if tools.G['isV']:
            result = result_addr[1]
        tools.G['isPrint'] and print(tools.makeRecords(result,"Access","HTTP响应码"))
        tools.G['isR'] and print(result)
if tools.G['isSend']:
    result = ''
    if tools.G['isUrl']:    
        if tools.G['isV']:
            result += tools.makeRecords(result_addr[1],addr_format_head,addr_format_result).get_string() + '\n'
        else:
            result += tools.makeRecords(result_addr[0],addr_format_head,addr_format_result).get_string() + '\n'
    if tools.G['isCert']:
        if tools.G['isV']:
            result += tools.makeRecords(result_cert[1],cert_format_head,cert_format_result).get_string() + '\n'
        else:
            result += tools.makeRecords(result_cert[0],cert_format_head,cert_format_result).get_string() + '\n'
    tools.send(result,"test")
