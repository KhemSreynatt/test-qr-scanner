document.getElementById('startButton').addEventListener('click', () => {
    const codeReader = new ZXing.BrowserQRCodeReader();
    const previewElem = document.getElementById('preview');

    codeReader.decodeFromVideoDevice(null, previewElem, (result, err) => {
        if (result) {
            const wifiCredentials = parseWifiConfig(result.text);
            if (wifiCredentials) {
                document.getElementById('wifiCredentials').innerText = `SSID: ${wifiCredentials.ssid}, Password: ${wifiCredentials.password}`;
                connectToWifi(wifiCredentials.ssid, wifiCredentials.password);
            } else {
                document.getElementById('wifiCredentials').innerText = 'Invalid Wi-Fi QR code.';
            }
        }
        if (err && !(err instanceof ZXing.NotFoundException)) {
            console.error(err);
            document.getElementById('wifiCredentials').innerText = 'Error reading QR code.';
        }
    });
});

function parseWifiConfig(qrResult) {
    const match = qrResult.match(/WIFI:T:(WPA|WEP|nopass);S:([^;]+);P:([^;]*);H:(true|false);?/);
    if (match) {
        return {
            ssid: match[2],
            password: match[3]
        };
    }
    return null;
}

function connectToWifi(ssid, password) {
    // This function is a placeholder. Connecting to Wi-Fi via JavaScript is not possible due to security reasons.
    console.log(`Connecting to Wi-Fi network: SSID: ${ssid}, Password: ${password}`);
}