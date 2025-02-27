# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from models import db, User
# from flask import session

# auth_bp = Blueprint('auth', __name__)  # 註冊藍圖

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if User.query.filter_by(username=username).first():
#             flash("使用者名稱已存在！")
#         else:
#             user = User(username=username)
#             user.set_password(password)
#             db.session.add(user)
#             db.session.commit()
#             flash("註冊成功！請登入")
#             return redirect(url_for('auth.login'))
#     return render_template('register.html')

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             session['user_id'] = user.id
#             flash("登入成功！")
#             return redirect(url_for('auth.login'))  
#         else:
#             flash("登入失敗，請檢查帳號或密碼")
#     return render_template('login.html')

# @auth_bp.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('auth.login'))
#     return "這是您的儀表板，歡迎！"
