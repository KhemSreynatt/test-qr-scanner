
const video = document.getElementById('qr-video');
const canvasElement = document.getElementById('qr-canvas');
const canvas = canvasElement.getContext('2d');
const qrResult = document.getElementById('qr-result');
const STOP_DELAY = 1000;
let scanning = false;

document.getElementById('scan_qrcode').addEventListener('click', function () {


});
const scanQRButton = document.getElementById('scan_qrcode');



function startScanning() {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function (stream) {
        scanning = true;
        video.srcObject = stream;
        video.setAttribute('playsinline', true);
        video.play();
        requestAnimationFrame(tick);
    }).catch(function (error) {
        console.error("Error accessing the camera", error);
        qrResult.textContent = "Error accessing the camera: " + error.message;
    });
}
function stopScanning() {
    scanning = false;
    video.pause();
    video.srcObject.getTracks().forEach(track => track.stop());
    qrResult.textContent += " (Scanning stopped)";
}
function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvasElement.height = video.videoHeight;
        canvasElement.width = video.videoWidth;
        canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
        var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
        var code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: "dontInvert",
        });
        if (code) {
            drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
            drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
            drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
            drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
            qrResult.textContent = "Detected QR code: " + code.data;

            // Add a delay before stopping the scanner
            setTimeout(() => {
                alert('Scan Done!');
                stopScanning();
            }, STOP_DELAY);

            return;
        } else {
            qrResult.textContent = "No QR code detected.";
        }
    }
    if (scanning) {
        requestAnimationFrame(tick);
    }
}

function drawLine(begin, end, color) {
    canvas.beginPath();
    canvas.moveTo(begin.x, begin.y);
    canvas.lineTo(end.x, end.y);
    canvas.lineWidth = 4;
    canvas.strokeStyle = color;
    canvas.stroke();
}

scanQRButton.addEventListener('click', startScanning());