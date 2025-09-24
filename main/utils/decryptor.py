import bcrypt

def decryptor_check(password, hashed_password):

    # 将输入密码转换为字节
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    # 使用 bcrypt 的检查方法来验证密码
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


