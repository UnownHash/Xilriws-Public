import * as utils from "./utils.js"

const screenSizes = [
    [1680, 1050],
    [1776, 1000],
    [1600, 1200],
    [1600, 1280],
    [1920, 1080],
    [1440, 1440],
    [2048, 1080],
    [1920, 1200],
    [2048, 1152],
    [1792, 1344],
    [1920, 1280],
    [2280, 1080],
    [1856, 1392],
    [2400, 1080],
    [1800, 1440],
    [2880, 900],
    [2160, 1200],
    [2048, 1280],
    [1920, 1400],
    [2520, 1080],
    [2436, 1125],
    [2538, 1080],
    [1920, 1440],
    [2560, 1080],
    [2160, 1440],
    [2048, 1536],
    [2304, 1440],
    [2256, 1504],
    [2560, 1440],
    [2576, 1450],
    [2304, 1728],
    [2560, 1600],
    [2880, 1440],
    [2960, 1440],
    [2560, 1700],
    [2560, 1800],
    [2880, 1620],
    [2560, 1920],
    [3440, 1440],
    [2736, 1824],
    [2880, 1800],
    [2880, 1920],
    [2560, 2048],
    [2732, 2048]
]

export function block() {
    const [screenWidth, screenHeight] = utils.randomChoose(screenSizes)
    console.log("screen size is " + screenWidth + "x" + screenHeight)
    utils.overwriteProp(window.screen, "width", screenWidth)
    utils.overwriteProp(window.screen, "height", screenHeight)
    utils.overwriteProp(window.screen, "availWidth", screenWidth)
    utils.overwriteProp(window.screen, "availHeight", screenHeight - 48)
    utils.overwriteProp(window.screen, "availLeft", 0)
    utils.overwriteProp(window.screen, "availTop", 0)
    utils.overwriteProp(window.screen, "pixelDepth", 24)
    utils.overwriteProp(window.screen.orientation, "type", "landscape-primary")

    utils.overwriteProp(window, "outerWidth", screenWidth)
    utils.overwriteProp(window, "outerHeight", screenHeight)
    utils.overwriteProp(window, "innerWidth", screenWidth)
    utils.overwriteProp(window, "innerHeight", screenHeight - 86)
    utils.overwriteProp(window, "screenX", 0)
    utils.overwriteProp(window, "screenY", 0)
    utils.overwriteProp(window, "devicePixelRatio", 1)
}