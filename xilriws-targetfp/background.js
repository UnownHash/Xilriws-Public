chrome.webNavigation.onCompleted.addListener((details) => {
    console.log(details.tabId)
})

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message === "getTabId") {
        sendResponse(sender.tab.id)
    }
    return true
})