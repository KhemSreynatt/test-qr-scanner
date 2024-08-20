document.addEventListener("DOMContentLoaded", function () {
    const jsonList = [
        { "isp": "S.I Group", "ipv4": "203.217.168.43", "branch": "SINET SR", "branch_id": "3", "gps": "11.556249586635, 104.921818467" },
        { "isp": "Another ISP", "ipv4": "192.168.1.1", "branch": "Branch A", "branch_id": "1", "gps": "10.000000, 105.000000" }
    ];

    // Hash the JSON objects
    function hashJsonData(jsonData) {
        const jsonString = JSON.stringify(jsonData);
        const encoder = new TextEncoder();
        const data = encoder.encode(jsonString);

        return crypto.subtle.digest('SHA-256', data).then(hash => {
            return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
        });
    }

    // Compare the scanned QR code data with the pre-hashed JSON data
    async function compareScannedData(scannedData) {
        const scannedHash = await hashJsonData(scannedData);

        for (let i = 0; i < jsonList.length; i++) {
            const originalHash = await hashJsonData(jsonList[i]);
            if (scannedHash === originalHash) {
                return true; // Match found
            }
        }
        return false; // No match
    }

    // Initialize the QR code scanner
    const html5QrCode = new Html5Qrcode("reader");
    const qrCodeSuccessCallback = (decodedText, decodedResult) => {
        try {
            const scannedData = JSON.parse(decodedText);
            compareScannedData(scannedData).then(isMatch => {
                if (isMatch) {
                    document.getElementById("result").innerText = "QR Code matched!";
                } else {
                    document.getElementById("result").innerText = "No match found.";
                }
            });
        } catch (error) {
            document.getElementById("result").innerText = "Invalid QR code data.";
        }
    };

    const config = { fps: 10, qrbox: 250 };
    html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback)
        .catch(err => {
            console.error(`Unable to start scanning, error: ${err}`);
        });
});
