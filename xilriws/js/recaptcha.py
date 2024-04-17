SRC = """
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var ReCaptchaInstance = (function () {
    function ReCaptchaInstance(siteKey, recaptchaID, recaptcha) {
        this.siteKey = siteKey;
        this.recaptchaID = recaptchaID;
        this.recaptcha = recaptcha;
        this.styleContainer = null;
    }
    ReCaptchaInstance.prototype.execute = function (action) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2, this.recaptcha.enterprise.execute(this.recaptchaID, { action: action })];
            });
        });
    };
    ReCaptchaInstance.prototype.getSiteKey = function () {
        return this.siteKey;
    };
    ReCaptchaInstance.prototype.hideBadge = function () {
        if (this.styleContainer !== null) {
            return;
        }
        this.styleContainer = document.createElement('style');
        this.styleContainer.innerHTML = '.grecaptcha-badge{display:none !important;}';
        document.head.appendChild(this.styleContainer);
    };
    ReCaptchaInstance.prototype.showBadge = function () {
        if (this.styleContainer === null) {
            return;
        }
        document.head.removeChild(this.styleContainer);
        this.styleContainer = null;
    };
    return ReCaptchaInstance;
}());

//////////


var ELoadingState;
(function (ELoadingState) {
    ELoadingState[ELoadingState["NOT_LOADED"] = 0] = "NOT_LOADED";
    ELoadingState[ELoadingState["LOADING"] = 1] = "LOADING";
    ELoadingState[ELoadingState["LOADED"] = 2] = "LOADED";
})(ELoadingState || (ELoadingState = {}));
var ReCaptchaLoader = (function () {
    function ReCaptchaLoader() {
    }
    ReCaptchaLoader.load = function (siteKey, options) {
        if (options === void 0) { options = {}; }
        if (typeof document === 'undefined') {
            return Promise.reject(new Error('This is a library for the browser!'));
        }
        if (ReCaptchaLoader.getLoadingState() === ELoadingState.LOADED) {
            if (ReCaptchaLoader.instance.getSiteKey() === siteKey) {
                return Promise.resolve(ReCaptchaLoader.instance);
            }
            else {
                return Promise.reject(new Error('reCAPTCHA already loaded with different site key!'));
            }
        }
        if (ReCaptchaLoader.getLoadingState() === ELoadingState.LOADING) {
            if (siteKey !== ReCaptchaLoader.instanceSiteKey) {
                return Promise.reject(new Error('reCAPTCHA already loaded with different site key!'));
            }
            return new Promise(function (resolve, reject) {
                ReCaptchaLoader.successfulLoadingConsumers.push(function (instance) { return resolve(instance); });
                ReCaptchaLoader.errorLoadingRunnable.push(function (reason) { return reject(reason); });
            });
        }
        ReCaptchaLoader.instanceSiteKey = siteKey;
        ReCaptchaLoader.setLoadingState(ELoadingState.LOADING);
        var loader = new ReCaptchaLoader();
        return new Promise(function (resolve, reject) {
            loader.loadScript(siteKey, options.useRecaptchaNet || false, options.renderParameters ? options.renderParameters : {}, options.customUrl).then(function () {
                ReCaptchaLoader.setLoadingState(ELoadingState.LOADED);
                // var widgetID = loader.doExplicitRender(grecaptcha, siteKey, options.explicitRenderParameters ? options.explicitRenderParameters : {});
                var instance = new ReCaptchaInstance(siteKey, 0, grecaptcha);
                ReCaptchaLoader.successfulLoadingConsumers.forEach(function (v) { return v(instance); });
                ReCaptchaLoader.successfulLoadingConsumers = [];
                if (options.autoHideBadge) {
                    instance.hideBadge();
                }
                ReCaptchaLoader.instance = instance;
                resolve(instance);
            }).catch(function (error) {
                ReCaptchaLoader.errorLoadingRunnable.forEach(function (v) { return v(error); });
                ReCaptchaLoader.errorLoadingRunnable = [];
                reject(error);
            });
        });
    };
    ReCaptchaLoader.getInstance = function () {
        return ReCaptchaLoader.instance;
    };
    ReCaptchaLoader.setLoadingState = function (state) {
        ReCaptchaLoader.loadingState = state;
    };
    ReCaptchaLoader.getLoadingState = function () {
        if (ReCaptchaLoader.loadingState === null) {
            return ELoadingState.NOT_LOADED;
        }
        else {
            return ReCaptchaLoader.loadingState;
        }
    };
    ReCaptchaLoader.prototype.loadScript = function (siteKey, useRecaptchaNet, renderParameters, customUrl) {
        var _this = this;
        if (useRecaptchaNet === void 0) { useRecaptchaNet = false; }
        if (renderParameters === void 0) { renderParameters = {}; }
        if (customUrl === void 0) { customUrl = ''; }
        var scriptElement = document.createElement('script');
        scriptElement.setAttribute('recaptcha-v3-enterprise-script', '');
        var scriptBase = 'https://www.google.com/recaptcha/enterprise.js';
        if (useRecaptchaNet) {
            scriptBase = 'https://recaptcha.net/recaptcha/enterprise.js';
        }
        if (customUrl) {
            scriptBase = customUrl;
        }
        if (renderParameters.render) {
            renderParameters.render = undefined;
        }
        var parametersQuery = this.buildQueryString(renderParameters);
        scriptElement.src = scriptBase + '?render=explicit' + parametersQuery;
        return new Promise(function (resolve, reject) {
            scriptElement.addEventListener('load', _this.waitForScriptToLoad(function () {
                resolve(scriptElement);
            }), false);
            scriptElement.onerror = function (error) {
                ReCaptchaLoader.setLoadingState(ELoadingState.NOT_LOADED);
                reject(error);
            };
            document.head.appendChild(scriptElement);
        });
    };
    ReCaptchaLoader.prototype.buildQueryString = function (parameters) {
        var parameterKeys = Object.keys(parameters);
        if (parameterKeys.length < 1) {
            return '';
        }
        return '&' + Object.keys(parameters)
            .filter(function (parameterKey) {
            return !!parameters[parameterKey];
        })
            .map(function (parameterKey) {
            return parameterKey + '=' + parameters[parameterKey];
        }).join('&');
    };
    ReCaptchaLoader.prototype.waitForScriptToLoad = function (callback) {
        var _this = this;
        return function () {
            if (window.grecaptcha === undefined) {
                setTimeout(function () {
                    _this.waitForScriptToLoad(callback);
                }, ReCaptchaLoader.SCRIPT_LOAD_DELAY);
            }
            else {
                window.grecaptcha.enterprise.ready(function () {
                    callback();
                });
            }
        };
    };
    ReCaptchaLoader.prototype.doExplicitRender = function (grecaptcha, siteKey, parameters) {
        var augmentedParameters = {
            sitekey: siteKey,
            badge: parameters.badge,
            size: parameters.size,
            tabindex: parameters.tabindex
        };
        if (parameters.container) {
            return grecaptcha.enterprise.render(parameters.container, augmentedParameters);
        }
        else {
            return grecaptcha.enterprise.render(augmentedParameters);
        }
    };
    ReCaptchaLoader.loadingState = null;
    ReCaptchaLoader.instance = null;
    ReCaptchaLoader.instanceSiteKey = null;
    ReCaptchaLoader.successfulLoadingConsumers = [];
    ReCaptchaLoader.errorLoadingRunnable = [];
    ReCaptchaLoader.SCRIPT_LOAD_DELAY = 25;
    return ReCaptchaLoader;
}());
"""