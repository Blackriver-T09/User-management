import re



def is_username_dangerous(username):
    # 定义潜在危险的模式列表
    danger_patterns = [
        r"script",  # 检测是否包含 <script> 标签或者其他JavaScript相关代码
        r"drop\s+table",  # SQL注入，尝试删除数据库表
        r"select\s+.*\s+from",  # SQL注入，尝试执行查询操作
        r"admin",  # 特定关键词，例如 "admin"，可能用于非法访问
        r"[;\"\'\(\)]"  # 特殊字符，可能用于SQL注入或代码注入
    ]

    for pattern in danger_patterns:    # 检查每一个模式
        if re.search(pattern, username, re.IGNORECASE):
            return True

    return False      # 如果没有发现危险模式，返回False



def username_check(username):
    
    # 检查电子邮件格式
    if len(username)<2:
        return (False,'The username must be no less than 2 characters')
    else:
        if is_username_dangerous(username):
            return (False   , 'The username contains dangerous characters')
        else:
            return (True, 'no error')
        


if __name__ =="__main__":
    print(username_check('1'))
    print(username_check('hhah<scripts>'))
    print(username_check('12dsa'))


