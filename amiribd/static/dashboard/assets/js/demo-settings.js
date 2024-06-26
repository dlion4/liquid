// sourcery skip: avoid-function-declarations-in-blocks
// sourcery skip: dont-reassign-parameters
// sourcery skip: avoid-using-var
"use strict"; function _typeof(e) { return (_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) { return typeof e } : function (e) { return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e })(e) } !function (e) { var t, o, a; "function" == typeof define && define.amd && (define(e), t = !0), "object" === ("undefined" == typeof exports ? "undefined" : _typeof(exports)) && (module.exports = e(), t = !0), t || (o = window.Cookies, (a = window.Cookies = e()).noConflict = function () { return window.Cookies = o, a }) }(function () {
    function d() { for (var e = 0, t = {}; e < arguments.length; e++) { var o, a = arguments[e]; for (o in a) t[o] = a[o] } return t } function u(e) { return e.replace(/(%[0-9A-Z]{2})+/g, decodeURIComponent) } return function e(s) {
        function i() { } function o(e, t, o) { if ("undefined" != typeof document) { "number" == typeof (o = d({ path: "/" }, i.defaults, o)).expires && (o.expires = new Date(+new Date + 864e5 * o.expires)), o.expires = o.expires ? o.expires.toUTCString() : ""; try { var a = JSON.stringify(t); /^[\{\[]/.test(a) && (t = a) } catch (e) { } t = s.write ? s.write(t, e) : encodeURIComponent(String(t)).replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent), e = encodeURIComponent(String(e)).replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent).replace(/[\(\)]/g, escape); var n, r = ""; for (n in o) o[n] && (r += "; " + n, !0 !== o[n]) && (r += "=" + o[n].split(";")[0]); return document.cookie = e + "=" + t + r } } function t(e, t) {
            if ("undefined" != typeof document) {
                for (var o = {}, a = document.cookie ? document.cookie.split("; ") : [], n = 0; n < a.length; n++) {
                    var r = a[n].split("="), i = r.slice(1).join("="); t || '"' !== i.charAt(0) || (i = i.slice(1, -1)); try {
                        var d = u(r[0]), i = (s.read || s)(i, d) || u(i); if (t) {
                            try { i = JSON.parse(i) } catch (e) { }
                        } if (o[d] = i, e === d) {
                            break
                        }
                    } catch (e) { }
                } return e ? o[e] : o
            }
        } return i.set = o, i.get = function (e) { return t(e, !1) }, i.getJSON = function (e) { return t(e, !0) }, i.remove = function (e, t) { o(e, "", d(t, { expires: -1 })) }, i.defaults = {}, i.withConverter = e, i
    }(function () { })
}), function (i, d) {
    var s = d("body"), u = d("head"), l = "#skin-theme", c = ".nk-header", m = ["demo6", "invest"], r = ["style", "header", "header_opt", "skin", "mode"], n = "light-mode", f = "dark-mode", p = ".nk-opt-item", h = ".nk-opt-list", v = { demo6: { header: "is-theme", header_opt: "is-regular", style: "ui-default" }, invest: { header: "is-theme", header_opt: "nk-header-fixed", style: "ui-default" } }; i.Demo = {
        // sourcery skip: avoid-using-var
        save: function (e, t) { Cookies.set(i.Demo.apps(e), t) }, remove: function (e) { Cookies.remove(i.Demo.apps(e)) }, current: function (e) { return Cookies.get(i.Demo.apps(e)) }, apps: function (e) { for (var t, o = window.location.pathname.split("/").map(function (e, t, o) { return e.replace("-", "") }), a = 0, n = m; a < n.length; a++) { var r = n[a]; o.indexOf(r) >= 0 && (t = r) } return e ? e + "_" + t : t }, style: function (e, t) { var o = { mode: n + " " + f, style: "ui-default ui-clean ui-shady ui-softy", header: "is-light is-default is-theme is-dark", header_opt: "nk-header-fixed" }; return "all" === e ? o[t] || "" : "any" === e ? o.mode + " " + o.style + " " + o.header : "body" === e ? o.mode + " " + o.style : "is-default" === e || "ui-default" === e || "is-regular" === e ? "" : e }, skins: function (e) { return !e || "default" === e ? "theme" : "theme-" + e }, defs: function (e) { var t = i.Demo.apps(), t = v[t][e] || ""; return i.Demo.current(e) || t }, apply: function () { i.Demo.apps(); for (var e = 0, t = r; e < t.length; e++) { var o, a, n = t[e]; "header" !== n && "header_opt" !== n && "style" !== n || (o = i.Demo.defs(n), d(a = "header" !== n && "header_opt" !== n ? s : c).removeClass(i.Demo.style("all", n)), "ui-default" !== o && "is-default" !== o && d(a).addClass(o)), "mode" === n && i.Demo.update(n, i.Demo.current("mode")), "skin" === n && i.Demo.update(n, i.Demo.current("skin")) } i.Demo.update("dir", i.Demo.current("dir")) }, locked: function (e) { !0 === e ? (d(p + "[data-key=header]").add(p + "[data-key=skin]").addClass("disabled"), i.Demo.update("skin", "default", !0), d(p + "[data-key=skin]").removeClass("active"), d(p + "[data-key=skin][data-update=default]").addClass("active")) : d(p + "[data-key=header]").add(p + "[data-key=skin]").removeClass("disabled") }, update: function (e, t, o) { var a, n = i.Demo.style(t, e), r = i.Demo.style("all", e); i.Demo.apps(); "header" !== e && "header_opt" !== e || (d(a = "header" == e || "header_opt" == e ? c : "").removeClass(r), d(a).addClass(n)), "mode" === e && (s.removeClass(r).removeAttr("theme"), n === f ? (s.addClass(n).attr("theme", "dark"), i.Demo.locked(!0)) : (s.addClass(n).removeAttr("theme"), i.Demo.locked(!1))), "style" === e && (s.removeClass(r), s.addClass(n)), "skin" === e && (a = i.Demo.skins(n), r = d("#skin-default").attr("href").replace("theme", "skins/" + a), "theme" === a ? d(l).remove() : d(l).length > 0 ? d(l).attr("href", r) : u.append('<link id="skin-theme" rel="stylesheet" href="' + r + '">')), !0 === o && i.Demo.save(e, t) }, reset: function () { var t = i.Demo.apps(); s.removeClass(i.Demo.style("body")).removeAttr("theme"), d(p).removeClass("active"), d(l).remove(), d(c).removeClass(i.Demo.style("all", "header")); for (var e = 0, o = r; e < o.length; e++) { var a = o[e]; d("[data-key='" + a + "']").each(function () { var e = d(this).data("update"); "header" !== a && "header_opt" !== a && "style" !== a || e === v[t][a] && d(this).addClass("active"), "mode" !== a && "skin" !== a || e !== n && "default" !== e || d(this).addClass("active") }), i.Demo.remove(a) } d("[data-key='dir']").each(function () { d(this).data("update") === i.Demo.current("dir") && d(this).addClass("active") }), i.Demo.apply() }, load: function () { i.Demo.apply(), d(p).length > 0 && d(p).each(function () { var e = d(this).data("update"), t = d(this).data("key"); "header" !== t && "header_opt" !== t && "style" !== t || e === i.Demo.defs(t) && (d(this).parent(h).find(p).removeClass("active"), d(this).addClass("active")), "mode" !== t && "skin" !== t && "dir" !== t || e != i.Demo.current("skin") && e != i.Demo.current("mode") && e != i.Demo.current("dir") || (d(this).parent(h).find(p).removeClass("active"), d(this).addClass("active")) }) }, trigger: function () { d(p).on("click", function (e) { e.preventDefault(); var e = d(this), t = e.parent(h), o = e.data("update"), a = e.data("key"); i.Demo.update(a, o, !0), t.find(p).removeClass("active"), e.addClass("active"), "dir" == a && setTimeout(function () { window.location.reload() }, 100) }), d(".nk-opt-reset > a").on("click", function (e) { e.preventDefault(), i.Demo.reset() }) },
        init: function (e) {
            i.Demo.load();
            i.Demo.trigger();
        }
    },
        i.coms.docReady.push(i.Demo.init),
        i.Promo = function () {
            var t = d(".pmo-st"),
                o = d(".pmo-lv"),
                e = d(".pmo-close");

            if (e.length > 0) {
                e.on("click", function () {
                    // sourcery skip: avoid-using-var
                    var e = Cookies.get("inv-offer");
                    return o.removeClass("active"),
                        t.addClass("active"),
                        null == e && Cookies.set("inv-offer", "true", { expires: 1, path: "" }),
                        !1;
                });
            }

            d(window).on("load", function () {
                (null == Cookies.get("inv-offer") ? o : t).addClass("active");
            });
        },
        i.coms.docReady.push(i.Promo)(NioApp, JQuery)
}
