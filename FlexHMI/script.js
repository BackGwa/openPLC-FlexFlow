const HOST = "broker.hivemq.com";
const PORT = 8000;
let mqtt;

function randint(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function on_connect() {
    console.log("FlexHMI - MQTT Connected!");
}

function on_failure() {
    console.log("FlexHMI - MQTT Connect Failure!");
}

function test_send() {
    msg = "TEST";
    message = new Paho.MQTT.Message(msg);
    message.destinationName = "flexflow/asm/rpi01";
    mqtt.send(message); 
}

function MQTT_connect() {
    console.log(`FlexHMI - ${HOST}:${PORT} Connecting...`);

    mqtt = new Paho.MQTT.Client(HOST, PORT, `flexhmi${randint(0, 65535)}`);
    
    let options = {
        timeout: 3,
        onSuccess: on_connect,
        onFailure: on_failure,
    }

    mqtt.connect(options);
}

document.addEventListener("DOMContentLoaded", MQTT_connect)