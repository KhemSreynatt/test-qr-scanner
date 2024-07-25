async function getWiFiInfo() {
    let wifiInfo = {
        ssid: 'Not available',
        bssid: 'Not available',
        ip: 'Not available',
        localIP: 'Not available',
        networkType: 'Not available',
        effectiveType: 'Not available',
        downlink: 'Not available',
        rtt: 'Not available'
    };

    // Get public IP address
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        wifiInfo.ip = data.ip;
    } catch (error) {
        console.error('Error fetching IP:', error);
    }

    // Try to get local IP
    try {
        wifiInfo.localIP = await getLocalIP();
    } catch (error) {
        console.error('Error getting local IP:', error);
    }

    // Get network information
    if ('connection' in navigator) {
        const connection = navigator.connection;
        wifiInfo.networkType = connection.type;
        wifiInfo.effectiveType = connection.effectiveType;
        wifiInfo.downlink = `${connection.downlink} Mbps`;
        wifiInfo.rtt = `${connection.rtt} ms`;
    }

    // Update display
    updateDisplay(wifiInfo);

    // Get geolocation (requires user permission)
    getGeolocation();
}

// ... (include getLocalIP and getGeolocation functions from above) ...

function updateDisplay(info) {
    for (let key in info) {
        if (document.getElementById(key)) {
            document.getElementById(key).textContent = info[key];
        }
    }
}

// Call the function when the page loads
window.onload = getWiFiInfo;