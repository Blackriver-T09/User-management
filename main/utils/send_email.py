from smtplib import SMTP,SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
import base64
from threading import Thread
import smtplib
from email.utils import formataddr


# 用于生成当前时间戳
from datetime import datetime, timedelta, timezone
def now_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def to_encode(nickname,email):  
    nickname_bytes = nickname.encode('utf-8')          # 使用UTF-8编码将昵称转换为字节数组
    base64_encoded_nickname = base64.b64encode(nickname_bytes).decode('utf-8')   # 对字节数组进行base64编码
    formatted_nickname = f'=?utf-8?B?{base64_encoded_nickname}?='   # 根据编码后的昵称和邮箱地址构建"From"标头
    from_header = f'"{formatted_nickname}" <{email}>'
    return from_header
#定义这个函数是因为message['From']和message['To']对格式有严格的要求。尤其是中文(非ASCLL编码)字符需要进一步编码
#然而这个编码函数对ASCLL码字符同样适用，所以直接全面采用了


# def send_email_async(sender, receivers,msg ,key):

#     try:
#         smtper = SMTP('smtp-mail.outlook.com')
#         smtper.starttls()
#         smtper.login(sender, key)
#         smtper.sendmail(sender, receivers, msg.as_string())
#         smtper.quit()
#         print(f'{now_time()}: email has been sent!')

#     except Exception as e:
#         print(f'{now_time()}: Failed to send mail: {e}')

# def send_email(receivers, message, mode ):
#     sender = 'svc-rshub_auto_reply@intl.zju.edu.cn'
#     key = 'this_is_key'
#     nickname1 = "RShub"
#     nickname2 = 'Receiver'
#     subject = 'Change Password' if mode == 1 else 'Successful Registration'
    
#     msg = MIMEText(message, 'plain', 'utf-8')
#     msg['From'] = to_encode(nickname1, sender)
#     msg['To'] = to_encode(nickname2, receivers)
#     msg['Subject'] = Header(subject, 'utf-8')
    
#     # 创建线程来异步发送邮件
#     thr = Thread(target=send_email_async, args=[sender, receivers,msg,key])
#     thr.start()



# # 开发使用的QQ邮箱
# def send_email(receivers, message, mode ):
#     sender = 'svc-rshub_auto_reply@intl.zju.edu.cn'
#     key ='***'
#     nickname1 = "RShub"
#     nickname2 = 'Receiver'
#     subject = 'Change Password' if mode == 1 else 'Successful Registration'

#     message = MIMEText(message, 'plain', 'utf-8')     #plain表示正文将包含纯文本信息，没有格式或样式。
#     message['From'] = to_encode(nickname1,sender)         #这里一定要注意格式，nickname和地址间有空格
#     message['To'] =  to_encode(nickname2,receivers)
#     message['Subject'] = Header(subject, 'utf-8')     #设置了邮件的主题
    
#     try:
#         smtper = SMTP('smtp-mail.outlook.com')
#         smtper.ehlo()
#         smtper.starttls()
#         smtper.login(sender, key)
#         smtper.sendmail(sender, receivers, message.as_string())
#         print(f'{now_time()}: email has been sent!')
#         smtper.quit()
        
#     except Exception as e:
#         print(f'{now_time()}: Failed to send mail: {e}')
def send_email(receivers, message, mode ):
    sender = '2812104715@qq.com'  # 发件人邮箱账号
    password = 'hldqnwrxaktkddcb'   # 授权码
    nickname1 = "RShub"
    nickname2 = 'Receiver'
    subject = 'Change Password' if mode == 1 else 'Successful Registration'

    message = MIMEText(message, 'plain', 'utf-8')     #plain表示正文将包含纯文本信息，没有格式或样式。
    message['From'] = formataddr((nickname1,sender))         #这里一定要注意格式，nickname和地址间有空格
    message['To'] =  formataddr((nickname2,receivers))
    message['Subject'] = Header(subject, 'utf-8')     #设置了邮件的主题
    
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)              # 连接SMTP服务器
        server.login(sender, password)
        server.sendmail(sender, receivers, message.as_string())
        print(f'{now_time()}: email has been sent!')
        server.quit()
        
    except Exception as e:
        print(f'{now_time()}: Failed to send mail: {e}')









if __name__=="__main__":
    message='You have been successfully registered'
    send_email('jiayang.23@intl.zju.edu.cn',message,1)
    # print(message)







# # ————————————————————————————短信——————————————————————————————————
# #python3
# #接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# #账户注册：请通过该地址开通账户https://user.ihuyi.com/new/register.html
# #注意事项：
# #（1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# #（2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
# #（3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

# import urllib.parse
# import urllib.request

# #接口地址
# url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'

# #定义请求的数据
# values = {
#     'account':'C19041438',
#     'password':'aba462e2d3cf544bfc1769d38788e177',
#     'mobile':'17306873582',
#     'content':'您的验证码是：7835。请不要把验证码泄露给其他人。',
#     'format':'json',
# }

# #将数据进行编码
# data = urllib.parse.urlencode(values).encode(encoding='UTF8')

# #发起请求
# req = urllib.request.Request(url, data)
# response = urllib.request.urlopen(req)
# res = response.read()

# #打印结果
# print(res.decode("utf8"))
