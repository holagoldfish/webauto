/* 左侧导航下拉 */
var hiddendivs = $('div.hidden');
var showmore = $('div.showmore');
(function ($) {
    showmore.click(function () {
        $(this).toggleClass('on')
        $(this).nextAll('div.hidden:first').slideToggle(300)
        this.blur();
        return false;
    })

})(jQuery);

/* 页面右侧缩放 */
var temp = 0;
function show_menu() {
    if (temp == 0) {
        $('.left').css({"display": "none"});
        $('.right').css({"margin-left": "0"});
        $('.center').css({"background": "url(img/center2.png)", "margin-left": "13px"});

        temp = 1;
    } else {

        $('.left').css({"display": "block"});
        $('.right').css({"margin-left": "227px"});
        $('.center').css({"background": "url(img/center.png)", "margin-left": "0"});

        temp = 0;
    }
}


/* 新增测试用例页面 新减步骤 */
(function ($) {
    var index = 0;
    $(".show_addmore").click(function () {
        var addstep = index + 1;
        $(".list02 tr:last").after("<tr>" +
        "<td><input type='checkbox' class='checkbox' id='' name='checkbox'></td>" +
        "<td>" + addstep + "</td>" +
        "<td><input type='text' name='step_name' value=''/></td>" +
        "<td><select name='method' id=''><option value=''></option><option value='id'>id</option><option value='name'>name</option><option value='class name'>class name</option><option value='css selector'>css selector</option><option value='xpath'>xpath</option><option value='tag name'>tag name</option><option value='link text'>link text</option></select></td>" +   
        "<td><input type='text' name='element' value=''/></td>" +
        "<td><input type='text' name='value' value=''/></td>" +
        "<td><select name='action' id=''><option value=''></option><option value='输入'>输入</option><option value='单击'>单击</option><option value='鼠标悬停'>鼠标悬停</option><option value='进入iframe'>进入iframe</option><option value='退出iframe'>退出iframe</option><option value='上传导入'>上传导入</option><option value='切换到下一个窗口'>切换到下一个窗口</option><option value='切换到默认窗口'>切换到默认窗口</option><option value='关闭当前窗口'>关闭当前窗口</option><option value='切换到指定窗口'>切换到指定窗口</option><option value='标准断言'>标准断言</option><option value='高级断言'>高级断言</option><option value='模拟回车键'>模拟回车键</option><option value='输入随机数字'>输入随机数字</option><option value='输入随机身份证'>输入随机身份证</option><option value='输入随机字符串'>输入随机字符串</option><option value='执行Linux命令'>执行Linux命令</option><option value='取值'>取值</option><option value='取值断言'>取值断言</option></select></td>" +
        "</tr>");
        index += 1;
        /* $(this).nextAll('ul.addmore:first').toggle(); */
        updateTags();
    });

    $(".show_addmore1").click(function () {
        var addstep = index + 1;
        $(".list02 tr:last").after("<tr>" +
        "<td><input type='checkbox' class='checkbox' id='' name='checkbox'></td>" +
        "<td>" + addstep + "</td>" +
        "<td><input type='text' name='step_name' value=''/></td>" +
        "<td><select name='method' id=''><option value=''></option><option value='id'>id</option><option value='name'>name</option><option value='class name'>class name</option><option value='css selector'>css selector</option><option value='xpath'>xpath</option><option value='tag name'>tag name</option><option value='link text'>link text</option></select></td>" +
        "<td><input type='text' name='element' value=''/></td>" +
        "<td><input type='text' name='value' value=''/></td>" +
        "<td><select name='action' id=''><option value=''></option><option value='输入'>输入</option><option value='单击'>单击</option><option value='鼠标悬停'>鼠标悬停</option><option value='进入iframe'>进入iframe</option><option value='退出iframe'>退出iframe</option><option value='上传导入'>上传导入</option><option value='切换到下一个窗口'>切换到下一个窗口</option><option value='切换到默认窗口'>切换到默认窗口</option><option value='关闭当前窗口'>关闭当前窗口</option><option value='切换到指定窗口'>切换到指定窗口</option><option value='标准断言'>标准断言</option><option value='高级断言'>高级断言</option><option value='模拟回车键'>模拟回车键</option><option value='输入随机数字'>输入随机数字</option><option value='输入随机身份证'>输入随机身份证</option><option value='输入随机字符串'>输入随机字符串</option><option value='执行Linux命令'>执行Linux命令</option><option value='取值'>取值</option><option value='取值断言'>取值断言</option></select></td>" +
        "</tr>");
        index += 1;
        updateTags();
        /* $(this).nextAll('ul.addmore:first').toggle(); */
    });
    $(".delete").click(function () {
        if (index == 0) {
            return false;
        } else {
            $(".list01 tr:last").remove();
            index -= 1;
        }
    });
})(jQuery);


