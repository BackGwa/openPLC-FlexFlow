const HOST = "broker.hivemq.com";
const PORT = 8000;
let mqtt;

function randint(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function on_connect() {
    console.log("FlexHMI - MQTT Connected!");
    subscribe();
}

function on_failure() {
    console.log("FlexHMI - MQTT Connect Failure!");
}

function on_message(message) {
    msg = message.payloadString;
    topic = message.destinationName.split("/");

    if (topic[3] == "INPUT") {
        query = "I";
    } else if (topic[3] == "OUTPUT") {
        query = "Q";
    } else if (topic[3] == "MEMORY") {
        query = "M";
    }

    query += topic[5];

    stat = document.querySelector(`#${query}`);
    lamp = stat.querySelector("item-lamp");

    if (msg == 1) {
        lamp.classList.add("focus");
    } else {
        lamp.classList.remove("focus");
    }
}

function subscribe() {
    mqtt.subscribe("flexflow/asm/rpi01/#");
    mqtt.onMessageArrived = on_message;
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