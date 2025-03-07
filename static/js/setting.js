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

    canvas.width = img.width;
    canvas.height = img.height;

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

    canvas.width = img.width;
    canvas.height = img.height;

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
