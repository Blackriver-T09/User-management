
import bcrypt

def hash_encipher(password):
    """

    返回:
    str: 加密后的密码散列。
    """
    # 将密码转化为字节
    password_bytes = password.encode('utf-8')
    
    salt = bcrypt.gensalt()      # 生成 salt，然后使用 salt 加密密码
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password.decode('utf-8')

if __name__=='__main__':
    print(len(hash_encipher('12344')))
