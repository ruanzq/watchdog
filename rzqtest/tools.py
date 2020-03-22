import datetime
import re
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import parse, request
import idna
from OpenSSL import SSL
import prettytable as pt

# 环境配置
G = {
    # 证书的有效期限
    "expire": 10000,

    # 是否发送邮件
    "isSend": False,

    # 是否向stdout打印工作结果
    "isPrint": False,

    # 是否打印原始数据
    "isR": False,

    # 是否反向选择输出结果
    "isV": False,

    # 是否检测证书
    "isCert": False,

    # 是否检测URL有效性
    "isUrl": False,

    # smtp服务器地址
    "smtpServer": None,

    # smtp服务器端口
    "smtpPort": None,

    # smtp帐号
    "account": None,

    # smtp密码
    "password": None,

    # 收信人列表
    "receivers": []
}

# url过滤器
r = re.compile(r'((?:https|http)://[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+/?)')


def getUrl(filename):
    try:
        urllist = []
        hander = open(filename, 'r', encoding='utf-8')
        for url in hander.readlines():
            url = url.strip().split('#')[0]
            if url == "":
                continue
            if r.search(url):
                urllist.append(url)
        return urllist
    except FileNotFoundError:
        print("{0} not found!".format(filename))
        exit(-1)
    except UnicodeDecodeError:
        print("{0} decode error".format(filename))
        exit(-1)
    except Exception as e:
        print("未知错误: {0}".format(e))
        exit(-1)


def test(func):
    """
    包装器 使用包装函数依次处理每个URL
    :param func:
    :return:
    """

    def wrapper(urllist):
        trueset = []
        falseset = []
        for url in urllist:
            result = func(url)
            if result[0]:
                trueset.append(result[1])
            else:
                falseset.append(result[1])
        return [trueset,falseset]

    return wrapper


@test
def verifyAddress(url):
    """
    检测URL的有效性
    :param url:待确认的url
    :return: 返回确认结果，元组格式，('url','result')
    """
    try:
        code = request.urlopen(url, timeout=5).getcode()
        if code < 400:
            result = [False,(url, code)]
        else:
            result = [True,(url, code)]
    except Exception as e:
        result = [True,(url, e)]
    return result


def _getCert(url):
    """
    根据一个URL获取证书
    :param url: 待获取证书对url
    :return: 返回获取到的证书
    """
    meta_url = parse.urlparse(url)
    sock_info = (meta_url.hostname, meta_url.port or 443)
    try:
        sock = socket.socket()
        sock.connect(sock_info)
        cxt = SSL.Context(SSL.SSLv23_METHOD)
        cxt.check_hostname = False
        cxt.verify_mode = SSL.VERIFY_NONE
        sock_ssl = SSL.Connection(cxt, sock)
        sock_ssl.set_tlsext_host_name(idna.encode(sock_info[0]))
        sock_ssl.set_connect_state()
        sock_ssl.do_handshake()
        cert = sock_ssl.get_peer_certificate()
        sock_ssl.close()
        sock.close()
    except Exception as e:
        cert = e
    return cert


@test
def verifyCert(url):
    """
    确认证书有效性
    :param url:根据url获取证书，并检测是否符合规则
    :return:检测的结果
    """
    cert = _getCert(url)
    if isinstance(cert, Exception):
        result = [True,(url, cert)]
    else:
        certTime = datetime.datetime.strptime(str(cert.get_notAfter()[: -1], encoding='utf-8'),
                                              '%Y%m%d%H%M%S') + datetime.timedelta(hours=8)
        TimeRemained = certTime - datetime.datetime.now()
        if TimeRemained.days > G['expire']:
            result = [False,(url,TimeRemained.days)]
        else:
            result = [True,(url, TimeRemained.days)]
    return result


def setMailConfig(args):
    """
    邮件发送配置
    :param args:命令行参数
    :return:None
    """
    if len(args) < 3:
        print("lost mail config")
        exit(-1)
    else:
        try:
            hand = open(args[2], "r", encoding="utf-8")
            for i in hand.readlines():
                i = i.strip().split('#')[0]
                if i == "":
                    continue
                elif i.startswith("server:"):
                    i = i.split(":")
                    G['smtpServer'] = i[1]
                    G['smtpPort'] = i[2]
                    G['account'] = i[3]
                    G['password'] = i[4]
                else:
                    G['receivers'].append(i)
            G['isSend'] = True
            print("mail config loaded")
        except Exception as c:
            print(c)
            exit(-1)


def send(content, subject):
    """
    发送一封以content作为正文的邮件
    :param content:邮件正文
    :param subject:邮件主题
    :return:None
    """
    con = smtplib.SMTP_SSL(G['smtpServer'], G['smtpPort'])
    con.login(G['account'], G['password'])
    text = MIMEText(content,'plain','utf-8')
    shell = MIMEMultipart()
    shell['Subject'] = subject
    shell['From'] = G['account']
    shell['to'] = ",".join(G['receivers'])
    shell.attach(text)
    con.sendmail(G['account'],G['receivers'], shell.as_string())
    con.close()
def makeRecords(record, col_1,col_2):
    """
    :param record:
    :param col_1:
    :param col_2:
    :return:
    """
    tb = pt.PrettyTable([col_1 , col_2])
    for i in record:
        addr = i[0]
        result = i[1]
        tb.add_row([addr, result])
    return tb


def setStat(args):
    """
    根据命令行参数设置程序状态
    :param args: 命令行参数
    :return: None
    """
    global G
    if len(args) < 3:
        printHelpExit()
    else:
        args = args[1:]
    switch = args[0]
    G['urlfile'] = args[1]
    isCert = re.search(r'c\d+', switch)
    isUrl = re.search(r'u', switch)
    isSend = re.search(r'e', switch)
    isPrint = re.search(r'p', switch)
    isR = re.search(r'r', switch)
    isV = re.search(r'v', switch)
    if not isCert and not isUrl:
        printHelpExit()
    if isSend:
        setMailConfig(args)
    if isCert:
        G['isCert'] = True
        G['expire'] = int(isCert.group()[1:])
    if isUrl:
        G['isUrl'] = True
    if isPrint:
        G['isPrint'] = True
    if isR:
        G['isR'] = True
    if isV:
        G['isV'] = True


def printHelpExit():
    """
    打印帮助信息并退出
    :return:None
    """
    print("""
Format:
    python -m rzqtest switch urlfile [emailconfig]

Switch:
    c[number] 启用证书检测和证书剩余时间上限，number不可省，如c200，会返回小于200天的站点信息
    u 启用url可访问性检测。
    p 将格式化结果打印在屏幕上。
    e 将格式化结果以邮件发送，必须指定emailconf文件的路径，可以配合选项v使用。
    r 将结果以python原生格式，输出到屏幕。
    v 反向选择结果，配合选项p，r，e使用。
emailconfig format:
    server:domain:port:account:password
    # 不以server:开头的行，均视为邮件接收者的一员。
    xxxxx@qq.com
    cccccc@gmail.com
""")
    exit(-1)