/* 选中删除 */
(function ($) {
    $(".delete_case").click(function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
        $.post("", {'get_id': id_str, btn_name: btn_name}, function (aa, bb) {
            alert(aa);
            location.reload();
            return (aa, bb);
        })
    });

})(jQuery);

(function ($) {
    $(".delete_business").click(function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
        $.post("", {'get_id': id_str, btn_name: btn_name}, function (aa, bb) {
            return (aa, bb);
        })
    });

})(jQuery);

(function ($) {
    $(".delete_perform").click(function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
        $.post("", {'get_id': id_str, btn_name: btn_name}, function (aa, bb) {
            location.reload();
            return (aa, bb);
        })
    });

})(jQuery);


(function ($) {
    $(".delete_mdy_perform").click(function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
    });

})(jQuery);


//input表单焦点获得失去
$("input.foucs_blur").focus(function () {
    if ($(this).val() == this.defaultValue) {
        $(this).val("");
    }
}).blur(function () {
    if ($(this).val() == '') {
        $(this).val(this.defaultValue);
    }
});


/*tab切换*/
function tabs(tabTit, on, tabCon) {
    $(tabCon).each(function () {
        $(this).children().eq(0).show();
    });
    $(tabTit).each(function () {
        $(this).children().eq(0).addClass(on);
    });
    $(tabTit).children().click(function (event) {
        event.stopPropagation();
        $(this).addClass(on).siblings().removeClass(on);
        var index = $(tabTit).children().index(this);
        $(tabCon).children().eq(index).show().siblings().hide();
    });
}
tabs(".tab-head", "active", ".tab-content");


/* 页面弹出框框 */
$(function () {

    $(".addcase_btn").click(function () {
        $(".mask").show();
        showDialog();
        $("#test_cases01").show();

        $("#test_list").empty();
        check_list = $(".checkbox");
        for (i = 0; i < check_list.length; i++) {
            check_list[i].checked = false
        }
        checkbox_case = $(".checkbox_case");
        for (i = 0; i < checkbox_case.length; i++) {
            checkbox_case[i].checked = false
        }

    })

    $(".addcase_btn02").click(function () {
        $(".mask").show();
        showDialog();
        $("#test_cases02").show();
        $("#business_list").empty();
        check_list = $(".checkbox");
        for (i = 0; i < check_list.length; i++) {
            check_list[i].checked = false
        }
        checkbox_case = $(".checkbox_case");
        for (i = 0; i < checkbox_case.length; i++) {
            checkbox_case[i].checked = false
        }
    })

    $(".adduser_btn").click(function () {
        $(".mask").show();
        showDialog();
        $(".user_dialog").show();
    })

    $(".add_pro").click(function () {
        $(".mask").show();
        showDialog();
        $(".pro_dialog").show();
    })
    // 项目管理-新增/编辑项目-添加/修改成员按钮
    $(".addmember").click(function () {
        showDialog();
        $(".moremember_dialog").show();

        // 获取现有项目人员
        name_str = $(".memberlist").text();

        // 获取所有人员对象,通过chebox遍历value值
        check_list = $(".checkbox2").valueOf();

        //遍历人员是否包含在享有项目人员中,如果包含且没勾选就勾选上
        for (i = 0; i < check_list.length; i++) {
            // 先取消所有勾选，再通过对比勾选所需
            check_list[i].checked = false;
            var check_val = check_list[i].value;
            if (name_str.indexOf(check_val) >= 0) {
                if (check_list[i].checked == false) {
                    check_list[i].click();
                }

            }
        }

    })

    /* 添加&修改项目人员 */
    $(".member_save").click(function () {
        var checkbox2 = $(".checkbox2");
        var user = $(".memberlist");
        user.html("");
        var value = new Array();
        var num = 0;
        for (var i = 0; i < checkbox2.length; i++) {
            if (checkbox2[i].checked == true) {
                value[num] = $(".checkbox2").eq(i).parent().siblings('.user').html();
                num++;
            }
        }
        user.html(value.join("，"));
        $(".moremember_dialog").hide();
    })

    /* 项目管理-项目修改 */
    $(".change_pro").click(function () {
        var checkbox = $(".checkbox");
        var id = $(".changepro_dialog .idnum input");
        var member = $(".changepro_dialog .memberlist");
        var proname = $(".changepro_dialog .resetproname input");
        var url = $(".changepro_dialog .resetprourl input");
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                var value1 = $(".checkbox").eq(i).parent().siblings('td.proid').html();//获取项目ID
                var value2 = $(".checkbox").eq(i).parent().siblings('td.member').html();//获取项目人员
                var value3 = $(".checkbox").eq(i).parent().siblings('td.proname').html();//获取项目名称
                var value4 = $(".checkbox").eq(i).parent().siblings('td.prostatus').html();//获取项目状态
                var value5 = $(".checkbox").eq(i).parent().siblings('td.prourl').html();//获取项目地址
                id.attr("value", value1);
                member.html(value2);
                proname.attr("value", value3);
                url.attr("value", value5);
                if (value4 == "进行中") {
                    $("input[name='radiobutton']").eq(0).attr("checked", true);
                } else {
                    $("input[name='radiobutton']").eq(1).attr("checked", true);
                }
                $(".mask").show();
                showDialog();
                $(".changepro_dialog").show();
            }
        }
    })


    $(".resetpwd").click(function () { //重置密码
        var checkbox = $(".checkbox");
        var user = $(".changepwd_dialog form.user input");
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                var value = $(".checkbox").eq(i).parent().siblings('td.username').html();
                user.val(value);
                $(".mask").show();
                showDialog();
                $(".changepwd_dialog").show();
            }
        }
    })


    $(".dialog .addcase_save").click(function () {//注册取消按钮点击事件
        $(".dialog").hide();
        $(".mask").hide();
    })

    $(".dialog .cancel").click(function () {//注册取消按钮点击事件
        $(".dialog").hide();
        $(".mask").hide();
    })

    $(".member_cancel").click(function () {
        $(".moremember_dialog").hide();
    })

    /*根据当前页面与滚动条位置，设置提示对话框的Top与Left*/
    function showDialog() {
        var objW = $(window); //当前窗口
        var objC = $(".dialog"); //对话框
        var brsW = objW.width();
        var brsH = objW.height();
        var sclL = objW.scrollLeft();
        var sclT = objW.scrollTop();
        var curW = objC.width();
        var curH = objC.height();
        //计算对话框居中时的左边距
        var left = sclL + (brsW - curW) / 2;
        //计算对话框居中时的上边距
        var top = sclT + (brsH - curH) / 2;
        //设置对话框在页面中的位置
        objC.css({"left": left, "top": top});
    }

    $(window).resize(function () {//页面窗口大小改变事件
        if (!$(".dialog").is(":visible")) {
            return;
        }
        showDialog(); //设置提示对话框的Top与Left
    });

})


