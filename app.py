from flask import Flask, render_template, request, url_for, redirect
import cv2
import numpy as np
import os
from flask_cors import CORS
from models import con_mySQL
# from routes import auth_bp  # 引入剛剛的 Blueprint
# import mysql.connector

app = Flask(__name__)
CORS(app)
# UPLOAD_FOLDER = 'static'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:你的密碼@localhost/flask_login'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'supersecretkey'
# db.init_app(app)
# app.register_blueprint(auth_bp, url_prefix="/auth")  # 註冊藍圖

@app.route('/')
def index():
    return render_template('index.html')

login_data ={
    "張三":"123456"
}

@app.route('/login', methods=['GET','POST'])
def login():
    name = request.form.get("username")
    pwd = request.form.get("password")


    code = "select * from login_user where username='%s'" %(name)
    cursor_ans = con_mySQL(code)
    cursor_select = cursor_ans.fetchall()

    if len(cursor_select)>0:
        if pwd == cursor_select["password"]:
            return "登錄成功"
        else:
            return "登錄失敗 <a href='login.html'>返回</a>"
    else:
        return "用戶不存在 <a href='login.html'>返回</a>"
    
    
@app.route('/register', methods=['GET','POST'])
def register():
    name = request.form.get("username")
    pwd = request.form.get("password")

    if name in login_data.keys():
        return "用戶已存在 <a href='register.html'>返回</a>"
    else:
        login_data[name]=pwd
        return "註冊成功 <a href='login.html'>登入</a>"

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

@app.route("/submit", methods=["POST"])
def submit():
    x1 = int(request.form.get("x1", 730))
    x2 = int(request.form.get("x2", 740))
    y1 = int(request.form.get("y1", 150))
    y2 = int(request.form.get("y2", 450))
    print(x1, x2, y1, y2)
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
    output_path = os.path.join(output_folder, "tes.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'X264')  # 使用 mp4v 編碼
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    cut = None
    while True:
        ret, frame = cap.read()
        if not ret:
            # print("影片讀取完畢")
            break
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        newF = frame[y1:y2, x1:x2]  # 偵測範圍
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        mask = (newF >= [210, 210, 210]).all(axis=2)
        if detect == 0:
            if np.any(mask):
                cut = frame
                # print("偵測到球了")
                detect = 1

        if detect == 1:
            cv2.putText(frame, "detect", (100, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

        out.write(frame)  # 將處理過的影像寫入輸出影片

    if cut is not None:
        output = os.path.join("static/video", "detected.jpg")
        cv2.imwrite(output, cut)
        # print(f"圖片已保存至: {output}")
    else:
        print("未偵測到球，無法保存圖片")

    cap.release()
    out.release()
    # cv2.destroyAllWindows()
    os.remove("static/uploaded_video.mp4")
    os.remove("static/setting_pitcure.jpg")
    return render_template("video.html")

@app.route("/video")
def video():
    return render_template("video.html")

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)


