// index.js
document.addEventListener('DOMContentLoaded', () => {
    const ssidElement = document.getElementById('ssid');
    const bssidElement = document.getElementById('bssid');

    window.addEventListener('message', (event) => {
        try {
            const wifiInfo = JSON.parse(event.data);
            ssidElement.textContent = `SSID: ${wifiInfo.ssid}`;
            bssidElement.textContent = `BSSID: ${wifiInfo.bssid}`;
        } catch (error) {
            console.error('Error parsing Wi-Fi info:', error);
        }
    });
});