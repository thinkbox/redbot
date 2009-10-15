"""\
<html>
<head>
	<title>RED: &lt;%(html_uri)s&gt;</title>
	<link rel="stylesheet" type='text/css' href="red_style.css">
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta name="ROBOTS" content="INDEX, NOFOLLOW" />
<script src="jquery.js"></script>
<script src="jquery.hoverIntent.js"></script>
<script language="JavaScript">

var tid = false;
jQuery.fn.hoverPopup = function(fnText, fnOver, fnOut) {
    var fnOverPopup = function(e) {
        if (tid != false) {
            clearTimeout(tid);
            tid = false;
        }
        var text = fnText.call(this, e);
        if (text) {
            var popup_width = 450;
            var popup_x;
            if (popup_width + 10 > window.innerWidth) {
                popup_x = 5;
                popup_width = window.innerWidth - 10;
            } else if (e.pageX + popup_width + 10 < window.innerWidth) {
                popup_x = e.pageX + 5;
            } else if (e.pageX - popup_width - 5 > 5) {
                popup_x = e.pageX - popup_width - 5;
            } else {
                popup_x = 5;
            }
            $("#popup")
                .fadeIn("fast")
                .css("top", (e.pageY + 5) + "px")
                .css("left", popup_x + "px")
                .css("width", popup_width + "px")
                .html(text);
        } else {
            $("#popup").hide();
        }
        if (fnOver) {
            fnOver.call(this, e);
        }
    };
    var fnOutPopup = function(e) {
        tid = setTimeout(function(){
            $("#popup").fadeOut("fast");
        }, 350);
        if (fnOut) {
            fnOut.call(this, e);
        }
    };
    return jQuery.fn.hoverIntent.call(this, fnOverPopup, fnOutPopup);
};


$(document).ready(function(){
    var hidden_list = $("#hidden_list");

    $("#popup").hoverIntent(function(){
        if (tid != false) {
            clearTimeout(tid);
            tid = false;
        }
    }, function(){
        $("#popup").fadeOut("fast");
    });

    $("span.hdr").hoverPopup(
        function(e){
            var name = $(this).attr('name');
            return $("li#" + name, hidden_list).html();
        },
        function(e){
            var name = $(this).attr('name');
            $("span." + name).css({"font-weight": "bold", "color": "white"});
            $("li.msg:not(." + name + ")").fadeTo(100, 0.15);
            $("li.msg." + name).fadeTo(50, 1.0);
        },
        function(e){
            var name = $(this).attr('name');
            $("span." + name).css({"font-weight": "normal", "color": "#ddd"});
            $("li.msg").fadeTo(100, 1.0);
        }
    );

    $("li.msg span").hoverPopup(
        function(e){
            return $("li#" + $(this).parent().attr('name'), hidden_list).html();
        },
        function(e){
            var classes = $(this).parent().attr("class").split(" ");
            for (var i=0; i < classes.length; i++) {
                var c = classes[i];
                $("span.hdr[name='" + c +"']").css({"font-weight": "bold", "color": "white"});
            }
        },
        function(e){
            var classes = $(this).parent().attr("class").split(" ");
            for (var i=0; i < classes.length; i++) {
                var c = classes[i];
                $("span.hdr[name='" + c +"']").css({"font-weight": "normal", "color": "#ddd"});
            }
        }
    );

    $("span.hdr").toggle(
        function(){
            var name = $(this).attr('name');
            $("li.msg." + name).slideDown("fast");
            $("li.msg:not('." + name + "')").slideUp("fast");
        },
        function(){
            $("li.msg").slideDown("fast", function(){
                $("li.msg").css('display', 'list-item')
            });
        }
    );

    $("h3").click(function(){
        $(this).next().slideToggle("normal");
    });

    $("a.link_view").click(function(){
        $("#details").html($("#link_list").html());
    });



    /* URI */

    var check_phrase = "Enter a HTTP URI to check";
    var uri = "%(js_uri)s";
    if (uri) {
        $("#uri").val(uri);
    } else if (! $("#uri").val()) {
        $("#uri").val(check_phrase);
        $("#uri").css({'color': '#ccc'});
    }

    $("#uri").focus(function(){
        if ($(this).val() == check_phrase) {
            $(this).val("");
            $("#uri").css({'color': '#111'});
        }
    });



    /* multiple result display */

    $("tr.droid").hoverIntent(
    function(){
        var classes = this.className.split(" ");
        $("li.msg").fadeTo(100, 0.15);
        for (var i=0; i < classes.length; i++) {
            var c = classes[i];
            if (c != 'droid') {
                $("li.msg:eq(" + c +")").fadeTo(50, 1.0);
            }
        }
        if (tid != false) {
            clearTimeout(tid);
            tid = false;
        }
    }, function(){
        tid = setTimeout(function(){
            $("li.msg").fadeTo(50, 1.0);
        }, 100);
    });

    $("span.prob_num").hoverPopup(
        function(e){
            return $(this).children(".hidden").html();
        });

    $("a.preview").hoverPopup(
        function(e){
            var link = (this.title != "") ? this.title : this.href;
            return "<img src='" + link + "'/><br />" + link;
        }
    );



    /* request headers */

    $("#add_req_hdr").click(function(){
        add_req_hdr();
        return false;
    });

    $(".delete_req_hdr").live("click", function(){
        var req_hdr = $(this).closest(".req_hdr");
        req_hdr.remove();
        return false;
    });


    $("select.hdr_name").live("change", function(){
        var req_hdr = $(this).closest(".req_hdr");
        var hdr_name = $(".hdr_name > option:selected", req_hdr).val()
        var hdr_val = "";
        if (hdr_name in known_req_hdrs) {
            if (known_req_hdrs[hdr_name] == null) {
                hdr_val = "<input class='hdr_val' type='text'/>";
            } else {
                hdr_val = "<select class='hdr_val'>";
                for (val in known_req_hdrs[hdr_name]) {
                    hdr_val += "<option>" + known_req_hdrs[hdr_name][val] + "</option>";
                }
                hdr_val += "<option value='other...'>other...</option>";
                hdr_val += "</select>";
            }
            $(".hdr_val", req_hdr).replaceWith(hdr_val);
        } else if (hdr_name == "other...") {
            $(".hdr_name", req_hdr).replaceWith("<input class='hdr_name' type='text'/>");
            $(".hdr_val", req_hdr).replaceWith("<input class='hdr_val' type='text'/>");
        }
    });

    $("select.hdr_val").live("change", function(){
        var req_hdr = $(this).closest(".req_hdr");
        var hdr_name = $(".hdr_name > option:selected", req_hdr).val()
        var hdr_val = "";
        if ($(".hdr_val > option:selected", req_hdr).val() == "other...") {
            $(".hdr_val", req_hdr).replaceWith("<input class='hdr_val' type='text'/>");
        } else {
            hdr_val = $(".hdr_val > option:selected", req_hdr).val();
        }
        $("input[type=hidden]", req_hdr).val(hdr_name + ":" + hdr_val);
    });

    $("input.hdr_name, input.hdr_val").live("change", function() {
        var req_hdr = $(this).closest(".req_hdr");
        var hdr_name = $(".hdr_name", req_hdr).val();
        var hdr_val = $(".hdr_val:text", req_hdr).val();
        $("input[type=hidden]", req_hdr).val(hdr_name + ":" + hdr_val);
    });

    $("input.hdr_name").live("change", function() {
        var req_hdr = $(this).closest(".req_hdr");
        var hdr_name = $(".hdr_name:text", req_hdr).val();
        if (red_req_hdrs.indexOf(hdr_name.toLowerCase()) > -1) {
            alert("The " + hdr_name + " request header is used by RED in its \
tests. Setting it yourself can lead to unpredictable results; please remove it.");
        }
    });
});


function add_req_hdr(hdr_name, hdr_val){
    var hdr_shell = "<div class='req_hdr'>";
    hdr_shell += "<a href='#' class='delete_req_hdr'>x</a> ";
    hdr_shell += "<span class='hdr_name'></span>";
    hdr_shell += ": <span class='hdr_val'></span>";
    hdr_shell += "<input type='hidden' name='req_hdr' value=''/>";
    hdr_shell += "</div>";
    $("#req_hdrs").append(hdr_shell);
    var req_hdr = $("#req_hdrs > .req_hdr:last");
    if (hdr_name == null || hdr_name in known_req_hdrs) {
        var name_html = "<select class='hdr_name'><option/>";
        for (name in known_req_hdrs) {
            if (name == hdr_name) {
                name_html += "<option selected='true'>" + name + "</option>";
            } else {
                name_html += "<option>" + name + "</option>";
            }
        }
        name_html += "<option value='other...'>other...</option>";
        name_html += "</select>";
        $(".hdr_name", req_hdr).replaceWith(name_html);

        if (hdr_name != null) {
            known_hdr_vals = known_req_hdrs[hdr_name];
            if (known_hdr_vals == null) {
                $(".hdr_val", req_hdr).replaceWith('<input class="hdr_val" type="text"/>');
                $(".hdr_val", req_hdr).val(hdr_val);
            } else if (known_hdr_vals.indexOf(hdr_val) >= 0) {
                var val_html = "<select class='hdr_val'>";
                val_html += "<option />";
                for (i in known_hdr_vals) {
                    var val = known_hdr_vals[i];
                    if (hdr_val == val) {
                        val_html += "<option selected='true'>" + val + "</option>";
                    } else {
                        val_html += "<option>" + val + "</option>";
                    }
                }
                val_html += "<option value='other...'>other...</option>";
                val_html += "</select>";
                $(".hdr_val", req_hdr).replaceWith(val_html);
            } else if (hdr_val != null) {
                $(".hdr_val", req_hdr).replaceWith('<input class="hdr_val" type="text"/>');
                $(".hdr_val", req_hdr).val(hdr_val);
            }
            $("input[type=hidden]", req_hdr).val(hdr_name + ":" + hdr_val);
        }
    } else {
        $(".hdr_name", req_hdr).replaceWith('<input class="hdr_name" type="text"/>');
        $(".hdr_name", req_hdr).val(hdr_name);
        $(".hdr_val", req_hdr).replaceWith('<input class="hdr_val" type="text"/>');
        $(".hdr_val", req_hdr).val(hdr_val);
        $("input[type=hidden]", req_hdr).val(hdr_name + ":" + hdr_val);
    }
}

function init_req_hdrs() {
    var req_hdrs = [%(js_req_hdrs)s];
    for (i in req_hdrs) {
        var req_hdr = req_hdrs[i];
        add_req_hdr(req_hdr[0], req_hdr[1]);
    }
    return false;
}


var known_req_hdrs = {
    'Accept-Language': ['', 'en', 'en-us', 'en-uk', 'fr'],
    'Cache-Control': ['', 'no-cache', 'only-if-cached'],
    'Cookie': null,
    'Referer': null,
    'User-Agent': [ "RED/%(version)s (http://redbot.org/about)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; )",
                    "Mozilla/5.0 (X11; U; Linux x86_64; en-US) Gecko Firefox/3.0.8",
                    "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.2.15 Version/10.00",
                  ]
};

var red_req_hdrs = [
    'accept-encoding',
    'if-modified-since',
    'if-none-match',
    'connection',
    'transfer-encoding',
    'content-length'
];

</script>
</head>

<body>

<div id="popup"></div>

<div id='head'>
<div id="request">
    <h1><span class="hilight">R</span>esource <span class="hilight">E</span>xpert <span class="hilight">D</span>roid</h1>

    <form method="GET" onLoad="init_req_hdrs();">
        <input type="url" name="uri" value="%(html_uri)s" id="uri"/><br />
        <div id="req_hdrs"></div>
        <div class="add_req_hdr">
            <a href="#" id="add_req_hdr">add a header</a>
        </div>
    </form>
    <script language="JavaScript">init_req_hdrs();</script>
</div>
"""