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
    console.log('Parsing QR Code:', qrResult); // Debugging line
    const wifiRegex = /^WIFI:S:([^;]+);T:WPA;P:([^;]+);;$/;
    const match = qrResult.match(wifiRegex);
    if (match) {
        console.log('Parsed SSID:', match[1]); // Debugging line
        console.log('Parsed Password:', match[2]); // Debugging line
        return {
            ssid: match[1],
            password: match[2]
        };
    }
    console.log('Failed to parse QR Code:', qrResult); // Debugging line
    return null;
}