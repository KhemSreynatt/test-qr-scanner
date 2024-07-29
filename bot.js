document.getElementById('startButton').addEventListener('click', () => {
    const codeReader = new ZXing.BrowserQRCodeReader();
    const previewElem = document.getElementById('preview');

    codeReader.decodeFromVideoDevice(null, previewElem, (result, err) => {
        if (result) {
            console.log('QR Code result:', result.text); // Debugging line
            const wifiCredentials = parseWifiConfig(result.text);
            if (wifiCredentials) {
                document.getElementById('wifiCredentials').innerText = `SSID: ${wifiCredentials.ssid}, Password: ${wifiCredentials.password}`;
                // Here you can add additional logic to handle the Wi-Fi connection
            } else {
                document.getElementById('wifiCredentials').innerText = 'Invalid Wi-Fi QR code.';
            }
        } else if (err && !(err instanceof ZXing.NotFoundException)) {
            console.error(err);
            document.getElementById('wifiCredentials').innerText = 'Error reading QR code.';
        }
    });
});

function parseWifiConfig(qrResult) {
    const wifiRegex = /^WIFI:T:(WPA|WEP|nopass);S:([^;]+);P:([^;]*);H:(true|false)?;?$/;
    const match = qrResult.match(wifiRegex);
    if (match) {
        return {
            ssid: match[2],
            password: match[3]
        };
    }
    console.log('Failed to parse QR Code:', qrResult); // Debugging line
    return null;
}