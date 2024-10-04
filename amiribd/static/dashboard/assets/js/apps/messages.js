"use strict";
function _typeof(e) {
  return (_typeof =
    "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
      ? function (e) {
          return typeof e;
        }
      : function (e) {
          return e &&
            "function" == typeof Symbol &&
            e.constructor === Symbol &&
            e !== Symbol.prototype
            ? "symbol"
            : typeof e;
        })(e);
}
!(function (e) {
  var t, o, a;
  "function" == typeof define && define.amd && (define(e), (t = !0)),
    "object" ===
      ("undefined" == typeof exports ? "undefined" : _typeof(exports)) &&
      ((module.exports = e()), (t = !0)),
    t ||
      ((o = window.Cookies),
      ((a = window.Cookies = e()).noConflict = function () {
        return (window.Cookies = o), a;
      }));
})(function () {
  function s() {
    for (var e = 0, t = {}; e < arguments.length; e++) {
      var o,
        a = arguments[e];
      for (o in a) t[o] = a[o];
    }
    return t;
  }
  function l(e) {
    return e.replace(/(%[0-9A-Z]{2})+/g, decodeURIComponent);
  }
  return (function e(d) {
    function r() {}
    function o(e, t, o) {
      if ("undefined" != typeof document) {
        "number" == typeof (o = s({ path: "/" }, r.defaults, o)).expires &&
          (o.expires = new Date(+new Date() + 864e5 * o.expires)),
          (o.expires = o.expires ? o.expires.toUTCString() : "");
        try {
          var a = JSON.stringify(t);
          /^[\{\[]/.test(a) && (t = a);
        } catch (e) {}
        (t = d.write
          ? d.write(t, e)
          : encodeURIComponent(String(t)).replace(
              /%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g,
              decodeURIComponent
            )),
          (e = encodeURIComponent(String(e))
            .replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent)
            .replace(/[\(\)]/g, escape));
        var n,
          i = "";
        for (n in o)
          o[n] &&
            ((i += "; " + n), !0 !== o[n]) &&
            (i += "=" + o[n].split(";")[0]);
        return (document.cookie = e + "=" + t + i);
      }
    }
    function t(e, t) {
      if ("undefined" != typeof document) {
        for (
          var o = {},
            a = document.cookie ? document.cookie.split("; ") : [],
            n = 0;
          n < a.length;
          n++
        ) {
          var i = a[n].split("="),
            r = i.slice(1).join("=");
          t || '"' !== r.charAt(0) || (r = r.slice(1, -1));
          try {
            var s = l(i[0]),
              r = (d.read || d)(r, s) || l(r);
            if (t)
              try {
                r = JSON.parse(r);
              } catch (e) {}
            if (((o[s] = r), e === s)) break;
          } catch (e) {}
        }
        return e ? o[e] : o;
      }
    }
    return (
      (r.set = o),
      (r.get = function (e) {
        return t(e, !1);
      }),
      (r.getJSON = function (e) {
        return t(e, !0);
      }),
      (r.remove = function (e, t) {
        o(e, "", s(t, { expires: -1 }));
      }),
      (r.defaults = {}),
      (r.withConverter = e),
      r
    );
  })(function () {});
}),
  (function (r, s) {
    var d = s("body"),
      l = s("head"),
      m = "#skin-theme",
      u = ".nk-sidebar",
      c = ".nk-header",
      f = ["demo2", "ecommerce"],
      i = ["style", "aside", "header", "skin", "mode"],
      n = "light-mode",
      p = "dark-mode",
      h = ".nk-opt-item",
      v = ".nk-opt-list",
      y = {
        demo2: { aside: "is-light", header: "is-light", style: "ui-default" },
        ecommerce: {
          aside: "is-light",
          header: "is-light",
          style: "ui-default",
        },
      };
    (r.Demo = {
      save: function (e, t) {
        Cookies.set(r.Demo.apps(e), t);
      },
      remove: function (e) {
        Cookies.remove(r.Demo.apps(e));
      },
      current: function (e) {
        return Cookies.get(r.Demo.apps(e));
      },
      apps: function (e) {
        for (
          var t,
            o = window.location.pathname.split("/").map(function (e, t, o) {
              return e.replace("-", "");
            }),
            a = 0,
            n = f;
          a < n.length;
          a++
        ) {
          var i = n[a];
          0 <= o.indexOf(i) && (t = i);
        }
        return e ? e + "_" + t : t;
      },
      style: function (e, t) {
        var o = {
          mode: n + " " + p,
          style: "ui-default ui-bordered",
          aside: "is-light is-default is-theme is-dark",
          header: "is-light is-default is-theme is-dark",
        };
        return "all" === e
          ? o[t] || ""
          : "any" === e
          ? o.mode + " " + o.style + " " + o.aside + " " + o.header
          : "body" === e
          ? o.mode + " " + o.style
          : "is-default" === e || "ui-default" === e
          ? ""
          : e;
      },
      skins: function (e) {
        return !e || "default" === e ? "theme" : "theme-" + e;
      },
      defs: function (e) {
        var t = r.Demo.apps();
        if (!y[t]) {
          console.error("Configuration for '" + t + "' not found.");
          return ""; // or a sensible default
        }
        var result = y[t][e] || "";
        if (!result) {
          return "";
        }
        return r.Demo.current(e) || result;
      },
      apply: function () {
        r.Demo.apps();
        for (var e = 0, t = i; e < t.length; e++) {
          var o,
            a,
            n = t[e];
          ("aside" !== n && "header" !== n && "style" !== n) ||
            ((o = r.Demo.defs(n)),
            s((a = "aside" === n ? u : "header" === n ? c : d)).removeClass(
              r.Demo.style("all", n)
            ),
            "ui-default" !== o && "is-default" !== o && s(a).addClass(o)),
            "mode" === n && r.Demo.update(n, r.Demo.current("mode")),
            "skin" === n && r.Demo.update(n, r.Demo.current("skin"));
        }
        r.Demo.update("dir", r.Demo.current("dir"));
      },
      locked: function (e) {
        !0 === e
          ? (s(h + "[data-key=aside]")
              .add(h + "[data-key=header]")
              .add(h + "[data-key=skin]")
              .addClass("disabled"),
            r.Demo.update("skin", "default", !0),
            s(h + "[data-key=skin]").removeClass("active"),
            s(h + "[data-key=skin][data-update=default]").addClass("active"))
          : s(h + "[data-key=aside]")
              .add(h + "[data-key=header]")
              .add(h + "[data-key=skin]")
              .removeClass("disabled");
      },
      update: function (e, t, o) {
        var a,
          n = r.Demo.style(t, e),
          i = r.Demo.style("all", e);
        r.Demo.apps();
        ("aside" !== e && "header" !== e) ||
          (s((a = "header" == e ? c : u)).removeClass(i), s(a).addClass(n)),
          "mode" === e &&
            (d.removeClass(i).removeAttr("theme"),
            n === p
              ? (d.addClass(n).attr("theme", "dark"), r.Demo.locked(!0))
              : (d.addClass(n).removeAttr("theme"), r.Demo.locked(!1))),
          "style" === e && (d.removeClass(i), d.addClass(n)),
          "skin" === e &&
            ((a = r.Demo.skins(n)),
            (i = s("#skin-default")
              .attr("href")
              .replace("theme", "skins/" + a)),
            "theme" === a
              ? s(m).remove()
              : 0 < s(m).length
              ? s(m).attr("href", i)
              : l.append(
                  '<link id="skin-theme" rel="stylesheet" href="' + i + '">'
                )),
          !0 === o && r.Demo.save(e, t);
      },
      reset: function () {
        var t = r.Demo.apps();
        d.removeClass(r.Demo.style("body")).removeAttr("theme"),
          s(h).removeClass("active"),
          s(m).remove(),
          s(u).removeClass(r.Demo.style("all", "aside")),
          s(c).removeClass(r.Demo.style("all", "header"));
        for (var e = 0, o = i; e < o.length; e++) {
          var a = o[e];
          s("[data-key='" + a + "']").each(function () {
            var e = s(this).data("update");
            ("aside" !== a && "header" !== a && "style" !== a) ||
              (e === y[t][a] && s(this).addClass("active")),
              ("mode" !== a && "skin" !== a) ||
                (e !== n && "default" !== e) ||
                s(this).addClass("active");
          }),
            r.Demo.remove(a);
        }
        s("[data-key='dir']").each(function () {
          s(this).data("update") === r.Demo.current("dir") &&
            s(this).addClass("active");
        }),
          r.Demo.apply();
      },
      load: function () {
        r.Demo.apply(),
          0 < s(h).length &&
            s(h).each(function () {
              var e = s(this).data("update"),
                t = s(this).data("key");
              ("aside" !== t && "header" !== t && "style" !== t) ||
                (e === r.Demo.defs(t) &&
                  (s(this).parent(v).find(h).removeClass("active"),
                  s(this).addClass("active"))),
                ("mode" !== t && "skin" !== t && "dir" !== t) ||
                  (e != r.Demo.current("skin") &&
                    e != r.Demo.current("mode") &&
                    e != r.Demo.current("dir")) ||
                  (s(this).parent(v).find(h).removeClass("active"),
                  s(this).addClass("active"));
            });
      },
      trigger: function () {
        s(h).on("click", function (e) {
          e.preventDefault();
          var e = s(this),
            t = e.parent(v),
            o = e.data("update"),
            a = e.data("key");
          r.Demo.update(a, o, !0),
            t.find(h).removeClass("active"),
            e.addClass("active"),
            "dir" == a &&
              setTimeout(function () {
                window.location.reload();
              }, 100);
        }),
          s(".nk-opt-reset > a").on("click", function (e) {
            e.preventDefault(), r.Demo.reset();
          });
      },
      init: function (e) {
        r.Demo.load(), r.Demo.trigger();
      },
    }),
      r.coms.docReady.push(r.Demo.init),
      (r.Promo = function () {
        var t = s(".pmo-st"),
          o = s(".pmo-lv"),
          e = s(".pmo-close");
        0 < e.length &&
          e.on("click", function () {
            var e = Cookies.get("intm-offer");
            return (
              o.removeClass("active"),
              t.addClass("active"),
              null == e &&
                Cookies.set("intm-offer", "true", { expires: 1, path: "" }),
              !1
            );
          }),
          s(window).on("load", function () {
            (null == Cookies.get("intm-offer") ? o : t).addClass("active");
          });
      }),
      r.coms.docReady.push(r.Promo);
  })(NioApp, jQuery);
