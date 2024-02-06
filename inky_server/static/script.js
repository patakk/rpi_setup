

function doLabel(){
    document.getElementById("synclabel").style.opacity = 1.;
    setTimeout(()=>{document.getElementById("synclabel").style.opacity = 0.}, 15000);
}


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
let currentBrushColorIndex = 0;
let currentBgColorIndex = 1;
let brushColor = `rgb(${DESATURATED_PALETTE[currentBrushColorIndex].join(',')})`;
let bgColor = `rgb(${DESATURATED_PALETTE[currentBgColorIndex].join(',')})`;

document.addEventListener('keydown', function(event) {
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

document.addEventListener('DOMContentLoaded', (event) => {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  
    if(!canvas)
        return;

    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  
    let isDrawing = false;
  
    function startDrawing(e) {
      isDrawing = true;
      draw(e); // This is to ensure the ellipse is drawn even if the mouse is not moved
    }
  
    function draw(e) {
      if (!isDrawing) return;
  
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left; // Get the x-coordinate relative to the canvas
      const y = e.clientY - rect.top; // Get the y-coordinate relative to the canvas
  
      // Draw an ellipse at the mouse position
      ctx.fillStyle = brushColor;
      console.log(brushColor);
      ctx.fillRect(x, y, 44, 44);
    }
  
    function stopDrawing() {
      isDrawing = false;
    }
  
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing); // Stop drawing when the mouse leaves the canvas
  });
  