from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
import base64

def to_encode(nickname,email):  
    nickname_bytes = nickname.encode('utf-8')          # 使用UTF-8编码将昵称转换为字节数组
    base64_encoded_nickname = base64.b64encode(nickname_bytes).decode('utf-8')   # 对字节数组进行base64编码
    formatted_nickname = f'=?utf-8?B?{base64_encoded_nickname}?='   # 根据编码后的昵称和邮箱地址构建"From"标头
    from_header = f'"{formatted_nickname}" <{email}>'
    return from_header
#定义这个函数是因为message['From']和message['To']对格式有严格的要求。尤其是中文(非ASCLL编码)字符需要进一步编码
#然而这个编码函数对ASCLL码字符同样适用，所以直接全面采用了

def alert(receivers,message):
    sender = '2812104715@qq.com'              # 发件人邮箱
    # receivers = ['jiayang.23@intl.zju.edu.cn']         # 接收人邮箱，可以是多个，用逗号分隔
    key='vvkoihawmhwpdeih'                    # QQ邮箱授权码，需要从“账号安全”设置里获取
    
    nickname1="anonymous"
    nickname2='anonymous'

    message = MIMEText(message, 'plain', 'utf-8')     #plain表示正文将包含纯文本信息，没有格式或样式。
    message['From'] = to_encode(nickname1,sender)         #这里一定要注意格式，nickname和地址间有空格
    message['To'] =  to_encode(nickname2,receivers)
    message['Subject'] = Header('警报邮件', 'utf-8')     #设置了邮件的主题
    
    smtper = SMTP('smtp.qq.com')             ## 使用 QQ 邮箱的 SMTP 服务器
    smtper.login(sender,key )
    smtper.sendmail(sender, receivers, message.as_string())   #将邮件内容以字符串形式发送
    print('email has been sent!')


if __name__=="__main__":

    conversation_history = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                             {'role': 'user', 'content': 'hello'}, 
                             {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}, 
                             {'role': 'user', 'content': 'i love you'}, 
                             {'role': 'assistant', 'content': "That's kind of you! I'm here to help you with any questions or tasks you have. How can I assist you today?"}]
    message=''
    for i in conversation_history:
        role=i['role']
        content=i['content']
        inf=role+':'+content
        message+=f'\n{inf}'
    alert('jiayang.23@intl.zju.edu.cn',message)
    print(message)







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
