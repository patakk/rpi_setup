

const DESATURATED_PALETTE = [
    [0, 0, 0],
    [255, 255, 255],
    [0, 255, 0],
    [0, 0, 255],
    [255, 0, 0],
    [255, 255, 0],
    [255, 140, 0],
];

let canvas;
let ctx;
let isDrawing = false;
let currentBrushColorIndex = 0;
let currentBgColorIndex = 1;
let brushColor = `rgb(${DESATURATED_PALETTE[currentBrushColorIndex].join(',')})`;
let bgColor = `rgb(${DESATURATED_PALETTE[currentBgColorIndex].join(',')})`;

document.addEventListener('keydown', function (event) {
    if (event.key === 'q') {
        currentBrushColorIndex = (currentBrushColorIndex + 1) % DESATURATED_PALETTE.length;
        brushColor = `rgb(${DESATURATED_PALETTE[currentBrushColorIndex].join(',')})`;
    }
    if (event.key === 'e') {
        currentBgColorIndex = (currentBgColorIndex + 1) % DESATURATED_PALETTE.length;
        bgColor = `rgb(${DESATURATED_PALETTE[currentBgColorIndex].join(',')})`;
        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    if (event.key === 'c') {
        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
});

function sendCanvasToServer() {
    doLabel();
    var dataURL = canvas.toDataURL('image/png');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload_canvas', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            console.log('Server responded with:', response);
        }
    };
    xhr.send(JSON.stringify({ image: dataURL }));
}

document.addEventListener('touchmove',
    function (event) {
        event.preventDefault();
    },
    { passive: false }
);

function draw(e) {
    if (!isDrawing) return;

    let clientX, clientY;
    if (e.touches) {
        clientX = e.touches[0].clientX;
        clientY = e.touches[0].clientY;
    } else {
        clientX = e.clientX;
        clientY = e.clientY;
    }

    const rect = canvas.getBoundingClientRect();
    const x = clientX - rect.left; // Get the x-coordinate relative to the canvas
    const y = clientY - rect.top; // Get the y-coordinate relative to the canvas

    // Draw an ellipse at the mouse/touch position
    ctx.fillStyle = brushColor;
    console.log(brushColor);
    ctx.fillRect(x, y, 44, 44);
}

function stopDrawing() {
    isDrawing = false;
}


document.addEventListener('DOMContentLoaded', (event) => {
    let aspect = 800 / 480;
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    if(window.innerWidth < window.innerHeight){
        canvas.style.width = window.innerWidth-5*2 + "px";
        canvas.style.height = (window.innerWidth-5*2) / aspect + "px";
    }
    else{
        canvas.style.width = window.innerWidth * .6 + "px";
        canvas.style.height = window.innerWidth * .6 / aspect + "px";
    }

    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    if (!canvas) return;

    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    function startDrawing(e) {
        isDrawing = true;
        draw(e); // This is to ensure the ellipse is drawn even if the mouse/touch is not moved
    }

    // Mouse event listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing); // Stop drawing when the mouse leaves the canvas

    // Touch event listeners
    canvas.addEventListener('touchstart', function (e) {
        e.preventDefault(); // Prevent scrolling when touching the canvas
        startDrawing(e);
    }, { passive: false });

    canvas.addEventListener('touchmove', function (e) {
        e.preventDefault(); // Prevent scrolling when touching the canvas
        draw(e);
    }, { passive: false });

    canvas.addEventListener('touchend', function (e) {
        e.preventDefault(); // Prevent additional mouse event firing
        stopDrawing();
    }, { passive: false });

    canvas.addEventListener('touchcancel', stopDrawing); // Stop drawing when the touch is cancelled
});