from flask import request, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash
from database.models_user import User
from database.config import db
from sqlalchemy.exc import SQLAlchemyError



# https://yourdomain.com/reset-password?token=abc123xyz


@app.route('/submit-new-password', methods=['POST'])
def submit_new_password():
    token = request.args.get('token')  # 假设链接中带有token参数
    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-new-password')

    if new_password != confirm_password:
        flash('Passwords do not match. Please try again.')
        return redirect(url_for('reset_password', token=token))  # 重定向回密码重置页面

    try:
        # 这里需要一个函数来根据token找到用户
        user_id = verify_reset_token(token)  # 你需要实现这个函数
        if not user_id:
            flash('Invalid or expired token.')
            return redirect(url_for('login'))

        user = User.query.get(user_id)
        if user:
            user.Password = generate_password_hash(new_password)
            db.session.commit()
            flash('Your password has been updated successfully.')
            return redirect(url_for('login'))
        else:
            flash('User not found.')
            return redirect(url_for('login'))
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during password reset: {e}")
        flash('An error occurred. Please try again.')
        return redirect(url_for('reset_password', token=token))

def verify_reset_token(token):
    # 这里添加你的逻辑来验证token并解析出user_id
    return None
