# from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# from models import db, User

# # 創建 Blueprint（用來管理登入/註冊）
# auth_bp = Blueprint('auth', __name__)

# # 登入頁面
# @auth_bp.route('/')
# def login():
#     return render_template('login.html')

# # 註冊頁面
# @auth_bp.route('/register')
# def register():
#     return render_template('register.html')

# # 登入邏輯
# @auth_bp.route('/login_form', methods=['POST'])
# def login_form():
#     name = request.form.get("username")
#     pwd = request.form.get("password")

#     user = User.query.filter_by(username=name).first()  # 從資料庫查詢使用者
#     if user and user.check_password(pwd):
#         session['user_id'] = user.id  # 記錄登入狀態
#         flash("登入成功！", "success")
#         return redirect(url_for('dashboard'))  # 將來可以導向 dashboard
#     else:
#         flash("登入失敗，請檢查帳號或密碼", "danger")
#         return redirect(url_for('auth.login'))

# # 註冊邏輯
# @auth_bp.route('/register_form', methods=['POST'])
# def register_form():
#     name = request.form.get("username")
#     pwd = request.form.get("password")

#     if User.query.filter_by(username=name).first():
#         flash("使用者名稱已存在！", "warning")
#         return redirect(url_for('auth.register'))
    
#     new_user = User(username=name)
#     new_user.set_password(pwd)  # 加密密碼
#     db.session.add(new_user)
#     db.session.commit()

#     flash("註冊成功！請登入", "success")
#     return redirect(url_for('auth.login'))

# # 儀表板（登入成功後才能訪問）
# @auth_bp.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('auth.login'))
#     return "這是您的儀表板，歡迎！"

# # 登出
# @auth_bp.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash("已成功登出！", "info")
#     return redirect(url_for('auth.login'))
import torch
print(torch.cuda.memory_allocated() / 1024**2, "MB 已使用")
print(torch.cuda.memory_reserved() / 1024**2, "MB 預留")



