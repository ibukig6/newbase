from flask import Flask, render_template, request, url_for, redirect
import cv2
import numpy as np
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/input")
def input():
    return render_template("input.html")

@app.route('/upload', methods=['POST'])
def upload():
    video = request.files['video']
    if not video:
        return "未上傳影片", 400

    if video:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_video.mp4')    # 路徑
        video.save(video_path)      # 存影片

        cap = cv2.VideoCapture(video_path)      # 讀取影片
        success, frame = cap.read()

        if success:
            frame_path = os.path.join(app.config['UPLOAD_FOLDER'], 'setting_pitcure.jpg')
            cv2.imwrite(frame_path, frame)
        cap.release()

        return redirect(url_for('setting'))

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/submit_setting', methods=["POST"])
def submit_setting():
    x1 = int(request.form["x1"])
    x2 = int(request.form["x2"])
    y1 = int(request.form["y1"])
    y2 = int(request.form["y2"])

    newF = (y1, y2, x1, x2)
    return f"Selected range: newF = frame[{y1}:{y2}, {x1}:{x2}]"

@app.route("/submit", methods=["POST"])
def submit():
    # 接收影片檔案
    video_file = request.files["video"]
    if not video_file:
        return "未上傳影片", 400

    # 保存上傳的影片到伺服器
    upload_folder = "uploads"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    video_path = os.path.join(upload_folder, video_file.filename)
    video_file.save(video_path)  # 將影片保存到伺服器

    # 使用 OpenCV 處理影片
    cap = cv2.VideoCapture("uploads/v_1.mp4")
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
    s = 0
    while True:
        s += 1
        ret, frame = cap.read()
        if not ret:
            print("影片讀取完畢")
            break
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        newF = frame[150:450, 730:740]  # 偵測範圍
        cv2.rectangle(frame, (730, 150), (740, 450), (0, 0, 255), 2)

        mask = (newF >= [210, 210, 210]).all(axis=2)
        if detect == 0:
            if np.any(mask):
                cut = frame
                print("偵測到球了")
                detect = 1

        if detect == 1:
            cv2.putText(frame, "detect", (100, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

        out.write(frame)  # 將處理過的影像寫入輸出影片

    if cut is not None:
        output = os.path.join("static/video", "detected.jpg")
        cv2.imwrite(output, cut)
        print(f"圖片已保存至: {output}")
    else:
        print("未偵測到球，無法保存圖片")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"影片總幀數: {s}")
    return render_template("video.html")

@app.route("/video")
def video():
    return render_template("video.html")

if __name__ == '__main__':
    app.run(debug=True)
