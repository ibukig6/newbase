const image = document.getElementById('image');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// 獲取圖片訊息
let img = new Image();
img.src = "static/setting_pitcure.jpg";

let img2 = document.getElementById("image");
img.onload = function() {
    console.log("原始寬度:", img.width);
    console.log("原始高度:", img.height);
};
img2.onload = function() {
    console.log("網站上寬度:", img2.width);
    console.log("網站上高度:", img2.height);
};


// 即時更新數值
function updateSettings() {
    // 獲取滑桿數值
    let x1 = document.getElementById('x1');
    let x2 = document.getElementById('x2');
    let y1 = document.getElementById('y1');
    let y2 = document.getElementById('y2');

    // 讓 X1 最大值不超過 X2-1
    x1.max = x2.value - 1;
    if (parseInt(x1.value) >= parseInt(x2.value)) {
        x1.value = x2.value - 1; // 若 X1 超過範圍，自動調整
    }

    // 讓 X2 最小值不低於 X1+1
    x2.min = parseInt(x1.value) + 1;
    if (parseInt(x2.value) <= parseInt(x1.value)) {
        x2.value = parseInt(x1.value) + 1; // 若 X2 低於範圍，自動調整
    }

    // 讓 Y1 最大值不超過 Y2-1
    y1.max = y2.value - 1;
    if (parseInt(y1.value) >= parseInt(y2.value)) {
        y1.value = y2.value - 1; // 若 Y1 超過範圍，自動調整
    }

    // 讓 Y2 最小值不低於 Y1+1
    y2.min = parseInt(y1.value) + 1;
    if (parseInt(y2.value) <= parseInt(y1.value)) {
        y2.value = parseInt(y1.value) + 1; // 若 Y2 低於範圍，自動調整
    }

    // 更新數值顯示
    document.getElementById('x1_val').innerText = x1.value;
    document.getElementById('x2_val').innerText = x2.value;
    document.getElementById('y1_val').innerText = y1.value;
    document.getElementById('y2_val').innerText = y2.value;

    // 重新繪製矩形，這裡假設 drawRectangle() 需要的是寬高
    drawRectangle(parseInt(x1.value), parseInt(y1.value), 
                parseInt(x2.value), 
                parseInt(y2.value));
}


function drawRectangle(x1, y1, x2, y2) {
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');

    // 清除之前的畫面
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 設定不同顏色
    ctx.lineWidth = 3;

    // 左邊 (紅色)
    ctx.strokeStyle = 'red';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1, y2);
    ctx.stroke();

    // 右邊 (藍色)
    ctx.strokeStyle = 'blue';
    ctx.beginPath();
    ctx.moveTo(x2, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // 上邊 (綠色)
    ctx.strokeStyle = 'green';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y1);
    ctx.stroke();

    // 下邊 (橘色)
    ctx.strokeStyle = 'orange';
    ctx.beginPath();
    ctx.moveTo(x1, y2);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}

// 更新值時重新繪製
function updateValue(span_id, value) {
    document.getElementById(span_id).innerText = value;
    
    let x1 = parseInt(document.getElementById('x1').value);
    let x2 = parseInt(document.getElementById('x2').value);
    let y1 = parseInt(document.getElementById('y1').value);
    let y2 = parseInt(document.getElementById('y2').value);

    drawRectangle(x1, y1, x2, y2);
}


// 頁面加載時初始化畫布
window.onload = function() {
    let image = document.getElementById('image');
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');

    // 設定 Canvas 尺寸與圖片相同
    canvas.width = image.width;
    canvas.height = image.height;

    // 初始繪製
    drawRectangle(730, 150, 740, 450); // 預設範圍
};