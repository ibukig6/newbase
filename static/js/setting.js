// **側面視角 - 偵測線**
function updateDetectionLine() {
    let x = document.getElementById("x").value;
    document.getElementById("x_val").innerText = x;
    drawDetectionLine(parseInt(x));
}

function drawDetectionLine(x) {
    let canvas = document.getElementById("side_canvas");
    let ctx = canvas.getContext("2d");
    let img = document.getElementById("side_image");

    canvas.width = img.clientWidth;
    canvas.height = img.clientHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "red";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
}

// **正面視角 - 好球帶矩形**
function updateStrikeZone() {
    let x1 = parseInt(document.getElementById("x1").value);
    let x2 = parseInt(document.getElementById("x2").value);
    let y1 = parseInt(document.getElementById("y1").value);
    let y2 = parseInt(document.getElementById("y2").value);

    document.getElementById("x1_val").innerText = x1;
    document.getElementById("x2_val").innerText = x2;
    document.getElementById("y1_val").innerText = y1;
    document.getElementById("y2_val").innerText = y2;

    drawStrikeZone(x1, x2, y1, y2);
}

function drawStrikeZone(x1, x2, y1, y2) {
    let canvas = document.getElementById("front_canvas");
    let ctx = canvas.getContext("2d");
    let img = document.getElementById("front_image");

    canvas.width = img.clientWidth;
    canvas.height = img.clientHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "red";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.rect(x1, y1, x2 - x1, y2 - y1);
    ctx.stroke();
}

// **初始化畫布**
window.onload = function () {
    updateDetectionLine();
    updateStrikeZone();
};

// **靈活轉換：根據圖片實際縮放比自動轉換回原始座標**
document.querySelector("form").addEventListener("submit", function (e) {
    const sideImg = document.getElementById("side_image");
    const frontImg = document.getElementById("front_image");

    // 側面圖比例
    const sideScaleX = sideImg.naturalWidth / sideImg.clientWidth;

    // 側面偵測線
    const x = document.getElementById("x");
    x.value = Math.round(parseInt(x.value) * sideScaleX);

    // 正面圖比例
    const frontScaleX = frontImg.naturalWidth / frontImg.clientWidth;
    const frontScaleY = frontImg.naturalHeight / frontImg.clientHeight;

    // 正面好球帶
    const x1 = document.getElementById("x1");
    const x2 = document.getElementById("x2");
    const y1 = document.getElementById("y1");
    const y2 = document.getElementById("y2");

    x1.value = Math.round(parseInt(x1.value) * frontScaleX);
    x2.value = Math.round(parseInt(x2.value) * frontScaleX);
    y1.value = Math.round(parseInt(y1.value) * frontScaleY);
    y2.value = Math.round(parseInt(y2.value) * frontScaleY);
});
