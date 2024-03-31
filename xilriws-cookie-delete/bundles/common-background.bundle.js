/*! For license information please see common-background.bundle.js.LICENSE.txt */
"use strict";
(self.webpackChunkcookie_autodelete = self.webpackChunkcookie_autodelete || []).push([[287], {
    6441: (e, t, n) => {
        function a(e) {
            return function (t) {
                var n = t.dispatch, a = t.getState;
                return function (t) {
                    return function (o) {
                        return "function" == typeof o ? o(n, a, e) : t(o)
                    }
                }
            }
        }

        n.r(t), n.d(t, {default: () => i});
        var o = a();
        o.withExtraArgument = a;
        const i = o
    }, 9805: (e, t, n) => {
        function a(e) {
            return a = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
                return typeof e
            } : function (e) {
                return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
            }, a(e)
        }

        function o(e, t, n) {
            return (t = function (e) {
                var t = function (e, t) {
                    if ("object" !== a(e) || null === e) return e;
                    var n = e[Symbol.toPrimitive];
                    if (void 0 !== n) {
                        var o = n.call(e, "string");
                        if ("object" !== a(o)) return o;
                        throw new TypeError("@@toPrimitive must return a primitive value.")
                    }
                    return String(e)
                }(e);
                return "symbol" === a(t) ? t : String(t)
            }(t)) in e ? Object.defineProperty(e, t, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0
            }) : e[t] = n, e
        }

        function i(e, t) {
            var n = Object.keys(e);
            if (Object.getOwnPropertySymbols) {
                var a = Object.getOwnPropertySymbols(e);
                t && (a = a.filter((function (t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable
                }))), n.push.apply(n, a)
            }
            return n
        }

        function r(e) {
            for (var t = 1; t < arguments.length; t++) {
                var n = null != arguments[t] ? arguments[t] : {};
                t % 2 ? i(Object(n), !0).forEach((function (t) {
                    o(e, t, n[t])
                })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : i(Object(n)).forEach((function (t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(n, t))
                }))
            }
            return e
        }

        function s(e) {
            return "Minified Redux error #" + e + "; visit https://redux.js.org/Errors?code=" + e + " for the full message or use the non-minified dev environment for full errors. "
        }

        n.r(t), n.d(t, {
            __DO_NOT_USE__ActionTypes: () => l,
            applyMiddleware: () => S,
            bindActionCreators: () => f,
            combineReducers: () => E,
            compose: () => m,
            createStore: () => g,
            legacy_createStore: () => p
        });
        var d = "function" == typeof Symbol && Symbol.observable || "@@observable", c = function () {
            return Math.random().toString(36).substring(7).split("").join(".")
        }, l = {
            INIT: "@@redux/INIT" + c(), REPLACE: "@@redux/REPLACE" + c(), PROBE_UNKNOWN_ACTION: function () {
                return "@@redux/PROBE_UNKNOWN_ACTION" + c()
            }
        };

        function u(e) {
            if ("object" != typeof e || null === e) return !1;
            for (var t = e; null !== Object.getPrototypeOf(t);) t = Object.getPrototypeOf(t);
            return Object.getPrototypeOf(e) === t
        }

        function g(e, t, n) {
            var a;
            if ("function" == typeof t && "function" == typeof n || "function" == typeof n && "function" == typeof arguments[3]) throw new Error(s(0));
            if ("function" == typeof t && void 0 === n && (n = t, t = void 0), void 0 !== n) {
                if ("function" != typeof n) throw new Error(s(1));
                return n(g)(e, t)
            }
            if ("function" != typeof e) throw new Error(s(2));
            var o = e, i = t, r = [], c = r, p = !1;

            function E() {
                c === r && (c = r.slice())
            }

            function I() {
                if (p) throw new Error(s(3));
                return i
            }

            function f(e) {
                if ("function" != typeof e) throw new Error(s(4));
                if (p) throw new Error(s(5));
                var t = !0;
                return E(), c.push(e), function () {
                    if (t) {
                        if (p) throw new Error(s(6));
                        t = !1, E();
                        var n = c.indexOf(e);
                        c.splice(n, 1), r = null
                    }
                }
            }

            function m(e) {
                if (!u(e)) throw new Error(s(7));
                if (void 0 === e.type) throw new Error(s(8));
                if (p) throw new Error(s(9));
                try {
                    p = !0, i = o(i, e)
                } finally {
                    p = !1
                }
                for (var t = r = c, n = 0; n < t.length; n++) (0, t[n])();
                return e
            }

            function S(e) {
                if ("function" != typeof e) throw new Error(s(10));
                o = e, m({type: l.REPLACE})
            }

            function D() {
                var e, t = f;
                return (e = {
                    subscribe: function (e) {
                        if ("object" != typeof e || null === e) throw new Error(s(11));

                        function n() {
                            e.next && e.next(I())
                        }

                        return n(), {unsubscribe: t(n)}
                    }
                })[d] = function () {
                    return this
                }, e
            }

            return m({type: l.INIT}), (a = {dispatch: m, subscribe: f, getState: I, replaceReducer: S})[d] = D, a
        }

        var p = g;

        function E(e) {
            for (var t = Object.keys(e), n = {}, a = 0; a < t.length; a++) {
                var o = t[a];
                "function" == typeof e[o] && (n[o] = e[o])
            }
            var i, r = Object.keys(n);
            try {
                !function (e) {
                    Object.keys(e).forEach((function (t) {
                        var n = e[t];
                        if (void 0 === n(void 0, {type: l.INIT})) throw new Error(s(12));
                        if (void 0 === n(void 0, {type: l.PROBE_UNKNOWN_ACTION()})) throw new Error(s(13))
                    }))
                }(n)
            } catch (e) {
                i = e
            }
            return function (e, t) {
                if (void 0 === e && (e = {}), i) throw i;
                for (var a = !1, o = {}, d = 0; d < r.length; d++) {
                    var c = r[d], l = n[c], u = e[c], g = l(u, t);
                    if (void 0 === g) throw t && t.type, new Error(s(14));
                    o[c] = g, a = a || g !== u
                }
                return (a = a || r.length !== Object.keys(e).length) ? o : e
            }
        }

        function I(e, t) {
            return function () {
                return t(e.apply(this, arguments))
            }
        }

        function f(e, t) {
            if ("function" == typeof e) return I(e, t);
            if ("object" != typeof e || null === e) throw new Error(s(16));
            var n = {};
            for (var a in e) {
                var o = e[a];
                "function" == typeof o && (n[a] = I(o, t))
            }
            return n
        }

        function m() {
            for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++) t[n] = arguments[n];
            return 0 === t.length ? function (e) {
                return e
            } : 1 === t.length ? t[0] : t.reduce((function (e, t) {
                return function () {
                    return e(t.apply(void 0, arguments))
                }
            }))
        }

        function S() {
            for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++) t[n] = arguments[n];
            return function (e) {
                return function () {
                    var n = e.apply(void 0, arguments), a = function () {
                        throw new Error(s(15))
                    }, o = {
                        getState: n.getState, dispatch: function () {
                            return a.apply(void 0, arguments)
                        }
                    }, i = t.map((function (e) {
                        return e(o)
                    }));
                    return a = m.apply(void 0, i)(n.dispatch), r(r({}, n), {}, {dispatch: a})
                }
            }
        }
    }, 8136: (e, t, n) => {
        const a = n(3940), o = n(4719), i = a.__importDefault(n(6595)), r = n(3185), s = a.__importDefault(n(9659)),
            d = a.__importDefault(n(7583)), c = n(292), l = a.__importDefault(n(210)), u = a.__importDefault(n(8661)),
            g = a.__importDefault(n(2863)), p = a.__importDefault(n(3112));
        let E, I = !1;
        const f = () => {
            I || (I = !0, setTimeout((() => (I = !1, browser.storage.local.set({state: JSON.stringify(E.getState())}))), 1e3))
        }, m = [];

        function S(e) {
            return a.__awaiter(this, void 0, void 0, (function* () {
                const t = (0, c.extractMainDomain)(e.cookie.domain);
                m.forEach((n => {
                    if (!n.name) return;
                    if (!n.name.startsWith("popupCAD_")) return;
                    const a = n.name.slice(9).split(",");
                    (a[0].endsWith(e.cookie.domain) || a[0].endsWith(t)) && n.postMessage({cookieUpdated: !0})
                }))
            }))
        }

        browser.runtime.onConnect.addListener((function (e) {
            e.name && e.name.startsWith("popupCAD_") && ((0, c.eventListenerActions)(browser.cookies.onChanged, S, "ADD"), e.onMessage.addListener((e => {
                (0, c.cadLog)({
                    msg: "Received unexpected message from CAD Popup",
                    type: "warn",
                    x: JSON.stringify(e)
                }, !0)
            })), e.onDisconnect.addListener((e => {
                if (m.length - 1 == 0 && (0, c.eventListenerActions)(browser.cookies.onChanged, S, "REMOVE"), !e.name) return;
                const t = m.findIndex((t => !!t.name && t.name === e.name));
                -1 !== t && m.splice(t, 1)
            })), e.postMessage({cookieUpdated: !0}), m.push(e))
        })), a.__awaiter(void 0, void 0, void 0, (function* () {
            const e = browser.runtime.getManifest();
            browser.browserAction.setTitle({title: `${e.name} ${e.version} [STARTING UP...] (0)`});
            const t = yield browser.storage.local.get();
            let n;
            try {
                n = t.state ? JSON.parse(t.state) : {}
            } catch (e) {
                n = {}
            }
            if (E = (0, i.default)(n), E.dispatch({type: "ON_STARTUP"}), "Firefox" === browserDetect()) {
                const e = yield browser.runtime.getBrowserInfo(), t = Number.parseInt(e.version);
                E.dispatch({
                    payload: {key: "browserVersion", value: t},
                    type: "ADD_CACHE"
                }), E.dispatch({payload: {key: "browserInfo", value: e}, type: "ADD_CACHE"})
            }
            E.dispatch({payload: {key: "browserDetect", value: browserDetect()}, type: "ADD_CACHE"});
            const a = yield browser.runtime.getPlatformInfo();
            E.dispatch({
                payload: {key: "platformInfo", value: a},
                type: "ADD_CACHE"
            }), E.dispatch({
                payload: {key: "platformOs", value: a.os},
                type: "ADD_CACHE"
            }), l.default.init(E), p.default.init(), E.subscribe(p.default.onSettingsChange), E.subscribe(f), E.dispatch((0, o.validateSettings)()), yield(0, r.setGlobalIcon)((0, c.getSetting)(E.getState(), "activeMode")), yield(0, r.checkIfProtected)(E.getState()), browser.tabs.onUpdated.addListener(u.default.onDomainChange), browser.tabs.onUpdated.addListener(u.default.onTabDiscarded), browser.tabs.onUpdated.addListener(u.default.onTabUpdate), browser.tabs.onRemoved.addListener(u.default.onDomainChangeRemove), browser.tabs.onRemoved.addListener(u.default.cleanFromTabEvents), browser.cookies.onChanged.addListener(d.default.onCookieChanged), browser.contextMenus && s.default.menuInit(), browser.contextualIdentities && (yield g.default.init()), browser.browserAction.setTitle({title: `${e.name} ${e.version} [READY] (0)`})
        })).then((() => {
            (0, c.cadLog)({
                msg: "background.onStartUp has been executed",
                type: "info"
            }, (0, c.getSetting)(E.getState(), "debugMode"))
        })), browser.runtime.onStartup.addListener((() => a.__awaiter(void 0, void 0, void 0, (function* () {
            if (yield D(), !0 === (0, c.getSetting)(E.getState(), "activeMode")) if (!0 === (0, c.getSetting)(E.getState(), "enableGreyListCleanup")) {
                let e = !1;
                (yield browser.tabs.query({windowType: "normal"})).forEach((t => {
                    "about:sessionrestore" === t.url && (e = !0)
                })), e ? (0, c.cadLog)({
                    msg: "Found a tab with [ about:sessionrestore ] in Firefox. Skipping Grey startup cleanup this time.",
                    type: "info"
                }, !0 === (0, c.getSetting)(E.getState(), "debugMode")) : _()
            } else (0, c.cadLog)({
                msg: "GreyList Cleanup setting is disabled.  Not cleaning cookies on startup.",
                type: "info"
            }, !0 === (0, c.getSetting)(E.getState(), "debugMode"));
            yield(0, r.checkIfProtected)(E.getState())
        })))), browser.runtime.onInstalled.addListener((e => a.__awaiter(void 0, void 0, void 0, (function* () {
            switch (yield D(), yield(0, r.checkIfProtected)(E.getState()), e.reason) {
                case"update":
                    if (E.dispatch((0, o.validateSettings)()), (0, c.convertVersionToNumber)(e.previousVersion) < 350) {
                        E.getState().settings.localstorageCleanup && E.dispatch({
                            payload: {
                                name: "localStorageCleanup",
                                value: E.getState().settings.localstorageCleanup.value
                            }, type: "UPDATE_SETTING"
                        }), Object.values(E.getState().lists).forEach((e => {
                            e.forEach((e => {
                                e.cleanLocalStorage && !e.cleanSiteData && E.dispatch({
                                    payload: Object.assign(Object.assign({}, e), {cleanSiteData: ["LocalStorage"]}),
                                    type: "UPDATE_EXPRESSION"
                                })
                            }))
                        }));
                        for (const e of ["GREY", "WHITE"]) if ((0, c.getSetting)(E.getState(), `${e.toLowerCase()}CleanLocalstorage`)) {
                            const t = new Set(Object.keys(E.getState().lists));
                            t.add("default"), (0, c.getSetting)(E.getState(), "contextualIdentities") && (yield browser.contextualIdentities.query({})).forEach((e => t.add(e.cookieStoreId))), t.forEach((t => {
                                E.dispatch({
                                    payload: {
                                        expression: `_Default:${e}`,
                                        cleanSiteData: ["LocalStorage"],
                                        listType: e,
                                        storeId: t
                                    }, type: "ADD_EXPRESSION"
                                })
                            }))
                        }
                    }
                    (0, c.convertVersionToNumber)(e.previousVersion) < 300 && E.dispatch({type: "RESET_COOKIE_DELETED_COUNTER"}), (0, c.getSetting)(E.getState(), "enableNewVersionPopup") && (yield browser.runtime.openOptionsPage())
            }
        }))));
        const D = () => a.__awaiter(void 0, void 0, void 0, (function* () {
            for (; !E;) yield(0, c.sleep)(250)
        })), _ = () => {
            (0, c.getSetting)(E.getState(), "activeMode") && ((0, c.cadLog)({msg: "background.greyCleanup:  dispatching browser restart greyCleanup."}, (0, c.getSetting)(E.getState(), "debugMode")), E.dispatch((0, o.cookieCleanup)({
                greyCleanup: !0,
                ignoreOpenTabs: (0, c.getSetting)(E.getState(), "cleanCookiesFromOpenTabsOnStartup")
            })))
        }
    }, 1764: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0}), t.cache = t.activityLog = t.cookieDeletedCounterSession = t.cookieDeletedCounterTotal = t.settings = t.lists = t.expressions = t.expression = void 0;
        const a = n(3940), o = n(9805), i = a.__importDefault(n(3987)), r = n(3555),
            s = (e, t) => Object.assign(Object.assign({}, t.payload), {
                cookieNames: t.payload.cookieNames ? t.payload.cookieNames : [],
                cleanSiteData: t.payload.cleanSiteData ? t.payload.cleanSiteData : [],
                id: i.default.generate(),
                listType: t.payload.listType ? t.payload.listType : "WHITE"
            }),
            d = (e, t) => "WHITE" === e.listType && "GREY" === t.listType ? -1 : "WHITE" === t.listType && "GREY" === e.listType ? 1 : e.expression.localeCompare(t.expression);
        t.expression = (e = {
            cookieNames: [],
            expression: "",
            id: "1",
            listType: "WHITE",
            storeId: "default"
        }, t) => "UPDATE_EXPRESSION" === t.type && e.id === t.payload.id ? s(0, t) : e, t.expressions = (e = [], n) => {
            switch (n.type) {
                case"ADD_EXPRESSION":
                    return ((e, t) => e.some((e => e.expression === t.payload.expression)))(e, n) ? e : [...e, s(0, n)].sort(d);
                case"UPDATE_EXPRESSION":
                    return e.map((e => (0, t.expression)(e, n))).sort(d);
                case"REMOVE_EXPRESSION":
                    return e.filter((e => e.id !== n.payload.id));
                case"RESET_ALL":
                    return [];
                default:
                    return e
            }
        }, t.lists = (e = {}, n) => {
            switch (n.type) {
                case"ADD_EXPRESSION":
                case"REMOVE_EXPRESSION":
                case"UPDATE_EXPRESSION": {
                    const a = Object.assign({}, e);
                    return a[n.payload.storeId] = (0, t.expressions)(e[n.payload.storeId], n), 0 === a[n.payload.storeId].length && delete a[n.payload.storeId], a
                }
                case"REMOVE_LIST": {
                    const t = Object.assign({}, e);
                    return delete t[n.payload.toString()], t
                }
                case"CLEAR_EXPRESSIONS":
                case"RESET_ALL":
                    return {};
                default:
                    return e
            }
        }, t.settings = (e = r.initialState.settings, t) => {
            switch (t.type) {
                case"UPDATE_SETTING": {
                    const n = Object.assign({}, e);
                    return n[t.payload.name] = Object.assign({}, t.payload), n
                }
                case"RESET_ALL":
                case"RESET_SETTINGS":
                    return r.initialState.settings;
                default:
                    return e
            }
        }, t.cookieDeletedCounterTotal = (e = 0, t) => {
            switch (t.type) {
                case"INCREMENT_COOKIE_DELETED_COUNTER":
                    return e + (void 0 === t.payload ? 1 : t.payload);
                case"RESET_ALL":
                case"RESET_COOKIE_DELETED_COUNTER":
                    return 0;
                default:
                    return e
            }
        }, t.cookieDeletedCounterSession = (e = 0, t) => {
            switch (t.type) {
                case"INCREMENT_COOKIE_DELETED_COUNTER":
                    return e + (void 0 === t.payload ? 1 : t.payload);
                case"RESET_ALL":
                case"ON_STARTUP":
                case"RESET_COOKIE_DELETED_COUNTER":
                    return 0;
                default:
                    return e
            }
        }, t.activityLog = (e = [], t) => {
            switch (t.type) {
                case"ADD_ACTIVITY_LOG":
                    return Object.keys(t.payload.storeIds).length > 0 || t.payload.siteDataCleaned ? [t.payload, ...e].slice(0, 10) : e;
                case"REMOVE_ACTIVITY_LOG":
                    return e.filter((e => e.dateTime !== t.payload.dateTime));
                case"RESET_ALL":
                case"CLEAR_ACTIVITY_LOG":
                    return [];
                default:
                    return e
            }
        }, t.cache = (e = {}, t) => {
            switch (t.type) {
                case"ADD_CACHE": {
                    const n = Object.assign({}, e);
                    return n[`${t.payload.key}`] = t.payload.value, n
                }
                case"RESET_ALL":
                    return {};
                default:
                    return e
            }
        }, t.default = (0, o.combineReducers)({
            activityLog: t.activityLog,
            cache: t.cache,
            cookieDeletedCounterSession: t.cookieDeletedCounterSession,
            cookieDeletedCounterTotal: t.cookieDeletedCounterTotal,
            lists: t.lists,
            settings: t.settings
        })
    }, 6595: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0});
        const a = n(3940), o = n(9805), i = a.__importDefault(n(6441)), r = n(9477), s = n(4719),
            d = a.__importDefault(n(1764)), c = e => e => t => e(t), l = {
                ADD_EXPRESSION: s.addExpression,
                CLEAR_ACTIVITY_LOG: s.clearActivities,
                CLEAR_EXPRESSIONS: s.clearExpressions,
                COOKIE_CLEANUP: s.cookieCleanup,
                REMOVE_ACTIVITY_LOG: s.removeActivity,
                REMOVE_EXPRESSION: s.removeExpression,
                REMOVE_LIST: s.removeList,
                RESET_ALL: s.resetAll,
                RESET_COOKIE_DELETED_COUNTER: s.resetCookieDeletedCounter,
                RESET_SETTINGS: s.resetSettings,
                UPDATE_EXPRESSION: s.updateExpression,
                UPDATE_SETTING: s.updateSetting
            };
        t.default = (e = {}) => (0, r.createBackgroundStore)({
            actions: l,
            store: (0, o.createStore)(d.default, e, (0, o.applyMiddleware)(i.default, c))
        })
    }, 406: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0});
        const a = n(3940), o = n(4719), i = n(292), r = a.__importDefault(n(210));

        class s extends r.default {
        }

        t.default = s, s.createActiveModeAlarm = () => a.__awaiter(void 0, void 0, void 0, (function* () {
            const e = parseInt((0, i.getSetting)(r.default.store.getState(), "delayBeforeClean"), 10),
                t = 1e3 * (e > 0 ? e : .5);
            s.alarmFlag || (s.alarmFlag = !0, yield(0, i.sleep)(t), (0, i.getSetting)(r.default.store.getState(), "activeMode") && r.default.store.dispatch((0, o.cookieCleanup)({
                greyCleanup: !1,
                ignoreOpenTabs: !1
            })), s.alarmFlag = !1)
        })), s.alarmFlag = !1
    }, 9659: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0});
        const a = n(3940), o = n(4719), i = n(7459), r = n(292), s = a.__importDefault(n(210));

        class d extends s.default {
            static menuInit() {
                browser.contextMenus && (0, r.getSetting)(s.default.store.getState(), "contextMenus") && (d.isInitialized || (d.isInitialized = !0, d.menuCreate({
                    id: d.MenuID.PARENT_CLEAN,
                    title: browser.i18n.getMessage("contextMenusParentClean")
                }), d.menuCreate({
                    id: d.MenuID.CLEAN,
                    parentId: d.MenuID.PARENT_CLEAN,
                    title: browser.i18n.getMessage("cleanText")
                }), d.menuCreate({
                    id: d.MenuID.CLEAN_OPEN,
                    parentId: d.MenuID.PARENT_CLEAN,
                    title: browser.i18n.getMessage("cleanIgnoringOpenTabsText")
                }), d.menuCreate({parentId: d.MenuID.PARENT_CLEAN, type: "separator"}), d.menuCreate({
                    enabled: !1,
                    parentId: d.MenuID.PARENT_CLEAN,
                    title: browser.i18n.getMessage("cleanupActionsBypass")
                }), [...r.SITEDATATYPES, "All", "Cookies"].sort().forEach((e => {
                    d.menuCreate({
                        id: `${d.MenuID.MANUAL_CLEAN_SITEDATA}${e}`,
                        parentId: d.MenuID.PARENT_CLEAN,
                        title: browser.i18n.getMessage(`manualCleanSiteData${e}`)
                    })
                })), d.menuCreate({type: "separator"}), d.menuCreate({
                    contexts: ["link", "page", "selection"],
                    id: d.MenuID.PARENT_EXPRESSION,
                    title: browser.i18n.getMessage("contextMenusParentExpression")
                }), d.menuCreate({
                    contexts: ["link"],
                    id: d.MenuID.PARENT_LINK_DOMAIN,
                    parentId: d.MenuID.PARENT_EXPRESSION,
                    title: browser.i18n.getMessage("contextMenusSelectedDomainLink")
                }), d.menuCreate({
                    contexts: ["link"],
                    id: d.MenuID.LINK_ADD_GREY_DOMAIN,
                    parentId: d.MenuID.PARENT_LINK_DOMAIN,
                    title: browser.i18n.getMessage("toGreyListText")
                }), d.menuCreate({
                    contexts: ["link"],
                    id: d.MenuID.LINK_ADD_WHITE_DOMAIN,
                    parentId: d.MenuID.PARENT_LINK_DOMAIN,
                    title: browser.i18n.getMessage("toWhiteListText")
                }), d.menuCreate({
                    contexts: ["link"],
                    id: d.MenuID.PARENT_LINK_SUBS,
                    parentId: d.MenuID.PARENT_EXPRESSION,
                    title: browser.i18n.getMessage("contextMenusSelectedSubdomainLink")
                }), d.menuCreate({
                    contexts: ["link"],
                    id: d.MenuID.LINK_ADD_GREY_SUBS,
                    parentId: d.MenuID.PARENT_LINK_SUBS,
                    title: browser.i18n.getMessage("toGreyListText")
                }), d.menuCreate({
                    contexts: ["link"],
                    id: d.MenuID.LINK_ADD_WHITE_SUBS,
                    parentId: d.MenuID.PARENT_LINK_SUBS,
                    title: browser.i18n.getMessage("toWhiteListText")
                }), d.menuCreate({
                    contexts: ["page"],
                    id: d.MenuID.PARENT_PAGE_DOMAIN,
                    parentId: d.MenuID.PARENT_EXPRESSION,
                    title: browser.i18n.getMessage("contextMenusSelectedDomainPage")
                }), d.menuCreate({
                    contexts: ["page"],
                    id: d.MenuID.PAGE_ADD_GREY_DOMAIN,
                    parentId: d.MenuID.PARENT_PAGE_DOMAIN,
                    title: browser.i18n.getMessage("toGreyListText")
                }), d.menuCreate({
                    contexts: ["page"],
                    id: d.MenuID.PAGE_ADD_WHITE_DOMAIN,
                    parentId: d.MenuID.PARENT_PAGE_DOMAIN,
                    title: browser.i18n.getMessage("toWhiteListText")
                }), d.menuCreate({
                    contexts: ["page"],
                    id: d.MenuID.PARENT_PAGE_SUBS,
                    parentId: d.MenuID.PARENT_EXPRESSION,
                    title: browser.i18n.getMessage("contextMenusSelectedSubdomainPage")
                }), d.menuCreate({
                    contexts: ["page"],
                    id: d.MenuID.PAGE_ADD_GREY_SUBS,
                    parentId: d.MenuID.PARENT_PAGE_SUBS,
                    title: browser.i18n.getMessage("toGreyListText")
                }), d.menuCreate({
                    contexts: ["page"],
                    id: d.MenuID.PAGE_ADD_WHITE_SUBS,
                    parentId: d.MenuID.PARENT_PAGE_SUBS,
                    title: browser.i18n.getMessage("toWhiteListText")
                }), d.menuCreate({
                    contexts: ["selection"],
                    id: d.MenuID.PARENT_SELECT_DOMAIN,
                    parentId: d.MenuID.PARENT_EXPRESSION,
                    title: browser.i18n.getMessage("contextMenusSelectedDomainText", ["%s"])
                }), d.menuCreate({
                    contexts: ["selection"],
                    id: d.MenuID.SELECT_ADD_GREY_DOMAIN,
                    parentId: d.MenuID.PARENT_SELECT_DOMAIN,
                    title: browser.i18n.getMessage("toGreyListText")
                }), d.menuCreate({
                    contexts: ["selection"],
                    id: d.MenuID.SELECT_ADD_WHITE_DOMAIN,
                    parentId: d.MenuID.PARENT_SELECT_DOMAIN,
                    title: browser.i18n.getMessage("toWhiteListText")
                }), d.menuCreate({
                    contexts: ["selection"],
                    id: d.MenuID.PARENT_SELECT_SUBS,
                    parentId: d.MenuID.PARENT_EXPRESSION,
                    title: browser.i18n.getMessage("contextMenusSelectedSubdomainText", ["%s"])
                }), d.menuCreate({
                    contexts: ["selection"],
                    id: d.MenuID.SELECT_ADD_GREY_SUBS,
                    parentId: d.MenuID.PARENT_SELECT_SUBS,
                    title: browser.i18n.getMessage("toGreyListText")
                }), d.menuCreate({
                    contexts: ["selection"],
                    id: d.MenuID.SELECT_ADD_WHITE_SUBS,
                    parentId: d.MenuID.PARENT_SELECT_SUBS,
                    title: browser.i18n.getMessage("toWhiteListText")
                }), d.menuCreate({type: "separator"}), d.menuCreate({
                    checked: (0, r.getSetting)(s.default.store.getState(), "activeMode"),
                    id: d.MenuID.ACTIVE_MODE,
                    title: browser.i18n.getMessage("activeModeText"),
                    type: "checkbox"
                }), d.menuCreate({
                    id: d.MenuID.SETTINGS,
                    title: browser.i18n.getMessage("settingsText")
                }), (0, r.eventListenerActions)(browser.contextMenus.onClicked, d.onContextMenuClicked, "ADD")))
            }

            static menuClear() {
                return a.__awaiter(this, void 0, void 0, (function* () {
                    yield browser.contextMenus.removeAll(), (0, r.eventListenerActions)(browser.contextMenus.onClicked, d.onContextMenuClicked, "REMOVE"), d.isInitialized = !1, (0, r.cadLog)({msg: "ContextMenuEvents.menuClear:  Context Menu has been removed."}, (0, r.getSetting)(s.default.store.getState(), "debugMode"))
                }))
            }

            static menuCreate(e) {
                return browser.contextMenus.create(Object.assign(Object.assign({}, e), {contexts: e.contexts ? e.contexts : ["browser_action", "page"]}), d.onCreatedOrUpdated)
            }

            static updateMenuItemCheckbox(e, t) {
                browser.contextMenus.update(e, {checked: t}).finally(this.onCreatedOrUpdated), (0, r.cadLog)({
                    msg: "ContextMenuEvents.updateMenuItemCheckbox: Updated Menu Item.",
                    x: {id: e, checked: t}
                }, (0, r.getSetting)(s.default.store.getState(), "debugMode"))
            }

            static onCreatedOrUpdated() {
                const e = (0, r.getSetting)(s.default.store.getState(), "debugMode");
                browser.runtime.lastError ? (0, r.cadLog)({
                    msg: `ContextMenuEvents.onCreatedOrUpdated received an error: ${browser.runtime.lastError}`,
                    type: "error"
                }, !0) : (0, r.cadLog)({msg: "ContextMenuEvents.onCreatedOrUpdated:  Create/Update contextMenuItem was successful."}, e)
            }

            static onContextMenuClicked(e, t) {
                return a.__awaiter(this, void 0, void 0, (function* () {
                    const n = (0, r.getSetting)(s.default.store.getState(), "debugMode"),
                        a = (0, r.getSetting)(s.default.store.getState(), "contextualIdentities");
                    (0, r.cadLog)({
                        msg: "ContextMenuEvents.onContextMenuClicked:  Data received",
                        x: {info: e, tab: t}
                    }, n);
                    const c = t && t.cookieStoreId || "", l = e && e.selectionText || "";
                    if (e.menuItemId.toString().startsWith(d.MenuID.MANUAL_CLEAN_SITEDATA)) {
                        const a = e.menuItemId.toString().slice(d.MenuID.MANUAL_CLEAN_SITEDATA.length),
                            o = (0, r.getHostname)(t.url);
                        if (!o) return (0, r.cadLog)({
                            msg: `ContextMenuEvents.onContextMenuClicked cannot clean ${a} from tab:`,
                            type: "warn",
                            x: {tab: t}
                        }, n), void (0, r.showNotification)({
                            duration: (0, r.getSetting)(s.default.store.getState(), "notificationOnScreen"),
                            msg: `${browser.i18n.getMessage("manualCleanError", [browser.i18n.getMessage(`${(0, r.siteDataToBrowser)(a)}Text`)])}\n\n              ${t.title}\n\n\n              ${t.url}\n              `
                        });
                        if ((0, r.cadLog)({msg: `ContextMenuEvents.onContextMenuClicked triggered Clean Site Data (${a}) For This Domain.`}, n), "Cookies" === a) return void (yield(0, i.clearCookiesForThisDomain)(s.default.store.getState(), t));
                        switch (a) {
                            case"All":
                            case"Cache":
                            case"IndexedDB":
                            case"PluginData":
                            case"ServiceWorkers":
                                yield(0, i.clearSiteDataForThisDomain)(s.default.store.getState(), a, o);
                                break;
                            case"LocalStorage":
                                yield(0, i.clearLocalStorageForThisDomain)(s.default.store.getState(), t);
                                break;
                            default:
                                (0, r.cadLog)({
                                    msg: `ContextMenuEvents.onContextMenuClicked received unknown manual clean site data type: ${e.menuItemId}`,
                                    type: "warn",
                                    x: {info: e, tab: t}
                                }, n)
                        }
                    } else switch (e.menuItemId) {
                        case d.MenuID.CLEAN:
                            (0, r.cadLog)({msg: "ContextMenuEvents.onContextMenuClicked triggered Normal Clean."}, n), s.default.store.dispatch((0, o.cookieCleanup)({
                                greyCleanup: !1,
                                ignoreOpenTabs: !1
                            }));
                            break;
                        case d.MenuID.CLEAN_OPEN:
                            (0, r.cadLog)({msg: "ContextMenuEvents.onContextMenuClicked triggered Clean, include open tabs."}, n), s.default.store.dispatch((0, o.cookieCleanup)({
                                greyCleanup: !1,
                                ignoreOpenTabs: !0
                            }));
                            break;
                        case d.MenuID.LINK_ADD_GREY_DOMAIN:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was LINK_ADD_GREY_DOMAIN.",
                                x: {linkUrl: e.linkUrl, hostname: (0, r.getHostname)(e.linkUrl), cookieStoreId: c}
                            }, n), d.addNewExpression((0, r.getHostname)(e.linkUrl), "GREY", c);
                            break;
                        case d.MenuID.LINK_ADD_WHITE_DOMAIN:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was LINK_ADD_WHITE_DOMAIN.",
                                x: {linkUrl: e.linkUrl, hostname: (0, r.getHostname)(e.linkUrl), cookieStoreId: c}
                            }, n), d.addNewExpression((0, r.getHostname)(e.linkUrl), "WHITE", c);
                            break;
                        case d.MenuID.LINK_ADD_GREY_SUBS:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was LINK_ADD_GREY_SUBS.",
                                x: {linkUrl: e.linkUrl, hostname: (0, r.getHostname)(e.linkUrl), cookieStoreId: c}
                            }, n), d.addNewExpression(`*.${(0, r.getHostname)(e.linkUrl)}`, "GREY", c);
                            break;
                        case d.MenuID.LINK_ADD_WHITE_SUBS:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was LINK_ADD_WHITE_SUBS.",
                                x: {linkUrl: e.linkUrl, hostname: (0, r.getHostname)(e.linkUrl), cookieStoreId: c}
                            }, n), d.addNewExpression(`*.${(0, r.getHostname)(e.linkUrl)}`, "WHITE", c);
                            break;
                        case d.MenuID.PAGE_ADD_GREY_DOMAIN:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was PAGE_ADD_GREY_DOMAIN.",
                                x: {
                                    pageURL: e.pageUrl,
                                    hostname: (0, r.getHostname)(e.pageUrl),
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), d.addNewExpression((0, r.getHostname)(e.pageUrl), "GREY", c);
                            break;
                        case d.MenuID.PAGE_ADD_WHITE_DOMAIN:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was PAGE_ADD_WHITE_DOMAIN.",
                                x: {
                                    pageURL: e.pageUrl,
                                    hostname: (0, r.getHostname)(e.pageUrl),
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), d.addNewExpression((0, r.getHostname)(e.pageUrl), "WHITE", c);
                            break;
                        case d.MenuID.PAGE_ADD_GREY_SUBS:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was PAGE_ADD_GREY_SUBS.",
                                x: {
                                    pageURL: e.pageUrl,
                                    hostname: (0, r.getHostname)(e.pageUrl),
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), d.addNewExpression(`*.${(0, r.getHostname)(e.pageUrl)}`, "GREY", c);
                            break;
                        case d.MenuID.PAGE_ADD_WHITE_SUBS:
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was PAGE_ADD_WHITE_SUBS.",
                                x: {
                                    pageURL: e.pageUrl,
                                    hostname: (0, r.getHostname)(e.pageUrl),
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), d.addNewExpression(`*.${(0, r.getHostname)(e.pageUrl)}`, "WHITE", c);
                            break;
                        case d.MenuID.SELECT_ADD_GREY_DOMAIN: {
                            const t = l.trim().split(",");
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was SELECT_ADD_GREY_DOMAIN.",
                                x: {
                                    selectionText: e.selectionText,
                                    texts: t,
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), t.forEach((e => {
                                (0, r.cadLog)({
                                    msg: "ContextMenuEvents.onContextMenuClicked:  encodeURI on selected text",
                                    x: {rawInput: e.trim(), encodedInput: encodeURI(e.trim())}
                                }, n), d.addNewExpression(encodeURI(e.trim()), "GREY", c)
                            }))
                        }
                            break;
                        case d.MenuID.SELECT_ADD_WHITE_DOMAIN: {
                            const t = l.trim().split(",");
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was SELECT_ADD_WHITE_DOMAIN.",
                                x: {
                                    selectionText: e.selectionText,
                                    texts: t,
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), t.forEach((e => {
                                (0, r.cadLog)({
                                    msg: "ContextMenuEvents.onContextMenuClicked:  encodeURI on selected text",
                                    x: {rawInput: e.trim(), encodedInput: encodeURI(e.trim())}
                                }, n), d.addNewExpression(encodeURI(e.trim()), "WHITE", c)
                            }))
                        }
                            break;
                        case d.MenuID.SELECT_ADD_GREY_SUBS: {
                            const t = l.trim().split(",");
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was SELECT_ADD_GREY_SUBS.",
                                x: {
                                    selectionText: e.selectionText,
                                    texts: t,
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), t.forEach((e => {
                                (0, r.cadLog)({
                                    msg: "ContextMenuEvents.onContextMenuClicked:  encodeURI on selected text",
                                    x: {rawInput: e.trim(), encodedInput: encodeURI(e.trim())}
                                }, n), d.addNewExpression(`*.${encodeURI(e.trim())}`, "GREY", c)
                            }))
                        }
                            break;
                        case d.MenuID.SELECT_ADD_WHITE_SUBS: {
                            const t = l.trim().split(",");
                            (0, r.cadLog)({
                                msg: "ContextMenuEvents.onContextMenuClicked:  menuItemId was SELECT_ADD_WHITE_SUBS.",
                                x: {
                                    selectionText: e.selectionText,
                                    texts: t,
                                    cookieStoreId: c,
                                    parsedCookieStoreId: (0, r.parseCookieStoreId)(a, c)
                                }
                            }, n), t.forEach((e => {
                                (0, r.cadLog)({
                                    msg: "ContextMenuEvents.onContextMenuClicked:  encodeURI on selected text",
                                    x: {rawInput: e.trim(), encodedInput: encodeURI(e.trim())}
                                }, n), d.addNewExpression(`*.${encodeURI(e.trim())}`, "WHITE", c)
                            }))
                        }
                            break;
                        case d.MenuID.ACTIVE_MODE:
                            Object.prototype.hasOwnProperty.call(e, "checked") && Object.prototype.hasOwnProperty.call(e, "wasChecked") && e.checked !== e.wasChecked && ((0, r.cadLog)({msg: `ContextMenuEvents.onContextMenuClicked changed Automatic Cleaning value to:  ${e.checked}.`}, n), s.default.store.dispatch((0, o.updateSetting)({
                                name: "activeMode",
                                value: e.checked
                            })));
                            break;
                        case d.MenuID.SETTINGS:
                            (0, r.cadLog)({msg: "ContextMenuEvents.onContextMenuClicked triggered Open Settings."}, n), yield browser.tabs.create({
                                index: t.index + 1,
                                url: "/settings/settings.html#tabSettings"
                            });
                            break;
                        default:
                            (0, r.cadLog)({
                                msg: `ContextMenuEvents.onContextMenuClicked received unknown menu id: ${e.menuItemId}`,
                                type: "warn",
                                x: {info: e, tab: t}
                            }, n)
                    }
                }))
            }

            static addNewExpression(e, t, n) {
                if ("" === e.trim() || "*." === e) return void (0, r.showNotification)({
                    duration: (0, r.getSetting)(s.default.store.getState(), "notificationOnScreen"),
                    msg: `${browser.i18n.getMessage("addNewExpressionNotificationFailed")}`
                });
                const a = {
                    expression: (0, r.localFileToRegex)(e.trim()),
                    listType: t,
                    storeId: (0, r.parseCookieStoreId)((0, r.getSetting)(s.default.store.getState(), "contextualIdentities"), n)
                };
                (0, r.cadLog)({
                    msg: "background.addNewExpression - Parsed from Right-Click:",
                    x: a
                }, (0, r.getSetting)(s.default.store.getState(), "debugMode"));
                const i = s.default.store.getState().cache;
                (0, r.showNotification)({
                    duration: (0, r.getSetting)(s.default.store.getState(), "notificationOnScreen"),
                    msg: `${browser.i18n.getMessage("addNewExpressionNotification", [a.expression, a.listType, `${a.storeId}${(0, r.getSetting)(s.default.store.getState(), "contextualIdentities") && void 0 !== i[a.storeId] ? ` (${i[a.storeId]})` : ""}`])}\n${browser.i18n.getMessage("addNewExpressionNotificationIgnore")}`
                }), s.default.store.dispatch((0, o.addExpressionUI)(a))
            }
        }

        t.default = d, d.MenuID = {
            ACTIVE_MODE: "cad-active-mode",
            CLEAN: "cad-clean",
            CLEAN_OPEN: "cad-clean-open",
            LINK_ADD_GREY_DOMAIN: "cad-link-add-grey-domain",
            LINK_ADD_GREY_SUBS: "cad-link-add-grey-subs",
            LINK_ADD_WHITE_DOMAIN: "cad-link-add-white-domain",
            LINK_ADD_WHITE_SUBS: "cad-link-add-white-subs",
            PAGE_ADD_GREY_DOMAIN: "cad-page-add-grey-domain",
            PAGE_ADD_GREY_SUBS: "cad-page-add-grey-subs",
            PAGE_ADD_WHITE_DOMAIN: "cad-page-add-white-domain",
            PAGE_ADD_WHITE_SUBS: "cad-page-add-white-subs",
            PARENT_CLEAN: "cad-parent-clean",
            PARENT_EXPRESSION: "cad-parent-expression",
            PARENT_LINK_DOMAIN: "cad-parent-link-domain",
            PARENT_LINK_SUBS: "cad-parent-link-subs",
            PARENT_PAGE_DOMAIN: "cad-parent-page-domain",
            PARENT_PAGE_SUBS: "cad-parent-page-subs",
            PARENT_SELECT_DOMAIN: "cad-parent-select-domain",
            PARENT_SELECT_SUBS: "cad-parent-select-subs",
            MANUAL_CLEAN_SITEDATA: "cad-clean-sitedata-",
            SELECT_ADD_GREY_DOMAIN: "cad-select-add-grey-domain",
            SELECT_ADD_GREY_SUBS: "cad-select-add-grey-subs",
            SELECT_ADD_WHITE_DOMAIN: "cad-select-add-white-domain",
            SELECT_ADD_WHITE_SUBS: "cad-select-add-white-subs",
            SETTINGS: "cad-settings"
        }, d.isInitialized = !1
    }, 2863: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0});
        const a = n(3940), o = a.__importDefault(n(210)), i = n(4719), r = n(292);

        class s extends o.default {
            static init() {
                return a.__awaiter(this, void 0, void 0, (function* () {
                    browser.contextualIdentities && (0, r.getSetting)(o.default.store.getState(), "contextualIdentities") && !s.isInitialized && (s.isInitialized = !0, yield s.cacheCookieStoreIdNames(), (0, r.eventListenerActions)(browser.contextualIdentities.onCreated, s.onContainerCreated, "ADD"), (0, r.eventListenerActions)(browser.contextualIdentities.onRemoved, s.onContainerRemoved, "ADD"), (0, r.eventListenerActions)(browser.contextualIdentities.onUpdated, s.onContainerUpdated, "ADD"), (0, r.cadLog)({msg: "ContextualIdentitiesEvents.deInit:  Container Events have been added."}, (0, r.getSetting)(o.default.store.getState(), "debugMode")))
                }))
            }

            static deInit() {
                return a.__awaiter(this, void 0, void 0, (function* () {
                    if (!s.isInitialized) return;
                    (0, r.eventListenerActions)(browser.contextualIdentities.onCreated, s.onContainerCreated, "REMOVE"), (0, r.eventListenerActions)(browser.contextualIdentities.onRemoved, s.onContainerRemoved, "REMOVE"), (0, r.eventListenerActions)(browser.contextualIdentities.onUpdated, s.onContainerUpdated, "REMOVE"), s.isInitialized = !1;
                    const e = yield browser.contextualIdentities.query({});
                    for (const t of e) o.default.store.dispatch({
                        payload: {key: t.cookieStoreId, value: void 0},
                        type: "ADD_CACHE"
                    });
                    (0, r.cadLog)({msg: "ContextualIdentitiesEvents.deInit:  Container Events have been removed."}, (0, r.getSetting)(o.default.store.getState(), "debugMode"))
                }))
            }

            static onContainerCreated(e) {
                o.default.store.dispatch({
                    payload: {
                        key: e.contextualIdentity.cookieStoreId,
                        value: e.contextualIdentity.name
                    }, type: "ADD_CACHE"
                })
            }

            static onContainerRemoved(e) {
                (0, r.getSetting)(o.default.store.getState(), "contextualIdentitiesAutoRemove") && o.default.store.dispatch((0, i.removeListUI)(e.contextualIdentity.cookieStoreId)), o.default.store.dispatch({
                    payload: {
                        key: e.contextualIdentity.cookieStoreId,
                        value: void 0
                    }, type: "ADD_CACHE"
                })
            }

            static onContainerUpdated(e) {
                const t = o.default.store.getState().cache;
                t[e.contextualIdentity.cookieStoreId] && t[e.contextualIdentity.cookieStoreId] !== e.contextualIdentity.name && o.default.store.dispatch({
                    payload: {
                        key: e.contextualIdentity.cookieStoreId,
                        value: e.contextualIdentity.name
                    }, type: "ADD_CACHE"
                })
            }

            static cacheCookieStoreIdNames() {
                return a.__awaiter(this, void 0, void 0, (function* () {
                    const e = yield browser.contextualIdentities.query({});
                    o.default.store.dispatch({
                        payload: {key: "default", value: "Default"},
                        type: "ADD_CACHE"
                    }), o.default.store.dispatch({
                        payload: {key: "firefox-default", value: "Default"},
                        type: "ADD_CACHE"
                    }), o.default.store.dispatch({
                        payload: {key: "firefox-private", value: "Private"},
                        type: "ADD_CACHE"
                    }), e.forEach((e => o.default.store.dispatch({
                        payload: {key: e.cookieStoreId, value: e.name},
                        type: "ADD_CACHE"
                    })))
                }))
            }
        }

        t.default = s, s.isInitialized = !1
    }, 7583: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0});
        const a = n(3940), o = n(292), i = a.__importDefault(n(210)), r = a.__importDefault(n(8661));

        class s extends i.default {
            static onCookieChanged(e) {
                return a.__awaiter(this, void 0, void 0, (function* () {
                    e.cookie.value = "***", (yield browser.tabs.query({
                        active: !0,
                        windowType: "normal"
                    })).forEach((t => {
                        t.id && t.url && (0, o.extractMainDomain)((0, o.getHostname)(t.url)) === (0, o.extractMainDomain)(e.cookie.domain) && r.default.onTabUpdate(t.id, {cookieChanged: e}, t)
                    }))
                }))
            }
        }

        t.default = s
    }, 3112: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0});
        const a = n(3940), o = a.__importDefault(n(210)), i = a.__importDefault(n(2863)), r = n(4719), s = n(292),
            d = n(3185), c = a.__importDefault(n(9659));

        class l extends o.default {
            static init() {
                l.current = o.default.store.getState().settings, l.isInitialized = !0
            }

            static onSettingsChange() {
                return a.__awaiter(this, void 0, void 0, (function* () {
                    l.isInitialized || l.init();
                    const e = l.current;
                    l.current = o.default.store.getState().settings, l.hasNewValue(e, "contextualIdentities") && (l.getCurrent("contextualIdentities") ? yield i.default.init() : yield i.default.deInit());
                    for (const t of s.SITEDATATYPES) {
                        const n = `${(0, s.siteDataToBrowser)(t)}Cleanup`;
                        if ((void 0 === e[n] || !e[n].value) && l.current[n].value) {
                            if ("LocalStorage" === t && void 0 !== e.localstorageCleanup && e.localstorageCleanup.value) continue;
                            if (!1 === l.getCurrent("siteDataEmptyOnEnable")) {
                                (0, s.cadLog)({
                                    msg: `${t} setting activated, but Empty Site Data on Enable is false. Existing site data kept.`,
                                    type: "info"
                                }, l.getCurrent("debugMode"));
                                continue
                            }
                            yield browser.browsingData.remove({since: 0}, {[(0, s.siteDataToBrowser)(t)]: !0}), (0, s.cadLog)({
                                msg: `${t} setting activated.  All previous ${t} has been cleared for a clean slate.`,
                                type: "info"
                            }, l.getCurrent("debugMode"))
                        }
                    }
                    if (l.hasNewValue(e, "activeMode")) {
                        const e = l.getCurrent("activeMode");
                        e || (yield browser.alarms.clear("activeModeAlarm")), yield(0, d.setGlobalIcon)(e), c.default.updateMenuItemCheckbox(c.default.MenuID.ACTIVE_MODE, e)
                    }
                    l.hasNewValue(e, "contextMenus") && (l.getCurrent("contextMenus") ? c.default.menuInit() : yield c.default.menuClear()), l.updateDeprecatedSetting(e, "localStorageCleanup", "localstorageCleanup"), l.updateDeprecatedSetting(e, "localstorageCleanup", "localStorageCleanup"), yield(0, d.checkIfProtected)(o.default.store.getState()), o.default.store.dispatch((0, r.validateSettings)())
                }))
            }

            static getCurrent(e) {
                return l.current[e].value
            }

            static hasNewValue(e, t) {
                return e[t].value !== l.current[t].value
            }

            static updateDeprecatedSetting(e, t, n) {
                e[t] && l.current[t] && l.hasNewValue(e, t) && o.default.store.dispatch({
                    payload: {
                        name: n,
                        value: l.getCurrent(t)
                    }, type: "UPDATE_SETTING"
                })
            }
        }

        t.default = l, l.delaySave = !1, l.isInitialized = !1
    }, 210: (e, t) => {
        Object.defineProperty(t, "__esModule", {value: !0});

        class n {
            static init(e) {
                n.store = e
            }
        }

        t.default = n
    }, 8661: (e, t, n) => {
        Object.defineProperty(t, "__esModule", {value: !0});
        const a = n(3940), o = a.__importDefault(n(3987)), i = a.__importDefault(n(406)), r = n(3185), s = n(292),
            d = a.__importDefault(n(210));

        class c extends d.default {
            static onTabDiscarded(e, t, n) {
                if ((0, s.getSetting)(d.default.store.getState(), "discardedCleanup")) {
                    const a = (0, s.getSetting)(d.default.store.getState(), "debugMode"),
                        o = (0, s.createPartialTabInfo)(n);
                    t.favIconUrl && a && (t.favIconUrl = "***"), t.discarded || n.discarded ? ((0, s.cadLog)({
                        msg: "TabEvents.onTabDiscarded: Tab was discarded.  Executing cleanFromTabEvents",
                        x: {tabId: e, changeInfo: t, partialTabInfo: o}
                    }, a), c.cleanFromTabEvents()) : (0, s.cadLog)({
                        msg: "TabEvents.onTabDiscarded:  Tab was not discarded.",
                        x: {tabId: e, changeInfo: t, partialTabInfo: o}
                    }, a)
                }
            }

            static onTabUpdate(e, t, n) {
                if ("complete" === n.status) {
                    const a = (0, s.getSetting)(d.default.store.getState(), "debugMode"),
                        o = (0, s.createPartialTabInfo)(n);
                    t.favIconUrl && a && (t.favIconUrl = "***"), c.onTabUpdateDelay ? (0, s.cadLog)({
                        msg: "TabEvents.onTabUpdate: actions delay is pending already.",
                        x: {tabId: e, changeInfo: t, partialTabInfo: o}
                    }, a) : (c.onTabUpdateDelay = !0, (0, s.cadLog)({
                        msg: "TabEvents.onTabUpdate: action delay has been set for ~750 ms.",
                        x: {tabId: e, changeInfo: t, partialTabInfo: o}
                    }, a), setTimeout((() => {
                        (0, s.cadLog)({
                            msg: "TabEvents.onTabUpdate: actions will now commence.",
                            x: {tabId: e, changeInfo: t, partialTabInfo: o}
                        }, a), c.getAllCookieActions(n), c.onTabUpdateDelay = !1, (0, s.cadLog)({msg: "TabEvents.onTabUpdate: actions have been processed and flag cleared."}, a)
                    }), 750))
                }
            }

            static onDomainChange(e, t, n) {
                const a = (0, s.getSetting)(d.default.store.getState(), "debugMode");
                if ("complete" === n.status) {
                    const o = (0, s.createPartialTabInfo)(n), i = (0, s.extractMainDomain)((0, s.getHostname)(n.url));
                    if (t.favIconUrl && a && (t.favIconUrl = "***"), void 0 === c.tabToDomain[e] && "" !== i) (0, s.cadLog)({
                        msg: "TabEvents.onDomainChange: First mainDomain set.",
                        x: {tabId: e, changeInfo: t, mainDomain: i, partialTabInfo: o}
                    }, a), c.tabToDomain[e] = i; else if (c.tabToDomain[e] === i || "" === i && "about:blank" !== n.url && "about:home" !== n.url && "about:newtab" !== n.url && "chrome://newtab/" !== n.url) (0, s.cadLog)({
                        msg: "TabEvents.onDomainChange: mainDomain has not changed yet.",
                        x: {tabId: e, changeInfo: t, mainDomain: i, partialTabInfo: o}
                    }, a); else {
                        const n = c.tabToDomain[e];
                        if (c.tabToDomain[e] = i, (0, s.getSetting)(d.default.store.getState(), "domainChangeCleanup")) {
                            if ("" === n) return void (0, s.cadLog)({
                                msg: "TabEvents.onDomainChange: mainDomain has changed, but previous domain may have been a blank or new tab.  Not executing domainChangeCleanup",
                                x: {tabId: e, changeInfo: t, partialTabInfo: o}
                            }, a);
                            (0, s.cadLog)({
                                msg: "TabEvents.onDomainChange: mainDomain has changed.  Executing domainChangeCleanup",
                                x: {tabId: e, changeInfo: t, oldMainDomain: n, mainDomain: i, partialTabInfo: o}
                            }, a), c.cleanFromTabEvents()
                        } else (0, s.cadLog)({
                            msg: "TabEvents.onDomainChange: mainDomain has changed, but cleanOnDomainChange is not enabled.  Not cleaning.",
                            x: {tabId: e, changeInfo: t, oldMainDomain: n, mainDomain: i, partialTabInfo: o}
                        }, a)
                    }
                }
            }

            static onDomainChangeRemove(e, t) {
                (0, s.cadLog)({
                    msg: "TabEvents.onDomainChangeRemove: Tab was closed.  Removing old tabToDomain info.",
                    x: {tabId: e, mainDomain: c.tabToDomain[e], removeInfo: t}
                }, (0, s.getSetting)(d.default.store.getState(), "debugMode")), delete c.tabToDomain[e]
            }
        }

        t.default = c, c.cleanFromTabEvents = () => a.__awaiter(void 0, void 0, void 0, (function* () {
            const e = (0, s.getSetting)(d.default.store.getState(), "debugMode");
            if ((0, s.getSetting)(d.default.store.getState(), "activeMode")) {
                const t = yield browser.alarms.get("activeModeAlarm");
                !t || t.name && "activeModeAlarm" !== t.name ? ((0, s.cadLog)({msg: "TabEvents.cleanFromTabEvents:  No Alarms detected.  Creating alarm for cleaning..."}, e), yield i.default.createActiveModeAlarm()) : (0, s.cadLog)({
                    msg: "TabEvents.cleanFromTabEvents:  An alarm for cleaning was created already.  Cleaning will commence soon.",
                    x: t
                }, e)
            }
        })), c.getAllCookieActions = e => a.__awaiter(void 0, void 0, void 0, (function* () {
            if (!e.url || "" === e.url) return;
            if (e.url.startsWith("about:") || e.url.startsWith("chrome:")) return;
            const t = (0, s.getSetting)(d.default.store.getState(), "debugMode"), n = (0, s.createPartialTabInfo)(e),
                a = yield(0, s.getAllCookiesForDomain)(d.default.store.getState(), e);
            if (!a) return void (0, s.cadLog)({
                msg: "TabEvents.getAllCookieActions: Libs.getAllCookiesForDomain returned undefined.  Skipping Cookie Actions.",
                x: {partialTabInfo: n}
            }, t);
            const i = a.filter((e => e.name === s.CADCOOKIENAME));
            if (0 === i.length && ((0, s.getSetting)(d.default.store.getState(), "cacheCleanup") || (0, s.getSetting)(d.default.store.getState(), "indexedDBCleanup") || (0, s.getSetting)(d.default.store.getState(), "localStorageCleanup") || (0, s.getSetting)(d.default.store.getState(), "pluginDataCleanup") || (0, s.getSetting)(d.default.store.getState(), "serviceWorkersCleanup")) && (0, s.isAWebpage)(e.url) && !e.url.startsWith("file:")) {
                const a = (0, s.returnOptionalCookieAPIAttributes)(d.default.store.getState(), {
                    expirationDate: Math.floor(Date.now() / 1e3 + 31557600),
                    firstPartyDomain: (yield(0, s.isFirstPartyIsolate)()) ? (0, s.extractMainDomain)((0, s.getHostname)(e.url)) : "",
                    name: s.CADCOOKIENAME,
                    path: `/${o.default.generate()}`,
                    storeId: e.cookieStoreId,
                    url: e.url,
                    value: s.CADCOOKIENAME
                });
                yield browser.cookies.set(Object.assign(Object.assign({}, a), {url: e.url})), (0, s.cadLog)({
                    msg: "TabEvents.getAllCookieActions:  A temporary cookie has been set for future BrowsingData cleaning as the site did not set any cookies yet.",
                    x: {partialTabInfo: n, cadLSCookie: a}
                }, t)
            }
            const c = a.length - i.length;
            a.length !== c && (0, s.cadLog)({
                msg: "TabEvents.getAllCookieActions:  New Cookie Count after filtering out cookie set by extension",
                x: {preFilterCount: a.length, newCookieCount: c}
            }, t), (0, s.cadLog)({msg: "TabEvents.getAllCookieActions: executing checkIfProtected to update Icons and Title."}, t), yield(0, r.checkIfProtected)(d.default.store.getState(), e, c), (0, s.getSetting)(d.default.store.getState(), "showNumOfCookiesInIcon") && "android" !== (d.default.store.getState().cache.platformOs || "") && ((0, s.cadLog)({msg: "TabEvents.getAllCookieActions: executing showNumberOfCookiesInIcon."}, t), (0, r.showNumberOfCookiesInIcon)(e, c))
        })), c.onTabUpdateDelay = !1, c.tabToDomain = {}
    }
}]);