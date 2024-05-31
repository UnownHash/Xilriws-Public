import * as utils from "./utils.js"

const baseLanguages = [
    "en-US",
    "fr",
    "de",
    "es"
]

const extraLanguages = [
    "en-GB",
    "pt-BR",
    "ru",
    "tr",
    "de",
    "fr",
    "es",
    "hr",
    "el",
    "hu",
    "no",
    "ro",
    "sr"
]

const englishes = [
    "en-US",
    "en-GB"
]

export function block() {
    utils.overwriteProp(navigator, "platform", "Win32")

    // language
    const baseLanguage = utils.randomChoose(baseLanguages)
    const languages = [baseLanguage]

    const randomExtraLangs = utils.randomNumber(0, 10)
    if (randomExtraLangs > 3) {
        if (englishes.includes(baseLanguage)) {
            languages.push(utils.randomChoose(extraLanguages))
        } else {
            languages.push(utils.randomChoose(englishes))
        }
    }
    console.log("languages are " + languages.join(","))

    // TODO: seed Math.random using the tabId (or the url possibly) - the content script will be reloaded by the iframe. in some cases (like the language) this can be detcted by the script
    utils.overwriteProp(navigator, "language", baseLanguage)
    utils.overwriteProp(navigator, "languages", languages)
}