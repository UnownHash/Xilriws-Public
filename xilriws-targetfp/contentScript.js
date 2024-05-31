(async () => {
    const tabId = await chrome.runtime.sendMessage("getTabId")
    const div = document.createElement("div")
    div.setAttribute("data-xil-tab-id", tabId)
    document.body.appendChild(div)
})()