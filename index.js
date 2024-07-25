// // index.js
// document.addEventListener('DOMContentLoaded', () => {
//     const ssidElement = document.getElementById('ssid');
//     const bssidElement = document.getElementById('bssid');
//     const ipElement = document.getElementById('ip');

//     // Simulate receiving Wi-Fi information
//     const simulatedWiFiInfo = {
//         ssid: 'ExampleSSID',
//         bssid: '00:11:22:33:44:55',
//         ip: '192.168.1.100'
//     };

//     // Display the simulated Wi-Fi information
//     ssidElement.textContent = `SSID: ${simulatedWiFiInfo.ssid}`;
//     bssidElement.textContent = `BSSID: ${simulatedWiFiInfo.bssid}`;
//     ipElement.textContent = `IP Address: ${simulatedWiFiInfo.ip}`;

//     // Listen for messages from a native app or other source
//     window.addEventListener('message', (event) => {
//         try {
//             const wifiInfo = JSON.parse(event.data);
//             ssidElement.textContent = `SSID: ${wifiInfo.ssid}`;
//             bssidElement.textContent = `BSSID: ${wifiInfo.bssid}`;
//             ipElement.textContent = `IP Address: ${wifiInfo.ip}`;
//         } catch (error) {
//             console.error('Error parsing Wi-Fi info:', error);
//         }
//     });
// });

function getWiFiInfo() {
    let wifiInfo = {
        ssid: 'Not available',
        bssid: 'Not available',
        ip: 'Not available',
        name: 'Not available'
    };

    // Get IP address
    fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {
            wifiInfo.ip = data.ip;
            updateDisplay(wifiInfo);
        })
        .catch(error => console.error('Error fetching IP:', error));

    // Try to get network information if available
    if ('connection' in navigator && 'type' in navigator.connection) {
        wifiInfo.name = navigator.connection.type;
    }

    // Update display with available information
    updateDisplay(wifiInfo);
}

function updateDisplay(info) {
    document.getElementById('ssid').textContent = info.ssid;
    document.getElementById('bssid').textContent = info.bssid;
    document.getElementById('ip').textContent = info.ip;
    document.getElementById('name').textContent = info.name;
}

// Call the function when the page loads
window.onload = getWiFiInfo;