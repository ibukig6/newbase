const image = document.getElementById('image');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// 獲取圖片訊息
let img = new Image();
img.src = "static/setting_pitcure.jpg";

img.onload = function() {
    console.log("原始寬度:", img.width);
    console.log("原始高度:", img.height);
};

// 取得影片高度（假設影片高度為 720，未來可以動態設定）
let videoHeight = 720;  // 這個數值可以從 Python 傳遞到 HTML

// 即時更新數值
function updateSettings() {
    let x = document.getElementById('x');

    // 更新數值顯示
    document.getElementById('x_val').innerText = x.value;

    // 重新繪製偵測線
    drawDetectionLine(parseInt(x.value));
}

// 繪製一條垂直偵測線
function drawDetectionLine(x) {
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');

    // 設定 Canvas 尺寸與圖片相同
    canvas.width = image.width;
    canvas.height = image.height;

    // 清除之前的畫面
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 畫一條紅色的垂直線，從 `y=0` 到 `y=最大影片高度`
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, videoHeight);  // 讓 Y 軸最大值與影片高度一致
    ctx.stroke();
}

// 頁面加載時初始化畫布
window.onload = function() {
    let image = document.getElementById('image');
    let canvas = document.getElementById('canvas');

    // 設定 Canvas 尺寸與圖片相同
    canvas.width = image.width;
    canvas.height = image.height;

    // 初始繪製偵測線
    drawDetectionLine(730); // 預設位置
};
