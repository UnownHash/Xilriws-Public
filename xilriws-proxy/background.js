console.log("test")

const ws = new WebSocket('ws://localhost:9091');

let currentProxyCreds = {
    "username": null,
    "password": null
}

ws.onmessage = (event) => {
    console.log('Message from server: ', event.data);
    const data = JSON.parse(event.data)

    currentProxyCreds = {
        username: data.username,
        password: data.password
    }
    startProxy(data.host, data.port)
};

function startProxy(host, port) {
    const config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: host,
                port: port,
            },
            bypassList: ["localhost"],
        },
    };
    chrome.proxy.settings.set(
        {value: config, scope: "regular"},
        function () {
        },
    );
}

function callbackFn(details) {
    return {
        authCredentials: currentProxyCreds,
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ["blocking"],
);