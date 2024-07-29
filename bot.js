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

                    // Parse the QR code data for Wi-Fi credentials
                    const wifiData = parseWifiData(code.data);
                    if (wifiData) {
                        // Display instructions or provide a download link for a configuration file
                        resultElement.innerHTML = `Connect to Wi-Fi:<br>SSID: ${wifiData.ssid}<br>Type: ${wifiData.type}<br>Password: ${wifiData.password}<br>`;
                        // Optionally, provide a downloadable file with the credentials
                        // For example, create a configuration file (this is platform-specific)
                        createDownloadableConfigFile(wifiData);
                    } else {
                        resultElement.textContent = 'Invalid QR code format.';
                    }

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

    function parseWifiData(data) {
        // Example QR code format: WIFI:S:<SSID>;T:<TYPE>;P:<PASSWORD>;;
        const regex = /WIFI:S:(.*?);T:(.*?);P:(.*?);;/;
        const match = data.match(regex);
        if (match) {
            return {
                ssid: match[1],
                type: match[2],
                password: match[3]
            };
        }
        return null;
    }

    function createDownloadableConfigFile(wifiData) {
        // Create a downloadable file or provide instructions
        const content = `SSID: ${wifiData.ssid}\nType: ${wifiData.type}\nPassword: ${wifiData.password}`;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'wifi-config.txt';
        a.textContent = 'Download Wi-Fi Configuration File';
        resultElement.appendChild(a);
    }
});
