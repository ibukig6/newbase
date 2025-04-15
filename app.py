from flask import Flask, render_template, request, url_for, redirect, session, flash
import cv2
import numpy as np
import mediapipe as mp
import csv
import os
from flask_cors import CORS
from models import con_mySQL
from datetime import timedelta
from ultralytics import YOLO

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"
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
    front_v = request.files['video2']
    if not video:
        return "未上傳側面影片", 400
    if not front_v:
        return "未上傳正面影片", 400

    if video and front_v:
        video_path = os.path.join('static', 'uploaded_video.mp4')    # 路徑
        fvideo_path = os.path.join('static', 'uploaded_video_front.mp4')    # 路徑
        video.save(video_path)      # 存影片
        front_v.save(fvideo_path)      # 存影片

        cap = cv2.VideoCapture(video_path)      # 讀取影片
        cap2 = cv2.VideoCapture(fvideo_path)      # 讀取影片
        success, frame = cap.read()
        success2, frame2 = cap2.read()

        if success and success2:
            frame_path = os.path.join('static', 'setting_pitcure.jpg')
            front_path = os.path.join('static', 'setting_pitcure_front.jpg')
            cv2.imwrite(frame_path, frame)
            cv2.imwrite(front_path, frame2)
        cap.release()
        cap2.release()

        return redirect(url_for('setting'))

@app.route('/setting')
def setting():
    return render_template('setting.html')

model = YOLO(r"static/model/best.pt")

@app.route("/submit", methods=["POST"])
def submit():
    detect_line_x = int(request.form.get("x", 720))
    detect_front_x1 = int(request.form.get("x1", 300))
    detect_front_x2 = int(request.form.get("x2", 600))
    detect_front_y1 = int(request.form.get("y1", 200))
    detect_front_y2 = int(request.form.get("y2", 500))

    cap = cv2.VideoCapture("static/uploaded_video.mp4")
    front_cap = cv2.VideoCapture("static/uploaded_video_front.mp4")

    detect = 0
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))      # 保留原尺寸
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    front_width = int(front_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    front_height = int(front_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_folder = "static/video"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, "output.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    front_output_path = os.path.join(output_folder, "output_front.mp4")
    front_out = cv2.VideoWriter(front_output_path, fourcc, fps, (front_width, front_height))

    detected_img_path = os.path.join(output_folder, "detected_frame.jpg")
    detected_front_img_path = os.path.join(output_folder, "detected_frame_front.jpg")

    while True:
        ret, frame = cap.read()
        front_ret, front_frame = front_cap.read()
        if not ret or not front_ret:
            break

        # 移除 resize，保留原始尺寸
        # frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # front_frame = cv2.resize(front_frame, (0, 0), fx=0.5, fy=0.5)

        cv2.line(frame, (detect_line_x, 0), (detect_line_x, height), (0, 0, 255), 2)
        cv2.rectangle(front_frame, (detect_front_x1, detect_front_y1), (detect_front_x2, detect_front_y2), (0, 0, 255), 2)

        results = model(frame)
        front_results = model(front_frame)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0])
                label = f"{model.names[cls]} {conf:.2f}"

                center_x = (x1 + x2) // 2

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if "baseball" in model.names[cls].lower() and center_x >= detect_line_x:
                    detect += 1

        if detect == 1:
            cv2.imwrite(detected_img_path, frame)
            cv2.imwrite(detected_front_img_path, front_frame)
            print(f"已儲存偵測到的影像: {detected_img_path}")
        elif detect > 1:
            cv2.putText(frame, "detect", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

        for front_result in front_results:
            front_boxes = front_result.boxes
            for front_box in front_boxes:
                fx1, fy1, fx2, fy2 = map(int, front_box.xyxy[0])
                front_conf = front_box.conf[0].item()
                front_cls = int(front_box.cls[0])
                front_label = f"{model.names[front_cls]} {front_conf:.2f}"

                center_x = (fx1 + fx2) // 2
                center_y = (fy1 + fy2) // 2

                cv2.rectangle(front_frame, (fx1, fy1), (fx2, fy2), (0, 255, 0), 2)
                cv2.putText(front_frame, front_label, (fx1, fy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if detect == 1:
            cv2.putText(frame, "DETECT", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

        out.write(frame)
        front_out.write(front_frame)

    cap.release()
    front_cap.release()
    out.release()
    front_out.release()

    os.remove("static/uploaded_video.mp4")
    os.remove("static/uploaded_video_front.mp4")

    return render_template("video.html", detected_img=detected_img_path, detected_front_img=detected_front_img_path)


@app.route("/video")
def video():
    return render_template("video.html")


# 初始化 MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

@app.route('/pose_index')
def pose_index():
    return render_template('pose_index.html')

@app.route("/upload_pose", methods=["POST"])
def upload_pose():
    if "pose_video" not in request.files:
        return "未上傳影片", 400

    video = request.files["pose_video"]
    if video.filename == "":
        return "沒有選擇檔案", 400

    # 儲存影片到 static 資料夾
    video_path = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded_pose_video.mp4")
    video.save(video_path)

    # 啟動 MediaPipe 偵測影片
    process_pose_video(video_path)

    return redirect(url_for("pose_video"))

def calculate_angle(a, b, c):
    """計算三點間的夾角"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def process_pose_video(input_path):
    """處理 MediaPipe 偵測骨架的影片"""
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_folder = "static/video"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, "pose_output.mp4")
    csv_file_path = os.path.join(output_folder, "pose_data.csv")
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frame", "Trigger", "Left Elbow Angle", "Right Elbow Angle", "Left Knee Angle", "Right Knee Angle"])

    frame_count = 0

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break

            frame_count += 1
            img = cv2.resize(img, (width, height))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )

            out.write(img)

    cap.release()
    out.release()

@app.route("/pose_video")
def pose_video():
    return render_template("pose_video.html")

if __name__ == '__main__':
    app.run(debug=True)
