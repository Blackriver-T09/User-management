import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from datetime import datetime, timedelta





# 加密函数（使用 URL 安全的 Base64 编码）
def encrypt_time(time_string: str, key: bytes, iv: bytes) -> str:
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(time_string.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # 使用 URL 安全的 Base64 编码 ,  这样就不会出现 / 等特殊字符
    return base64.urlsafe_b64encode(iv + ciphertext).decode('utf-8')



# 解密函数（使用 URL 安全的 Base64 解码）
def decrypt_time(token: str, key: bytes) -> str:
    encrypted_data = base64.urlsafe_b64decode(token)

    iv = encrypted_data[:16]  # 提取前16字节作为 IV
    actual_ciphertext = encrypted_data[16:]  # 剩余部分是密文

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(actual_ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode()



# 验证时间差异是否有效 （默认为1分钟）
def is_token_valid(encrypted_time: str, key: bytes, mins=1) -> bool:
    # 解密收到的时间字符串
    decrypted_time_str = decrypt_time(encrypted_time, key)
    decrypted_time = datetime.strptime(decrypted_time_str, "%Y-%m-%d %H:%M:%S")
    
    # 获取当前时间
    current_time = datetime.now()

    # 计算时间差距
    time_difference = abs(current_time - decrypted_time)

    # 检查差异是否在1分钟内
    return time_difference <= timedelta(minutes=mins)

# 获取当前时间并加密
def get_encrypted_current_time(key: bytes, iv: bytes) -> str:
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return encrypt_time(current_time_str, key, iv)
