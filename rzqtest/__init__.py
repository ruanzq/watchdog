import sys
from rzqtest import tools
tools.setStat(sys.argv)
urls = tools.getUrl(tools.G['urlfile'])
result_cert = []
result_addr = []
if tools.G['isCert'] :
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
        tools.G['isR'] and print(reuslt)
if tools.G['isSend']:
    if ['isV']:
        result = tools.makeRecords(result_addr[1],"Access","HTTP响应码").get_string() + tools.makeRecords(result_cert[1],"Cert","剩余日期天数").get_string()
    else:
        result = tools.makeRecords(result_addr[0],"Access","HTTP响应码").get_string() + tools.makeRecords(result_cert[0],"Cert","剩余日期天数").get_string()
    tools.send(result,"test")
