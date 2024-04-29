import re

def password_check(password):
    """
    返回:
    tuple: (bool, str) 布尔值表示密码是否有效，字符串给出不符合的原因。
    """
    # 长度检查
    if not (8 <= len(password) <= 26):
        return (False, "密码需要8-26位，至少包含大小写字母，数字和一个特殊字符")

    # 包含小写字母
    if not re.search("[a-z]", password):
        return (False, "密码需要8-26位，至少包含大小写字母，数字和一个特殊字符")

    # 包含大写字母
    if not re.search("[A-Z]", password):
        return (False, "密码需要8-26位，至少包含大小写字母，数字和一个特殊字符")

    # 包含数字
    if not re.search("[0-9]", password):
        return (False, "密码需要8-26位，至少包含大小写字母，数字和一个特殊字符")

    # 包含特殊字符
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return (False, "密码需要8-26位，至少包含大小写字母，数字和一个特殊字符")

    return (True,'no error')



 
 

 
 
 
 
 
 