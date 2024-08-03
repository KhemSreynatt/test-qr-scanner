
import * as my_dongle from 'bleuio'
import 'regenerator-runtime / runtime'

// Works the first time I drive
// If I stop it and try to start again, nothing happens

// After trying to insert a sleep () after at_advdatai () (line 102)
// does it work to run it over and over again

// The dongles I have work differently when I run this.
// On the marked dongle I can start a beacon once (if I do not use sleep ())
// so it can not start again if I have stopped it.
// The unmarked dongle will be reset as soon as I try to create an iBeacon


const output = document.querySelector("# output");
const connectButton = document.querySelector('# connectButton');
const iBeaconButton = document.querySelector('# iBeaconButton');
const uuidInputField = document.querySelector('# uuidInputField');

let isConnected = false;
let isAdvertising = false;

// / **
//  * Connects / disconnects the dongle
//  * /
const handleConnectButton = async () => {
    if (!isConnected) {
        connect();
    } else {
        disconnect();
    }
}

connectButton.addEventListener('click', handleConnectButton);

// / **
//  * Connects the dongle via the computers COM port
//  * Prompts the user to choose port from dialog in chrome
//  * Enables the button to start the beacon
//  * /
const connect = async () => {

    // Connect to dongle
    await my_dongle.at_connect();

    isConnected = true;

    connectButton.textContent = 'Disconnect';
    output.textContent = 'Connected to dongle';

    // Enable the iBeacon button which is disabled by default to avoid errors
    iBeaconButton.addEventListener('click', handleIBeaconButton);
    iBeaconButton.classList.remove('disabled');
}

// / **
//  * Stops advertising and disconnects the dongle
//  * and disables the button to start the beacon
//  * /
const disconnect = async () => {

    // Stop advertising
    await my_dongle.at_advstop();

    // Disconnects the dongle
    await my_dongle.at_disconnect();

    // Reset dongle status
    isConnected = false;
    isAdvertising = false;

    output.textContent = 'Dongle disconnected';
    connectButton.textContent = 'Connect';

    // Disable the iBeacon button
    iBeaconButton.classList.add('disabled');
    iBeaconButton.removeEventListener('click', handleIBeaconButton);
}

// / **
//  * Calls the dongles advertise function (at_advdatai ())
//  * and provides a UUID as the data
//  * Please notice the "i" in the function .at_advdatai ()
//  * which is used when creating an iBeacon
//  * /
const handleIBeaconButton = async () => {
    // If the dongle is not advertising, start advertising the iBeacon
    if (!isAdvertising) {
        startAdvertising();
    } else {
        stopAdvertising();
    }
}

// / **
//  * Starts advertising
//  * /
const startAdvertising = async () => {

    // Sets the advertise data
    await my_dongle.at_advdatai(uuidInputField.value);

    // Start advertising
    await my_dongle.at_advstart();

    isAdvertising = true;

    output.textContent = 'iBeacon created';
    iBeaconButton.textContent = 'Stop the iBeacon';
}

// / **
//  * Stops advertising
//  * /
const stopAdvertising = async () => {
    // Stop the dongle from advertising
    await my_dongle.at_advstop();

    isAdvertising = false;

    output.textContent = 'iBeacon stopped';
    iBeaconButton.textContent = 'Create an iBeacon';
}
