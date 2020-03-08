import sys
from rzqtest import tools
tools.setStat(sys.argv)
urls = tools.getUrl(tools.G['urlfile'])
result_cert = []
result_addr = []
if tools.G['isCert'] :
    result_cert = tools.verifyCert(urls)
    result_cert_format = tools.makeRecords(result_cert, "Cert","剩余天数")
    if tools.G['isPrint']:
        print(result_cert_format)
    if tools.G['isR']:
        print(result_cert)
if tools.G['isUrl']:
    result_addr = tools.verifyAddress(urls)
    result_addr_format = tools.makeRecords(result_addr, "Access","HTTP响应码")
    if tools.G['isPrint']:
        print(result_addr_format)
    if tools.G['isR']:
        print(result_addr)
if tools. G['isSend']:
    content = result_cert_format.get_string() + result_addr_format.get_string()
    if content == []:
        content = "everything is fine"
    print(type(content))
    #tools.send("".join(content),"测试结果")