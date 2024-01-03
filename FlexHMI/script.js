const HOST = "broker.hivemq.com";
const PORT = 8000;
let mqtt;

function randint(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function on_connect() {
    debug("FlexHMI - MQTT Connected!");
    subscribe();
}

function on_failure() {
    debug("FlexHMI - MQTT Connect Failure!");
}

function on_message(message) {
    msg = message.payloadString;
    topic = message.destinationName.split("/");
    debug("FlexHMI - MQTT Message")
    debug(`TOPIC : ${message.destinationName}`);
    debug(`MESSAGE : ${message.payloadString}`);

    if (topic[3] == "INPUT") {
        query = "I";
    } else if (topic[3] == "OUTPUT") {
        query = "Q";
    } else if (topic[3] == "MEMORY") {
        query = "M";
    }

    query += topic[5];

    if (topic[4] == "BOOL") {
        stat = document.querySelector(`#${query}`);
        lamp = stat.querySelector("item-lamp");
    
        if (msg == 1) {
            lamp.classList.add("focus");
        } else {
            lamp.classList.remove("focus");
        }
    } else if (topic[4] == "INT") {
        stat = document.querySelector(`.${query}`);
        counter = stat.querySelector("counter-int");
        counter.innerText = msg;
    }
}

function subscribe() {
    mqtt.subscribe("flexflow/asm/rpi01/#");
    debug(`FlexHMI - subscribe : flexflow/asm/rpi01/#`);
    mqtt.onMessageArrived = on_message;
}

function MQTT_connect() {
    debug(`FlexHMI - ${HOST}:${PORT} Connecting...`);

    mqtt = new Paho.MQTT.Client(HOST, PORT, `flexhmi${randint(0, 65535)}`);
    
    let options = {
        timeout: 3,
        onSuccess: on_connect,
        onFailure: on_failure,
    }

    mqtt.connect(options);
}

function debug(message) {
    document.querySelector("debug-message").innerHTML += message + "<br>";
    document.querySelector("debug-message").scrollTop =  document.querySelector("debug-message").scrollHeight;
}

document.addEventListener("DOMContentLoaded", MQTT_connect)