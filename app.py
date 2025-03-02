from flask import Flask, render_template, request, url_for, redirect, session, flash
import cv2
import numpy as np
import os
from flask_cors import CORS
from models import con_mySQL
from datetime import timedelta
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1/60)
app.secret_key = "123654"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:你的密碼@localhost/flask_login'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'supersecretkey'

# db.init_app(app)

# app.register_blueprint(auth_bp, url_prefix="/auth")

# 註冊與登入
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login_form', methods=['GET','POST'])
def login_form():
    name = request.form.get("username")
    pwd = request.form.get("password")

    code = "select * from login_user where username='%s'" %(name)
    cursor_ans = con_mySQL(code)
    cursor_select = cursor_ans.fetchall()

    if len(cursor_select)>0:
        if pwd == cursor_select[0]["password"]:
            session["username"] = name
            return redirect(url_for('home'))
        else:
            return "登入失敗 <a href='/'>返回</a>"
    else:
        return "用戶不存在 <a href='/'>返回</a>"
    
    
@app.route('/register_form', methods=['GET','POST'])
def register_form():
    name = request.form.get("username")
    pwd = request.form.get("password")
    pwd2 = request.form.get("password2")

    if pwd2 != pwd:
        return "密碼不一致 <a href='/register_form'>返回註冊頁面</a>"

    code = "select * from login_user where username='%s'" %(name)
    cursor_ans = con_mySQL(code)
    cursor_select = cursor_ans.fetchall()

    if len(cursor_select)>0:
        return "用戶已存在 <a href='/register'>返回</a>"
    else:
        code = "INSERT INTO `login_user` (`username`, `password`) VALUES ('%s', '%s')" %(name, pwd)
        con_mySQL(code)
        return "註冊成功 <a href='/'>登入</a>"

@app.route('/home')
def home():
    if "username" in session:                               # 這行後面我打算寫成函式
        return render_template('home.html')
    else:
        return "小調皮，還想專漏洞啊？ <a href='/'>知道錯了並回登入畫面</a>"
    
@app.route('/logout')
def logout():
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1/60)
    session.pop("user_id", None)
    flash("已成功登出！", "info")
    return redirect(url_for('login'))

# 上傳影片
@app.route("/input")
def input():
    return render_template("input.html")

@app.route('/upload', methods=['POST'])
def upload():
    video = request.files['video']
    if not video:
        return "未上傳影片", 400

    if video:
        video_path = os.path.join('static', 'uploaded_video.mp4')    # 路徑
        video.save(video_path)      # 存影片

        cap = cv2.VideoCapture(video_path)      # 讀取影片
        success, frame = cap.read()

        if success:
            frame_path = os.path.join('static', 'setting_pitcure.jpg')
            cv2.imwrite(frame_path, frame)
        cap.release()

        return redirect(url_for('setting'))

@app.route('/setting')
def setting():
    return render_template('setting.html')

model = YOLO(r"static/model/best.pt")
@app.route("/submit", methods=["POST"])
def submit():
    detect_line_x = int(request.form.get("x", 720))

    # print(x1, x2, y1, y2)
    # 使用 OpenCV 處理影片
    cap = cv2.VideoCapture("static/uploaded_video.mp4")
    detect = 0
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 幀率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.5)  # 調整後的寬
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.5)  # 調整後的高

    # 確保輸出目錄存在
    output_folder = "static/video"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 定義輸出的影片路徑
    output_path = os.path.join(output_folder, "output.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'X264')  # 使用 mp4v 編碼
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    while True:
        ret, frame = cap.read()
        if not ret:
            # print("影片讀取完畢")
            break
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # newF = frame[y1:y2, detect_line_x:x2]  # 偵測範圍
        cv2.line(frame, (detect_line_x, 0), (detect_line_x, height), (0, 0, 255), 2)

        results = model(frame)

        for result in results:
            boxes = result.boxes  # 取得所有偵測框
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # 取得座標
                conf = box.conf[0].item()  # 信心分數
                cls = int(box.cls[0])  # 取得物件類別
                label = f"{model.names[cls]} {conf:.2f}"

                # 計算物件中心點
                center_x = (x1 + x2) // 2

                # 畫出邊界框
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # 如果偵測到 "baseball" 且中心點超過偵測線
                if "baseball" in model.names[cls].lower() and center_x > detect_line_x:
                    detect += 1

        # 標記偵測狀態
        if detect == 1:
            detected_img_path = os.path.join(output_folder, "detected_frame.jpg")
            cv2.imwrite(detected_img_path, frame)
            print(f"已儲存偵測到的影像: {detected_img_path}")
        elif detect > 1:
            cv2.putText(frame, "detect", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

        # 儲存處理過的影片
        out.write(frame)

    # 釋放資源
    cap.release()
    out.release()
    os.remove("static/uploaded_video.mp4")  # 刪除上傳的影片

    return render_template("video.html", detected_img=detected_img_path)

@app.route("/video")
def video():
    return render_template("video.html")

if __name__ == '__main__':
    app.run(debug=True)
