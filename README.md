# rzqtest

检测url的可访问性和证书剩余有效期，并输出不符合条件的结果。

```
python -m rzqtest switch urlfile emailconf
```



switch参数说明

| 参数      | 说明                                                         |
| :-------- | ------------------------------------------------------------ |
| c[number] | 启用证书检测和证书剩余时间上限，number不可省，如c200，会返回小于200天的站点信息。 |
| u         | 启用url可访问性检测。                                        |
| p         | 将格式化结果打印在屏幕上。                                   |
| e         | 将结果以邮件发送，必须指定emailconf文件的路径。              |
| r         | 将结果以python原生格式，输出到屏幕                           |



##### urlfile文件格式

```
# 注释
https://www.baidu.com
```



##### emailconf文件格式

```
server:domain:port:account:password
# 不以server:开头的行，均视为邮件接收者的一员。
xxxxx@qq.com
cccccc@gmail.com

```







