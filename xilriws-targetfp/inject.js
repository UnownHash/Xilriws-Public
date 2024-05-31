(async () => {
    "use strict"

    const utils = await import("./utils.js")
    const screen = await import("./screen.js")
    const general = await import("./general.js")
    const canvas = await import("./canvas.js")

    const div = document.querySelector("[data-xil-tab-id]")
    const seed = div.getAttribute("data-xil-tab-id")
    document.body.removeChild(div)
    utils.setSeed(seed)

    screen.block()
    general.block()
    canvas.block()
})()



