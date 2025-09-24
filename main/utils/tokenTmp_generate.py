# 30位token生成器
import random
def tokenTmp_generate():
    token=''
    charaters='1234567890qwertyuiopasdfghjklzxcvbnm'
    for i in range(30):
        token+=random.choice(charaters)
    return token

if __name__=="__main__":
    print(tokenTmp_generate())