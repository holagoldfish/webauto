/**
 * Created by vip on 2015/2/4.
 */
window.onload = function() {
    //绑定事件
    var addEvent = document.addEventListener ? function (el, type, callback) {
        el.addEventListener(type, callback, !1);
    } : function (el, type, callback) {
        el.attachEvent("on" + type, callback);
    }
    //移除事件
    var removeEvent = document.removeEventListener ? function (el, type, callback) {
        el.removeEventListener(type, callback);
    } : function (el, type, callback) {
        el.detachEvent("on" + type, callback);
    }
    //精确获取样式
    var getStyle = document.defaultView ? function (el, style) {
        return document.defaultView.getComputedStyle(el, null).getPropertyValue(style)
    } : function (el, style) {
        style = style.replace(/\-(\w)/g, function ($, $1) {
            return $1.toUpperCase();
        });
        return el.currentStyle[style];
    }
    var dragManager = {
        clientY: 0,
        draging: function (e) {//mousemove时拖动行
            var dragObj = dragManager.dragObj;
            if (dragObj) {
                e = e || event;
                if (window.getSelection) {//w3c
                    window.getSelection().removeAllRanges();
                } else if (document.selection) {
                    document.selection.empty();//IE
                }
                var y = e.clientY;
                var down = y > dragManager.clientY;//是否向下移动
                var tr = document.elementFromPoint(e.clientX, e.clientY);
                if (tr && tr.nodeName == "TD") {
                    tr = tr.parentNode
                    dragManager.clientY = y;
                    if (dragObj !== tr) {
                        tr.parentNode.insertBefore(dragObj, (down ? tr.nextSibling : tr));
                    }
                }
            }
        },
        dragStart: function (e) {
            e = e || event;
            var target = e.target || e.srcElement;
            if (target.nodeName === "TD") {
                target = target.parentNode;
                dragManager.dragObj = target;
                if (!target.getAttribute("data-background")) {
                    var background = getStyle(target, "background-color");
                    target.setAttribute("data-background", background)
                }
                //显示为可移动的状态
                target.style.backgroundColor = "#ccc";
                target.style.cursor = "move";
                dragManager.clientY = e.clientY;
                addEvent(document, "mousemove", dragManager.draging);
                addEvent(document, "mouseup", dragManager.dragEnd);
            }
        },
        dragEnd: function (e) {
            var dragObj = dragManager.dragObj
            if (dragObj) {
                e = e || event;
                var target = e.target || e.srcElement;
                if (target.nodeName === "TD") {
                    target = target.parentNode;
                    dragObj.style.backgroundColor = dragObj.getAttribute("data-background");
                    dragObj.style.cursor = "default";
                    dragManager.dragObj = null;
                    removeEvent(document, "mousemove", dragManager.draging);
                    removeEvent(document, "mouseup", dragManager.dragEnd);
                }
            }
        updateTags()
        },
        main: function (el) {
            addEvent(el, "mousedown", dragManager.dragStart);
        }
    }
    var el = document.getElementById("tb");
    dragManager.main(el);
}
function updateTags() {
    var ck0 = document.getElementsByName("checkbox");
    for (var k = 0; k < ck0.length; k++) {
        var check_td = ck0[k].parentNode;
        var tag_td = check_td.nextSibling;
        tag_td.innerHTML = (k + 1);
    }
}