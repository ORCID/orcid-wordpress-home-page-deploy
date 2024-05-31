(function(a) {
    "use strict";
    a(document).ready(function() {
        a(".tpgb-tabs-wrapper").each(function() {
            var b = a(this)
              , c = b.data("tab-hover")
              , d = b.find(".tpgb-tab-header");
            "no" == c && (/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream ? d.on("touchstart", function() {
                var c = a(this).data("tab")
                  , d = a(this).closest(".tpgb-tabs-wrapper")
                  , e = a(d).children(".tpgb-tabs-nav").children(".tpgb-tab-li").children(".tpgb-tab-header")
                  , f = a(d).children(".tpgb-tabs-content-wrapper").children(".tpgb-tab-content");
                if (a(d).find(">.tpgb-tabs-nav-wrapper .tpgb-tab-header").removeClass("active default-active").addClass("inactive"),
                a(this).addClass("active").removeClass("inactive"),
                a(d).find(">.tpgb-tabs-content-wrapper>.tpgb-tab-content").removeClass("active").addClass("inactive"),
                a(">.tpgb-tabs-content-wrapper>.tpgb-tab-content[data-tab='" + c + "']", d).addClass("active").removeClass("inactive"),
                a(".tpgb-tab-content[data-tab='" + c + "']").find(".tpgb-carousel").length) {
                    var g = document.querySelectorAll(".tpgb-tab-content[data-tab='" + c + "'] .tpgb-carousel");
                    g.forEach(function(a) {
                        var b = slideStore.get(a);
                        b.refresh()
                    })
                }
                if (a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope .post-loop-inner", b).length) {
                    a("body").height() <= a(window).height() && a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope").each(function() {
                        a(this).find(".post-lazy-load").length && "function" == typeof tpgb_lazy_load_ajax && tpgb_lazy_load_ajax(a(this))
                    });
                    let d = a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope .post-loop-inner", b);
                    d.isotope({
                        itemSelector: ".grid-item",
                        resizable: !0,
                        sortBy: "original-order",
                        resizesContainer: !0,
                        initLayout: !1
                    }),
                    d.isotope("layout"),
                    setTimeout(function() {
                        d.isotope("layout")
                    }, 50),
                    "no" == d.data("anim") && d.isotope({
                        transitionDuration: 0
                    }),
                    0 == d.height() && (d.css("opacity", 0),
                    d.isotope("once", "layoutComplete", function() {
                        d.css("opacity", 1)
                    }))
                }
                if (a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-metro .post-loop-inner", b).length && (a("body").height() <= a(window).height() && a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-metro").each(function() {
                    a(this).find(".post-lazy-load").length && "function" == typeof tpgb_lazy_load_ajax && tpgb_lazy_load_ajax(a(this))
                }),
                setTimeout(function() {
                    tpgb_metro_layout("")
                }, 30)),
                a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-equal-height", b).length && setTimeout(function() {
                    var d = a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-equal-height", b);
                    if ("function" == typeof equalHeightFun) {
                        var e = d[0] ? d[0] : "";
                        equalHeightFun(e)
                    }
                }, 30),
                a(".tpgb-tab-content[data-tab='" + c + "'] .tp-expand", b).length) {
                    var h = a(".tpgb-tab-content[data-tab='" + c + "'] .tp-expand", b);
                    h.each(function() {
                        "function" == typeof tpgb_unfold && tpgb_unfold(a(this)[0])
                    })
                }
                a(f).each(function() {
                    a(this).removeClass("default-active")
                }),
                a(">.tpgb-tabs-content-wrapper>.tpgb-tab-content[data-tab='" + c + "'] .pt_tpgb_before_after", d).length && size_Elements()
            }) : d.on("click", function() {
                var c = a(this).data("tab")
                  , d = a(this).closest(".tpgb-tabs-wrapper")
                  , e = a(d).children(".tpgb-tabs-nav").children(".tpgb-tab-li").children(".tpgb-tab-header")
                  , f = a(d).children(".tpgb-tabs-content-wrapper").children(".tpgb-tab-content");
                if (a(d).find(">.tpgb-tabs-nav-wrapper .tpgb-tab-header").removeClass("active default-active").addClass("inactive"),
                a(this).addClass("active").removeClass("inactive"),
                a(d).find(">.tpgb-tabs-content-wrapper>.tpgb-tab-content").removeClass("active").addClass("inactive"),
                a(">.tpgb-tabs-content-wrapper>.tpgb-tab-content[data-tab='" + c + "']", d).addClass("active").removeClass("inactive"),
                a(".tpgb-tab-content[data-tab='" + c + "']").find(".tpgb-carousel").length) {
                    var g = document.querySelectorAll(".tpgb-tab-content[data-tab='" + c + "'] .tpgb-carousel");
                    g.forEach(function(a) {
                        var b = slideStore.get(a);
                        b.refresh()
                    })
                }
                if (a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope .post-loop-inner", b).length) {
                    a("body").height() <= a(window).height() && a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope").each(function() {
                        a(this).find(".post-lazy-load").length && "function" == typeof tpgb_lazy_load_ajax && tpgb_lazy_load_ajax(a(this))
                    });
                    let d = a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope .post-loop-inner", b);
                    d.isotope({
                        itemSelector: ".grid-item",
                        resizable: !0,
                        sortBy: "original-order",
                        resizesContainer: !0,
                        initLayout: !1
                    }),
                    d.isotope("layout"),
                    setTimeout(function() {
                        d.isotope("layout")
                    }, 50),
                    "no" == d.data("anim") && d.isotope({
                        transitionDuration: 0
                    }),
                    0 == d.height() && (d.css("opacity", 0),
                    d.isotope("once", "layoutComplete", function() {
                        d.css("opacity", 1)
                    }))
                }
                if (a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-metro .post-loop-inner", b).length && (a("body").height() <= a(window).height() && a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-metro").each(function() {
                    a(this).find(".post-lazy-load").length && "function" == typeof tpgb_lazy_load_ajax && tpgb_lazy_load_ajax(a(this))
                }),
                setTimeout(function() {
                    tpgb_metro_layout("")
                }, 30)),
                a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-equal-height", b).length && setTimeout(function() {
                    var d = a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-equal-height", b);
                    if ("function" == typeof equalHeightFun) {
                        var e = d[0] ? d[0] : "";
                        equalHeightFun(e)
                    }
                }, 30),
                a(".tpgb-tab-content[data-tab='" + c + "'] .tp-expand", b).length) {
                    var h = a(".tpgb-tab-content[data-tab='" + c + "'] .tp-expand", b);
                    h.each(function() {
                        "function" == typeof tpgb_unfold && tpgb_unfold(a(this)[0])
                    })
                }
                a(f).each(function() {
                    a(this).removeClass("default-active")
                }),
                a(">.tpgb-tabs-content-wrapper>.tpgb-tab-content[data-tab='" + c + "'] .pt_tpgb_before_after", d).length && size_Elements()
            })),
            "yes" == c && d.on("mouseover", function() {
                var c = a(this).data("tab")
                  , d = a(this).closest(".tpgb-tabs-wrapper")
                  , e = a(d).children(".tpgb-tabs-nav").children(".tpgb-tab-li").children(".tpgb-tab-header")
                  , f = a(d).children(".tpgb-tabs-content-wrapper").children(".tpgb-tab-content");
                if (a(d).find(">.tpgb-tabs-nav-wrapper .tpgb-tab-header").removeClass("active default-active").addClass("inactive"),
                a(this).addClass("active").removeClass("inactive"),
                a(d).find(">.tpgb-tabs-content-wrapper>.tpgb-tab-content").removeClass("active").addClass("inactive"),
                a(">.tpgb-tabs-content-wrapper>.tpgb-tab-content[data-tab='" + c + "']", d).addClass("active").removeClass("inactive"),
                a(".tpgb-tab-content[data-tab='" + c + "']").find(".tpgb-carousel").length) {
                    var g = document.querySelectorAll(".tpgb-tab-content[data-tab='" + c + "'] .tpgb-carousel");
                    g.forEach(function(a) {
                        var b = slideStore.get(a);
                        b.refresh()
                    })
                }
                if (a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope .post-loop-inner", b).length) {
                    a("body").height() <= a(window).height() && a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope").each(function() {
                        a(this).find(".post-lazy-load").length && "function" == typeof tpgb_lazy_load_ajax && tpgb_lazy_load_ajax(a(this))
                    });
                    let d = a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-isotope .post-loop-inner", b);
                    d.isotope({
                        itemSelector: ".grid-item",
                        resizable: !0,
                        sortBy: "original-order",
                        resizesContainer: !0,
                        initLayout: !1
                    }),
                    d.isotope("layout"),
                    setTimeout(function() {
                        d.isotope("layout")
                    }, 50),
                    "no" == d.data("anim") && d.isotope({
                        transitionDuration: 0
                    }),
                    0 == d.height() && (d.css("opacity", 0),
                    d.isotope("once", "layoutComplete", function() {
                        d.css("opacity", 1)
                    }))
                }
                if (a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-metro .post-loop-inner", b).length && (a("body").height() <= a(window).height() && a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-metro").each(function() {
                    a(this).find(".post-lazy-load").length && "function" == typeof tpgb_lazy_load_ajax && tpgb_lazy_load_ajax(a(this))
                }),
                setTimeout(function() {
                    tpgb_metro_layout("")
                }, 30)),
                a(f).each(function() {
                    a(this).removeClass("default-active")
                }),
                a(">.tpgb-tabs-content-wrapper>.tpgb-tab-content[data-tab='" + c + "'] .pt_tpgb_before_after", d).length && size_Elements(),
                a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-equal-height", b).length && setTimeout(function() {
                    var d = a(" .tpgb-tab-content[data-tab='" + c + "'] .tpgb-equal-height", b);
                    if ("function" == typeof equalHeightFun) {
                        var e = d[0] ? d[0] : "";
                        equalHeightFun(e)
                    }
                }, 30),
                a(".tpgb-tab-content[data-tab='" + c + "'] .tp-expand", b).length) {
                    var h = a(".tpgb-tab-content[data-tab='" + c + "'] .tp-expand", b);
                    h.each(function() {
                        "function" == typeof tpgb_unfold && tpgb_unfold(a(this)[0])
                    })
                }
            });
            var e = window.location.hash;
            if ("" != e && e != null && !a(e).hasClass("active") && a(e).length) {
                a("html, body").animate({
                    scrollTop: a(e).offset().top
                }, 1500),
                a(e + ".tpgb-tab-header").trigger("click");
                var f = a(e).data("tab");
                a(".tab-mobile-title[data-tab='" + f + "']").trigger("click")
            }
        }),
        0 < a(".tpgb-tabs-wrapper.swiper-container").length && new Swiper(".tpgb-tabs-wrapper.swiper-container",{
            slidesPerView: "auto",
            mousewheelControl: !0,
            freeMode: !0
        }),
        a(".tpgb-tabs-wrapper").hasClass("mobile-accordion") && (a(window).on("resize", function() {
            600 >= a(window).innerWidth() && a(".tpgb-tabs-wrapper").addClass("mobile-accordion-tab")
        }),
        a(".tpgb-tabs-content-wrapper .tab-mobile-title").on("click", function() {
            var b = a(this).data("tab")
              , c = a(this).closest(".tpgb-tabs-wrapper")
              , d = a(c).children(".tpgb-tabs-content-wrapper").children(".tab-mobile-title")
              , e = a(c).children(".tpgb-tabs-content-wrapper").children(".tpgb-tab-content");
            a(c).find(">.tpgb-tabs-content-wrapper .tab-mobile-title").removeClass("active default-active").addClass("inactive"),
            a(this).addClass("active").removeClass("inactive"),
            a(c).find(">.tpgb-tabs-content-wrapper>.tpgb-tab-content").removeClass("active").addClass("inactive"),
            a(">.tpgb-tabs-content-wrapper>.tpgb-tab-content[data-tab='" + b + "']", c).addClass("active").removeClass("inactive"),
            a(e).each(function() {
                a(this).removeClass("default-active")
            })
        }))
    })
}
)(jQuery);
