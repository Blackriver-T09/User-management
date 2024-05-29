import sys
import os
# 此处os.path.dirname()可以获得上一级目录，也就是当前文件或文件夹的父目录
# 将目录加入到sys.path即可生效，可以帮助python定位到文件（注：这种方法仅在运行时生效，不会对环境造成污染）
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import email_check,password_check,username_check,  hash_encipher, decryptor_check,alert,path_generate



# # 用户名测试
# result,error_message=username_check('h')
# print(result,error_message)
# result,error_message=username_check('hhaha<script>')
# print(result,error_message)
# result,error_message=username_check('hfddsa')
# print(result,error_message)



# # 邮件格式测试
# result,error_message=email_check('123')
# print(result,error_message)
# result,error_message=email_check('123@qq.com<script>')
# print(result,error_message)
# result,error_message=email_check('123@qq.com')
# print(result,error_message)
# result,error_message=email_check('123@intl.zju.edu.cn')
# print(result,error_message)



# # 密码安全性测试
# result,error_message=password_check('123')
# print(result,error_message)
# result,error_message=password_check('123221Wsddd!')
# print(result,error_message)



# # 密码加密测试  和  解密校验器测试
# password='b9!Sta88kVvCCR7'
# password_hashed=hash_encipher(password)
# # password_hashed='$2b$12$Fx31Lrq1cAr.6bqJdvTre.BYl0XsaQhjWGQhCBz/8ned56FOUpH1C'
# print(password_hashed)
# print('密码是否相等：',decryptor_check(password,password_hashed))



# # # 报警测试
# # alert('jiayang.23@intl.zju.edu.cn',"哈哈哈哈哈哈哈")
# for i in range(5):
#     alert('yang.23@intl.zju.edu.cn',"哈哈哈哈哈哈哈")


# # token 生成测试
# token=token_generate()
# print(token)



