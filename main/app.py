from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify
from utils import username_check,password_check,email_check, hash_encipher, decryptor_check,alert,path_generate

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个安全的密钥用于签名会话

user_list = {
    "heihe": hash_encipher('1234321'),
    "baishan": hash_encipher('1234'),
    "mool": hash_encipher('bilibili')  
    }

path_list = {
    "heihe": 'qwer',
    "baishan": 'asdf',
    "mool": 'zxcv'
    }

email_list={
    "heihe": 'heihe@qq.com',
    "baishan": 'baishan@qq.com',
    "mool": 'mool@qq.com'

}



# 本地API——查询path（下载结果）
@app.route('/api/search_path', methods=['GET'])
def search_path():
    username = request.args.get('username')
    password = request.args.get('password')

    # 检查请求来源是否是本地
    if request.remote_addr != '127.0.0.1':
        abort(403)  # 403错误：权限不足

    # 现有的验证逻辑...
    if username in user_list:
        if decryptor_check(password,user_list.get(username)):
            path=path_list[username]
            return jsonify({'result': False, "error_message": 'Token is not correct','path':path})
        else:
            return jsonify({'result': False, "error_message": 'Password is not correct','path':None})
    else:
        return jsonify({'result': False, "error_message": 'User not exist','path':None})


# 本地API——创建path（创建项目）
@app.route('/api/create_path', methods=['GET'])
def create_path():
    username = request.args.get('username')
    password = request.args.get('password')

    # 检查请求来源是否是本地
    if request.remote_addr != '127.0.0.1':
        abort(403)  # 403错误：权限不足

    # 现有的验证逻辑...
    if username in user_list:
        if decryptor_check(password,user_list.get(username)):
            path_list[username]=path_generate()
            path=path_list[username]
            return jsonify({'result': False, "error_message": 'Token is not correct','path':path})
        else:
            return jsonify({'result': False, "error_message": 'Password is not correct','path':None})
    else:
        return jsonify({'result': False, "error_message": 'User not exist','path':None})





class User(views.MethodView):
    def get(self):
        username = session.get('username')  # 从会话获取用户名
        if not username:
            return redirect(url_for('login'))  # 如果没有用户名，则重定向到登录页面
        
        key = token_list.get(username, '未找到您的秘钥！')  # 从token_list获取秘钥
        email=email_list.get(username,'未找到您的邮箱！')   # 从email_list获取秘钥
        return render_template('profile.html', username=username, key=key,email=email)



class Login(views.MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        if username in user_list and decryptor_check(password,user_list[username]):
            session['username'] = username
            return redirect(url_for('user'))  #随后User类去session中查询用户名
        else:
            error = "密码错误" if username in user_list else "用户不存在"  #error存储错误信息，要么是 “密码错误” 要么是 “用户不存在”
            return render_template("login.html", error=error)  #出现错误时，把错误信息传到login.html里，这样就不会重定向到一个新的网页




class Register(views.MethodView):
    def get(self):
            return render_template('register.html')
    def post(self):

        username=request.form.get('fullname')
        email=request.form.get('email') 
        password=request.form.get('password')
        confirm_password=request.form.get('confirm-password')

        username_result,username_error=username_check(username)
        email_result,email_error=email_check(email)
        password_result,password_error=password_check(password)

        if username_result:
            if email_result:
                if password_result:
                    if password==confirm_password:  
                        session['username'] = username
                        user_list[username] = hash_encipher(password)
                        # token_list[username] = token_generate()
                        email_list[username] = email
                        return redirect(url_for('user')) 
                    else:
                        return render_template('register.html',error="确认密码不匹配！")
                else:
                    return render_template('register.html',error=password_error)
            else:
                return render_template('register.html',error=email_error)
        else:
            return render_template('register.html',error=username_error)
        
        



# 注册路由
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/', view_func=Login.as_view('main_website'))
app.add_url_rule('/user', view_func=User.as_view('user'))
app.add_url_rule('/register',view_func=Register.as_view('register'))




# 错误处理模块
@app.errorhandler(404)
def handle_404_error(err):
    # return "发生了错误，错误情况是：%s"%err
    return render_template('404.html')
@app.errorhandler(403)
def handle_404_error(err):
    # return "发生了错误，错误情况是：%s"%err
    return render_template('403.html')




if __name__ == '__main__':
    app.run(debug=True)

# session存储了当前用户名
