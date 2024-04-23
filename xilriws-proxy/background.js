const ws = new WebSocket('ws://127.0.0.1:9091');

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
}

function sendWs(action, detail) {
    ws.send(JSON.stringify({action: action, detail: detail}))
}

function startProxy(host, port) {
    const proxyConfig = {
        mode: "system",
        rules: {
            proxyForHttps: {
                scheme: "http",
                host: host,
                port: port,
            },
            bypassList: ["localhost"],
        },
    };
    chrome.proxy.settings.set(
        {value: proxyConfig},
        () => {
            sendWs('finish:proxy', host + ':' + port)
        },
    )
}

chrome.webRequest.onAuthRequired.addListener(
    () => {
        return {
            authCredentials: currentProxyCreds
        }
    },
    {urls: ["<all_urls>"]},
    ["blocking"],
)

chrome.tabs.onRemoved.addListener(
    () => {
        chrome.storage.local.clear(() => console.log('deleted local storage'))
        chrome.cookies.getAll({}, cookies => {
                console.log('Deleting ' + cookies.length + ' cookies')
                let goal = cookies.length

                function deleteCallback() {
                    goal -= 1

                    if (goal <= 0) {
                        console.log('Deleted all cookies')
                        sendWs('finish:cookiePurge', null)
                    }
                }

                cookies.forEach(cookie => chrome.cookies.remove({
                    name: cookie.name,
                    url: `${cookie.secure ? 'https' : 'http'}://${cookie.domain}${cookie.path}`,
                    storeId: cookie.storeId
                }, deleteCallback))
            }
        )
    }
)
