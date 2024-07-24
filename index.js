// index.js
document.addEventListener('DOMContentLoaded', () => {
    const ssidElement = document.getElementById('ssid');
    const bssidElement = document.getElementById('bssid');
    const ipElement = document.getElementById('ip');

    // Simulate receiving Wi-Fi information
    const simulatedWiFiInfo = {
        ssid: 'ExampleSSID',
        bssid: '00:11:22:33:44:55',
        ip: '192.168.1.100'
    };

    // Display the simulated Wi-Fi information
    ssidElement.textContent = `SSID: ${simulatedWiFiInfo.ssid}`;
    bssidElement.textContent = `BSSID: ${simulatedWiFiInfo.bssid}`;
    ipElement.textContent = `IP Address: ${simulatedWiFiInfo.ip}`;

    // Listen for messages from a native app or other source
    window.addEventListener('message', (event) => {
        try {
            const wifiInfo = JSON.parse(event.data);
            ssidElement.textContent = `SSID: ${wifiInfo.ssid}`;
            bssidElement.textContent = `BSSID: ${wifiInfo.bssid}`;
            ipElement.textContent = `IP Address: ${wifiInfo.ip}`;
        } catch (error) {
            console.error('Error parsing Wi-Fi info:', error);
        }
    });
});