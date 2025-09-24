
import re


def is_dangerous(username):
    # 定义潜在危险的模式列表
    danger_patterns = [
        r"script",              # 检测是否包含 <script> 标签或者其他JavaScript相关代码
        r"drop\s+table",        # SQL注入，尝试删除数据库表
        r"select\s+.*\s+from",  # SQL注入，尝试执行查询操作
        r"admin",               # 特定关键词，例如 "admin"，可能用于非法访问
        r"[;\"\'\(\)]"          # 特殊字符，可能用于SQL注入或代码注入
    ]

    for pattern in danger_patterns:    # 检查每一个模式
        if re.search(pattern, username, re.IGNORECASE):
            return True

    return False      # 如果没有发现危险模式，返回False



def is_email_valid(email):
    # 电子邮件地址的正则表达式
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # 使用re.match检查电子邮件地址是否符合模式
    if re.match(pattern, email):
        return True
    else:
        return False


def email_check(email):
    if is_email_valid(email):
        if is_dangerous(email):
            return (False, 'The email address contains dangerous characters')
        else:
            return (True,'no_error')
    else:
        return (False,'Please enter the correct email format')


