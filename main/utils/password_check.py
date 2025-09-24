import re

def password_check(password):
    """
    返回:
    tuple: (bool, str) 布尔值表示密码是否有效，字符串给出不符合的原因。
    """
    # 长度检查
    if not (8 <= len(password) <= 26):
        return (False, "The password needs to be 8-26 digits, containing at least uppercase and lowercase letters, numbers, and one special character")

    # 包含小写字母
    if not re.search("[a-z]", password):
        return (False, "The password needs to be 8-26 digits, containing at least uppercase and lowercase letters, numbers, and one special character")

    # 包含大写字母
    if not re.search("[A-Z]", password):
        return (False, "The password needs to be 8-26 digits, containing at least uppercase and lowercase letters, numbers, and one special character")

    # 包含数字
    if not re.search("[0-9]", password):
        return (False, "The password needs to be 8-26 digits, containing at least uppercase and lowercase letters, numbers, and one special character")

    # 包含特殊字符
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return (False, "The password needs to be 8-26 digits, containing at least uppercase and lowercase letters, numbers, and one special character")

    return (True,'no error')



 
 

 
 
 
 
 
 