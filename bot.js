document.getElementById('startScan').addEventListener('click', function () {
    const video = document.getElementById('video');
    const resultElement = document.getElementById('result');

    // Show the video element
    video.style.display = 'block';

    // Request access to the camera
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(stream => {
            video.srcObject = stream;
            video.setAttribute('playsinline', true); // required to play video inline on iOS
            video.play();
            scanQRCode();
        })
        .catch(err => {
            console.error('Error accessing camera: ', err);
        });

    function scanQRCode() {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        function processFrame() {
            if (video.readyState === video.HAVE_ENOUGH_DATA) {
                canvas.height = video.videoHeight;
                canvas.width = video.videoWidth;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                const code = jsQR(imageData.data, canvas.width, canvas.height, { inversionAttempts: "dontInvert" });

                if (code) {
                    resultElement.textContent = `QR Code Data: ${code.data}`;
                    // Optionally, stop the camera and hide the video element
                    video.srcObject.getTracks().forEach(track => track.stop());
                    video.style.display = 'none';
                } else {
                    resultElement.textContent = 'No QR code detected.';
                }
            }
            requestAnimationFrame(processFrame);
        }

        processFrame();
    }
});