/* 用户管理 */
$(function () {
    var index = 0;
    $(".add_user").click(function () {
        var addstep = index + 1;
        $(".list02 tr:last").after("<tr>" +

        "<td><input type='checkbox' class='checkbox' id='' name=''></td>" +

        "<td>" + addstep + "</td>" +

        "<td class='username'></td>" +

        "<td><input type='password' value='' readonly='readonly'/></td>" +

        "<td></td>" +

        "</tr>");
        index += 1;
    });

})

/* 复选框只能选择一个 */
$(function () {
    var checkbox = $(".usertable .checkbox");
    checkbox.click(function () {
        var num = 0;
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked) {
                num++;
            }
        }
        if (num >= 2) {
            this.checked = false;
            alert("只能选择一条记录！");
        }
    })

});

/* 点击选项获取项目名称 */
//var subtitle = $('div.hidden .subtitle ul li');
//(function ($) {
//    $('div.hidden .subtitle ul li').click(function () {
//        var btn_name = $(this).text();
//        var pro_name = $(this).parents('.hidden').prev('div.showmore').text();
//        location.href = "/add_case?pro_name=" + pro_name;
//        if (btn_name == "新增测试用例") {
//            location.href = "/add_case?pro_name=" + pro_name;
//        }
//        else if (btn_name == "维护测试用例") {
//            location.href = "/case_list?pro_name=" + pro_name;
//        }
//        else if (btn_name == "新增业务流用例") {
//            location.href = "/add_business?pro_name=" + pro_name;
//        }
//        else if (btn_name == "维护业务流用例") {
//            location.href = "/business_list?pro_name=" + pro_name;
//        }
//        else if (btn_name == "新增接口测试用例") {
//           location.href = "/add_inter_case?pro_name="+pro_name;
//        }
//        else if (btn_name == "维护接口测试用例") {
//           location.href = "/modify_inter_case_list?pro_name="+pro_name;
//        }
//
//    })
//
//})(jQuery);


//添加用例的关闭div按钮

$(".close_div").click(function () {
    $("#test_cases01").hide();
    $("#test_cases02").hide();
    $("#mask").hide()
})

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	