const hprose = require("hprose");
const ip = require("ip");

function ping() {
    return ip.address();
}

const server = hprose.Server.create("http://0.0.0.0:8080");
server.addFunction(ping);
server.start();