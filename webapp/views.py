# -.- coding:utf-8 -.-
import sys, time, os

reload(sys)
sys.setdefaultencoding("utf-8")
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import *
from models import *
from runTest import runTest
import logging, datetime, os
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from django.db import connection, transaction
from django.contrib import auth
import threading, json



# log = logging.getLogger()
# log.info(u'项目启动成功')

# LOGDIR = os.getcwd() + "\\log"
#
# LOGFILE = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
# logging.basicConfig(level=logging.DEBUG,
# format='',
# datefmt='%a, %d %b %Y %H:%M:%S',
# filename=os.path.join(LOGDIR, LOGFILE),
# filemode='a'
# )
# fileLog = logging.FileHandler(os.path.join(LOGDIR, LOGFILE), 'w')
# formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s %(message)s')
# fileLog.setFormatter(formatter)
# log = logging.getLogger('admin')
# log.addHandler(fileLog)
# log.setLevel(logging.DEBUG)
# log.info(u'项目已启动：')


def logout_view(request):
    auth.logout(request)
    # return HttpResponse("")


def sql_commend(sql):
    # 封装的自定义sql语句
    cursor = connection.cursor()
    cursor.execute(sql)
    if "select" in sql.lower():
        # 如果是查询，就返回值
        print "当前SQL语句为查询，SQL语句为：%s" % sql

        def dictfechall():
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]

        row = dictfechall()
        return row
    else:
        # 否则就是增 删 改 语句，提交操作
        print "当前SQL语句为执行，SQL语句为：%s" % sql
        transaction.commit_unless_managed()


def get_project_name(request):
    # 通过模糊查询project的用户名得到相应的项目
    login_username = request.user
    project = Project.objects.all()
    project_query = Project.objects.filter(pro_user__contains=login_username)
    project_name = []
    for i in project_query:
        project_name.append(i.name)

    # 获取auth表中的first_name和是否为管理员
    user_object = User.objects.get(username=login_username)
    first_name = user_object.first_name
    is_superuser = user_object.is_superuser
    return project_name, is_superuser, first_name


@login_required
def index(request):
    function_object = get_project_name(request)
    project_name = function_object[0]
    is_superuser = function_object[1]
    first_name = function_object[2]
    return render_to_response("index.html", {"project_name": project_name, "is_superuser": is_superuser,
                                             "first_name": first_name})


def add_case(request):
    if request.method == 'POST':
        # ---当前项目名称---
        current_name = request.POST.get("current_name")
        # ---获取当前项目对象-----
        project_obj = Project.objects.get(name=current_name)
        # ----用例名称、用例性质---------
        case_name = request.POST.get("casename")
        nature = request.POST.get("nature")
        browser = request.POST.get("browser")
        try:
            # -----写入用例表------
            project_obj.case_set.create(name=case_name, browser=browser, case_nature=nature, category='测试用例')
        except:
            return HttpResponse("名称重复")

        try:
            # ----获取用例对象----------
            case_obj = Case.objects.get(name=case_name)
            # -----获取步骤长度--------
            date_length = len(request.POST.getlist('action'))
            # ------循环写入步骤---------
            for i in range(date_length):
                case_obj.case_step_set.create(desc=request.POST.getlist('step_name')[i],
                                              method=request.POST.getlist('method')[i],
                                              element=request.POST.getlist('element')[i],
                                              action=request.POST.getlist('action')[i],
                                              value=request.POST.getlist('value')[i], )

            return HttpResponse("保存成功")
        except:
            return HttpResponse("新增用例失败")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # -------获取当前项目名称,并显示---------
        current_pro_name = request.GET.get("pro_name").strip()
        sql = """select * from webapp_case where project_id=(SELECT id from webapp_project where name="%s")""" % current_pro_name
        case_list = sql_commend(sql=sql)

        return render_to_response("add_case.html", {"project_name": project_name, "is_superuser": is_superuser,
                                                    "first_name": first_name,
                                                    "current_pro_name": current_pro_name,
                                                    "case_list": case_list})


def case_list(request):
    if request.method == 'POST':
        if request.POST.get("btn_name") == u"删除用例":
            get_id = request.POST.getlist("get_id[]")
            for i in get_id:
                filter_business_stp = Business_stp.objects.filter(case_id=i)
                fileter_Execution_detail = Execution_detail.objects.filter(case_id=i)

                if bool(filter_business_stp) and bool(fileter_Execution_detail):
                    case_name = filter_business_stp[0].name
                    business_name = Business.objects.get(pk=(filter_business_stp[0].business_id)).name
                    execution_name = Test_execution.objects.get(pk=(fileter_Execution_detail[0].perform_id)).name
                    return HttpResponse(u"1、用例:‘%s’存在与业务流:‘%s’中\n2、存在与测试执行:‘%s’中\n3、请先在业务流和测试执行中删除该用例" % (
                        case_name, business_name, execution_name))

                elif bool(filter_business_stp) == True and bool(fileter_Execution_detail) == False:
                    case_name = filter_business_stp[0].name
                    business_name = Business.objects.get(pk=(filter_business_stp[0].business_id)).name
                    return HttpResponse(u"1、用例:‘%s’存在与业务流:'%s'中\n2、请先在业务流中删除该用例" % (case_name, business_name))

                elif bool(fileter_Execution_detail) == True and bool(filter_business_stp) == False:
                    case_name = fileter_Execution_detail[0].name
                    execution_name = Test_execution.objects.get(pk=(fileter_Execution_detail[0].perform_id)).name
                    return HttpResponse(u"1、用例:‘%s’存在与测试执行:'%s'中\n2、请先在测试执行中删除该用例" % (case_name, execution_name))
                else:
                    # 删除用例步骤
                    try:
                        del_step = "DELETE from webapp_case_process where case_id= %s" % i
                        sql_commend(del_step)
                        print u"删除步骤成功，当前用例ID是%s" % i
                    except:
                        print u"删除步骤失败，当前用例ID是%s" % i

                    # 删除测试用例
                    try:
                        del_case = "DELETE from webapp_case where id= %s" % i
                        sql_commend(del_case)
                        print u"删除用例成功，当前用例ID是%s" % i
                    except:
                        print u"删除用例失败，当前用例ID是%s" % i

        if request.POST.get("btn_name") == u"测试调试":
            # 取ID
            case_id = request.POST.get("case_id")  # 点击测试调试，返回用例的ID

            # 取名称
            get_name = Case.objects.get(pk=case_id)
            case_name = str(get_name.name)
            # 取IP
            regip = get_client_ip(request)

            runTest(regip, 'case', case_id, case_name)
            return HttpResponse("请确认打开调试客户端")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # 点击查询的form传过来的GET值
        case_id = request.GET.get("c_id")  # ID查询值
        case_name = request.GET.get("c_nm")  # 名称查询值
        case_nature = request.GET.get("select")  # 案例性质查询值

        if case_id or case_name or case_nature:  # 判断这三个值存在则做查询动作，否则做默认的GET动作
            current_project = request.GET.get("cur_pro_name")
            pro_id = Project.objects.get(name=current_project).id
            if case_id:  # 如果有ID，做唯一查询，忽略其他条件
                case_list = Case.objects.filter(project_id=pro_id, pk=case_id)
            else:
                if case_nature:  # 如果案例性质为真，组合名称查询
                    case_list = Case.objects.filter(project_id=pro_id, name__contains="%s" % case_name,
                                                    case_nature="%s" % case_nature)
                else:  # 如果为假，单一查询
                    case_list = Case.objects.filter(project_id=pro_id, name__contains="%s" % case_name)
        else:
            # -----当前项目名称----------
            try:
                # 尝试通过2中方式获取项目名称，容错查询值都为空时会报错
                current_project = request.GET.get("pro_name").strip()
            except:
                current_project = request.GET.get("cur_pro_name")
            # ------获取关联项目id--------
            project_id = Project.objects.get(name=current_project).id
            # 通过关联项目id获取所有的用例列表
            case_list = Case.objects.filter(project_id=project_id)

        return render_to_response("case_list.html",
                                  {"contacts": case_list, "project_name": project_name, "is_superuser": is_superuser,
                                   "first_name": first_name, "current_project": current_project},
                                  context_instance=RequestContext(request))


def modify_case(request):
    if request.method == "POST":
        # 通过id获取项目对象
        project_obj = Project.objects.get(pk=int(request.POST.get("project_id")))

        # 取测试用例ID
        case_id = request.POST.get("case_id")
        # 获取用例对象和POST到的案例名称和性质
        case_obj = project_obj.case_set.get(pk=case_id)
        name = request.POST.get("casename")
        case_nature = request.POST.get("nature")
        browser = request.POST.get("browser")
        try:
            case_obj.name = name
            case_obj.case_nature = case_nature
            case_obj.browser = browser
            case_obj.save()
            print u'写入测试用例名称为：%s\n案例性质是:%s' % (name, case_nature)
        except:
            return HttpResponse("名称重复")

        # 获取POST数据的长度
        req_length = len(request.POST.getlist("value"))
        # 获取当前用例在数据库中的长度，跟POST做长度对比。
        all_stp = case_obj.case_step_set.count()

        # 获取所有步骤值
        stp_val = case_obj.case_step_set.values()

        # 判断长度修改步骤，放弃值钱的全部删除再写入方法
        # 当数据长度和数据库长度一致时，修改。大于则增加，小于则删除多余数据
        if req_length == all_stp:
            num = -1
            for i in stp_val:
                # 遍历测试步骤所有值，取ID，写入相应值
                num += 1
                stp_id = int(i.get("id"))
                stp_object = case_obj.case_step_set.get(pk=stp_id)
                stp_object.desc = request.POST.getlist("step_name")[num]
                stp_object.method = request.POST.getlist("method")[num]
                stp_object.element = request.POST.getlist("element")[num]
                stp_object.action = request.POST.getlist("action")[num]
                stp_object.value = request.POST.getlist("value")[num]
                stp_object.save()

        if req_length > all_stp:
            # 去数据库中的ID和长度
            stp_id_tmp = []
            for nn in stp_val:
                get_id = nn.get("id")
                stp_id_tmp.append(get_id)

            for i in range(req_length):
                try:
                    # 尝试更新数据库内容，当超出时候则创建
                    stp = case_obj.case_step_set.get(pk=int(stp_id_tmp[i]))

                    stp.desc = request.POST.getlist('step_name')[i]
                    stp.method = request.POST.getlist("method")[i]
                    stp.element = request.POST.getlist("element")[i]
                    stp.action = request.POST.getlist("action")[i]
                    stp.value = request.POST.getlist("value")[i]
                    stp.save()
                except:
                    case_obj.case_step_set.create(desc=request.POST.getlist('step_name')[i],
                                                  method=request.POST.getlist("method")[i],
                                                  element=request.POST.getlist("element")[i],
                                                  action=request.POST.getlist("action")[i],
                                                  value=request.POST.getlist("value")[i], )

        if req_length < all_stp:
            stp_id_tmp = []
            for nn in stp_val:
                get_id = nn.get("id")
                stp_id_tmp.append(get_id)
            for i in range(req_length):
                stp = case_obj.case_step_set.get(pk=int(stp_id_tmp[i]))
                stp.desc = request.POST.getlist('step_name')[i]
                stp.method = request.POST.getlist("method")[i]
                stp.element = request.POST.getlist("element")[i]
                stp.action = request.POST.getlist("action")[i]
                stp.value = request.POST.getlist("value")[i]
                stp.save()

            # 计算差，得到多余的ID。删除相应数据
            del_data = stp_id_tmp[req_length:all_stp]
            for i in del_data:
                del_dd = Case_step.objects.get(pk=int(i))
                del_dd.delete()
        return HttpResponse("修改成功")

    if request.method == "GET":
        # 获取用例ID
        case_id = request.GET.get("name")

        # 获取用例对象
        case_obj = Case.objects.get(pk=int(case_id))
        # 获取用例步骤
        casestp = case_obj.case_step_set.all()

        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]
        # -----通过用例ID获取项目ID,并传到html中隐藏的button的value值----------
        project_id = case_obj.project_id

        # 获取项目名称
        current_project_name = Project.objects.get(pk=project_id).name
        sql = """select * from webapp_case where project_id=(SELECT id from webapp_project where name="%s")""" % current_project_name
        case_list = sql_commend(sql=sql)

        return render_to_response("modify_case.html",
                                  {"casename": case_obj, "casestep": casestp, "project_name": project_name,
                                   "is_superuser": is_superuser,
                                   "first_name": first_name,
                                   "project_id": project_id,
                                   "current_project_name": current_project_name,
                                   "case_list": case_list,
                                   })


def add_business(request):
    if request.method == "POST":
        # 取当前项目名称和对象
        current_project_name = request.POST.get("current_pro_name")
        project_object = Project.objects.get(name=current_project_name)

        # 获取业务流名称
        business_name = request.POST.get("ywlname")

        # 写业务流名称到数据库
        project_object.business_set.create(name=business_name, category='业务流用例')
        # 取该业务流对象
        business_stp = project_object.business_set.get(name=business_name)

        # 写入业务流详细
        case_id = request.POST.getlist("case_id")
        case_name = request.POST.getlist("case_name")
        case_date = request.POST.getlist("case_date")
        case_nature = request.POST.getlist("case_nature")
        if case_name:
            for i in range(len(case_name)):
                business_stp.business_stp_set.create(name=case_name[i],
                                                     date=case_date[i],
                                                     case_nature=case_nature[i],
                                                     case_id=case_id[i])

        return HttpResponse("保存成功")

    if request.method == "GET":
        # --获取当前项目名称，已经改项目下的所有用例-----
        current_pro_name = request.GET.get("pro_name").strip()
        project_obj = Project.objects.get(name=current_pro_name)
        # case_list = project_obj.case_set.all()

        # 获取当前用户下的所有项目
        user_name = request.user
        project_obj = Project.objects.filter(pro_user__contains=user_name)


        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]
        return render_to_response("add_business.html",
                                  {"project_obj": project_obj, "project_name": project_name,
                                   "current_pro_name": current_pro_name,
                                   "is_superuser": is_superuser, "first_name": first_name})


def business_list(request):
    if request.method == "POST":
        if request.POST.get("btn_name") == u"删除业务流":
            get_id = request.POST.getlist("get_id[]")
            for i in get_id:
                filter_Execution_detail = Execution_detail.objects.filter(business_id=i)
                if filter_Execution_detail:
                    case_name = filter_Execution_detail[0].name
                    execution_name = Test_execution.objects.get(pk=filter_Execution_detail[0].perform_id).name
                    return HttpResponse(u"1、业务流:‘%s’存在与测试执行:'%s'中\n2、请先在测试执行中删除该用例" % (case_name, execution_name))
                else:
                    Business.objects.get(pk=i).delete()
                    Business_stp.objects.filter(business_id=i).delete()



        else:
            # 取ID
            business_id = request.POST.get("business_id")
            # 点击测试调试，返回用例的ID

            # 取名称
            get_name = Business.objects.get(pk=business_id)
            business_name = str(get_name.name)

            # 取IP
            regip = get_client_ip(request)

            # log.info(u'连接的客户端ip是:%s，当前用例ID是:%s' % (regip, business_id))
            runTest(regip, "business", business_id, business_name)

            return HttpResponse("请确认打开调试客户端")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # ----获取当前项目名称和改项目下所有的业务流------
        current_pro_name = request.GET.get("pro_name").strip()
        business_name = Project.objects.get(name=current_pro_name).business_set.all()

        return render_to_response("business_list.html", {"business_name": business_name, "project_name": project_name,
                                                         "is_superuser": is_superuser, "first_name": first_name,
                                                         "current_pro_name": current_pro_name},
                                  context_instance=RequestContext(request))


def case_ajax(request):
    if request.method == "POST":
        stp_list = []
        case_id = request.POST.getlist("id[]")
        for i in case_id:
            case_stp = Case.objects.get(pk=i).case_process_set.all()
            stp_list.extend(case_stp)
        return render_to_response("add_case_ajax.html", {"case_stp": stp_list})

    return render_to_response("add_case_ajax.html")


def business_ajax(request):
    if request.method == "POST":
        case_set = []
        case_id = request.POST.getlist("id[]")

        for i in case_id:
            case_obj = Case.objects.get(pk=i)
            case_set.append(case_obj)

        return render_to_response("business_ajax.html", {"case_set": case_set})

    return render_to_response("business_ajax.html")


def modify_business(request):
    if request.POST:
        business_id = request.POST.get("business_id")
        name = request.POST.get("ywlname")

        case_name = request.POST.getlist("case_name")
        case_date = request.POST.getlist("case_date")
        case_nature = request.POST.getlist("case_nature")
        case_id = request.POST.getlist("case_id")

        # 写业务流名称
        try:
            bus_obj = Business.objects.get(pk=business_id)
            bus_obj.name = name
            bus_obj.save()
        except:
            return HttpResponse("名称重复")

        # 取POST数据库长度
        post_length = len(case_name)

        # 取当前业务流步骤的长度
        bus_stp_length = bus_obj.business_stp_set.count()

        # 取所有步骤，循环修改
        stp_val = bus_obj.business_stp_set.values()
        if post_length == bus_stp_length:
            # POST数据长度与数据库中一直，则直接修改数据库,遍历测试步骤所有值，取ID，写入相应值
            num = -1
            for i in stp_val:
                num += 1
                stp_id = int(i.get("id"))
                stp_object = Business_stp.objects.get(pk=stp_id)
                stp_object.name = case_name[num]
                stp_object.date = case_date[num]
                stp_object.case_nature = case_nature[num]
                stp_object.case_id = case_id[num]
                stp_object.save()
        if post_length > bus_stp_length:
            # POST数据长度大于数据库时，修改数据库长多，超过部分做写入
            # 去数据库中的ID和长度

            stp_id_tmp = []
            for nn in stp_val:
                get_id = nn.get("id")
                stp_id_tmp.append(get_id)
            for i in range(post_length):
                try:
                    # 尝试更新数据库内容，当超出时候则创建
                    stp = Business_stp.objects.get(pk=stp_id_tmp[i])
                    stp.name = case_name[i]
                    stp.date = case_date[i]
                    stp.case_nature = case_nature[i]
                    stp.case_id = case_id[i]
                    stp.save()
                except:
                    bus_obj.business_stp_set.create(name=case_name[i],
                                                    date=case_date[i],
                                                    case_nature=case_nature[i],
                                                    case_id=case_id[i])
        if post_length < bus_stp_length:
            # POST数据小于数据库时，修改数据库。数据库多余部分做删除操作
            stp_id_tmp = []
            for nn in stp_val:
                get_id = nn.get("id")
                stp_id_tmp.append(get_id)
            for i in range(post_length):
                stp = Business_stp.objects.get(pk=stp_id_tmp[i])
                stp.name = case_name[i]
                stp.date = case_date[i]
                stp.case_nature = case_nature[i]
                stp.case_id = case_id[i]
                stp.save()

            # 计算差，得到多余的ID。删除相应数据
            del_data = stp_id_tmp[post_length:bus_stp_length]

            for i in del_data:
                del_dd = Business_stp.objects.get(pk=int(i))
                del_dd.delete()
        return HttpResponse("修改成功")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]


        # ----通过GET方式获取到业务流的id------
        business_id = request.GET.get("business_id")

        # ---通过id获取业务流对象-----

        business_obj = Business.objects.get(pk=business_id)
        # -- 通过获取的业务流对象获current_pro_name取项目ID----------
        project_id = business_obj.Project_id

        # 获取当前项目名称
        current_pro_name = Project.objects.get(pk=project_id).name


        # ---通过业务流对象获取对应的步骤------
        business_stp = business_obj.business_stp_set.all()

        # 获取当前用户下的所有项目
        user_name = request.user
        project_obj = Project.objects.filter(pro_user__contains=user_name)

        return render_to_response("modify_business.html",
                                  {"project_obj": project_obj, "project_name": project_name,
                                   "is_superuser": is_superuser,
                                   "first_name": first_name, "project_id": project_id, "business_obj": business_obj,
                                   "business_stp": business_stp, "current_pro_name": current_pro_name,
                                   "business_id": business_id})


def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip


def use_case_management(request):
    # 用例和业务流TAB切换页面，暂未启用
    if request.method == 'POST':
        csts = request.POST.values()[0]
        if csts == "用例调试":
            # 取ID
            case_id = request.POST.dict().keys()[0]  # 点击测试调试，返回用例的ID

            # 取名称
            get_name = Case.objects.get(pk=case_id)
            case_name = str(get_name.name)

            # 取IP
            regip = get_client_ip(request)

            # log.info(u'连接的客户端ip是:%s，当前用例ID是:%s' % (regip, case_id))
            runTest(regip, 'case', case_id, case_name)
            return HttpResponseRedirect("/use_case_management/")

        if csts == '业务流调试':
            # 取ID
            business_id = request.POST.dict().keys()[0]  # 点击测试调试，返回用例的ID

            # 取名称
            get_name = Business.objects.get(pk=business_id)
            business_name = str(get_name.name)

            # 取IP
            regip = get_client_ip(request)

            # log.info(u'连接的客户端ip是:%s，当前用例ID是:%s' % (regip, business_id))
            runTest(regip, "business", business_id, business_name)

            return HttpResponseRedirect("/use_case_management/")
    if request.method == "GET":
        all_case = Case.objects.all()
        all_business = Business.objects.all()
        return render_to_response("use_case_management.html", {"all_case": all_case, "all_business": all_business},
                                  context_instance=RequestContext(request))


def add_perform(request):
    # 增加测试执行
    if request.method == "POST":
        # 获取用户名，取用户表对象
        print request.POST

        user_obj = User.objects.get(username=request.POST.get("user_name"))
        try:
            # 通过用户表对象创建执行表
            user_obj.test_execution_set.create(name=request.POST.get('perform_n'))
        except:
            return HttpResponse("名称重复")

        # 获取执行表对象
        perform_detail = Test_execution.objects.get(name=request.POST.get('perform_n'))

        # 获取长度
        date_len = len(request.POST.getlist("date"))

        # 根据长度循环写入到执行详细表中
        for i in range(date_len):
            name_list = request.POST.getlist("name")
            case_nature_list = request.POST.getlist("case_nature")
            category_list = request.POST.getlist("category")
            if category_list[i] == u"测试用例":
                case_id_list = request.POST.getlist("case_id")

                perform_detail.execution_detail_set.create(name=name_list[i],
                                                           case_nature=case_nature_list[i],
                                                           category=category_list[i],
                                                           case_id=case_id_list[i])

            if category_list[i] == u"业务流用例":
                business_id = request.POST.getlist("case_id")
                perform_detail.execution_detail_set.create(name=name_list[i],
                                                           case_nature=case_nature_list[i],
                                                           category=category_list[i],
                                                           business_id=business_id[i])

        return HttpResponse("保存成功")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # 获取当前登录用户名，筛选改用户下所有项目中的所有用例和业务流
        user_name = request.user
        project_obj = Project.objects.filter(pro_user__contains=user_name)

        return render_to_response("add_perform.html", {"project_name": project_name,
                                                       "is_superuser": is_superuser, "first_name": first_name,
                                                       "user_name": user_name,
                                                       "project_obj": project_obj})


def perform_ajax(request):
    # 测试执行A-Jax页面，为新增提供ajax动态
    if request.method == "POST":
        case_id_list = request.POST.getlist("case[]")
        business_id_list = request.POST.getlist("business[]")

        perform_list = []
        if case_id_list:
            for i in case_id_list:
                case_name = Case.objects.filter(pk=i)
                perform_list.extend(case_name)

        if business_id_list:
            for i in business_id_list:
                case_name = Business.objects.filter(pk=i)
                perform_list.extend(case_name)

        return render_to_response("perform_ajax.html", {"perform_list": perform_list})

    return render_to_response("perform_ajax.html")


def perform_list(request):
    if request.method == "POST":
        btn_name = request.POST.get("btn_name")
        if btn_name == u"删除执行":
            get_id = request.POST.getlist("get_id[]")
            for i in get_id:
                # 删除执行中的用例和业务流
                del_step = "DELETE from webapp_execution_detail where perform_id= %s" % i
                sql_commend(del_step)

                # 删除执行
                del_case = "DELETE from webapp_test_execution where id= %s" % i
                sql_commend(del_case)
        if btn_name == u"测试调试":
            # 取ID
            case_id = request.POST.get("case_id")
            # 取名称
            get_name = Test_execution.objects.get(pk=case_id)
            case_name = str(get_name.name)

            # 取客户端IP
            regip = get_client_ip(request)

            # 多线程启动客户端和服务端代码
            def run_key():
                print "开始运行服务端自动化框架"
                # os.system(r"D:\Project\autotest\webapp\run_automation.bat")

            threads = []
            t1 = threading.Thread(target=run_key)
            threads.append(t1)
            t2 = threading.Thread(runTest(regip, "perform", case_id, case_name))
            threads.append(t2)

            for i in threads:
                print "start threading"
                i.setDaemon(True)
                i.start()
            i.join()

            return HttpResponse("请确认打开调试客户端")
    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # 获取当前用户，以及当前用户下所有的执行
        user = request.user
        user_obj = User.objects.get(username=user)

        # 获取所有执行的用例和业务流并分页
        user_perform = user_obj.test_execution_set.all()

        return render_to_response("perform_list.html", {"user_perform": user_perform, "project_name": project_name,
                                                        "is_superuser": is_superuser, "first_name": first_name},
                                  context_instance=RequestContext(request))


def modify_perform(request):
    if request.method == "POST":
        # 取执行id
        perform_id = request.POST.get("perform_id")
        perform_obj = Test_execution.objects.get(pk=perform_id)
        # 修改perform name
        try:
            perform_obj.name = request.POST.get("perform_n")
            perform_obj.save()
        except:
            return HttpResponse("名称与数据库中重复")

        # 取POST数据长度
        req_length = len(request.POST.getlist("name"))
        # 取原来数据长度与POST数据对比
        detail_len = perform_obj.execution_detail_set.count()
        # 取步骤数据
        detail_val = perform_obj.execution_detail_set.values()
        if req_length == detail_len:
            # POST数据长度与数据库中一直，则直接修改数据库
            num = -1
            for i in detail_val:
                # 遍历测试步骤所有值，取ID，写入相应值
                num += 1
                detail_id = int(i.get("id"))
                detail_object = Execution_detail.objects.get(pk=detail_id)
                if request.POST.getlist("category")[num] == u"测试用例":
                    detail_object.name = request.POST.getlist("name")[num]
                    detail_object.case_nature = request.POST.getlist("case_nature")[num]
                    detail_object.category = request.POST.getlist("category")[num]
                    detail_object.case_id = request.POST.getlist("case_id")[num]
                    detail_object.business_id = ""
                    detail_object.save()

                if request.POST.getlist("category")[num] == u"业务流用例":
                    detail_object.name = request.POST.getlist("name")[num]
                    detail_object.case_nature = request.POST.getlist("case_nature")[num]
                    detail_object.category = request.POST.getlist("category")[num]
                    detail_object.business_id = request.POST.getlist("case_id")[num]
                    detail_object.case_id = ""
                    detail_object.save()

        if req_length > detail_len:
            # POST数据长度大于数据库时，修改数据库长多，超过部分做写入
            # 去数据库中的ID和长度
            stp_id_tmp = []
            for nn in detail_val:
                get_id = nn.get("id")
                stp_id_tmp.append(get_id)

            for i in range(req_length):
                try:
                    # 尝试更新数据库内容，当超出时候则创建
                    detail_object = Execution_detail.objects.get(pk=int(stp_id_tmp[i]))
                    if request.POST.getlist("category")[i] == u"测试用例":
                        detail_object.name = request.POST.getlist('name')[i]
                        detail_object.case_nature = request.POST.getlist("case_nature")[i]
                        detail_object.category = request.POST.getlist("category")[i]
                        detail_object.case_id = request.POST.getlist("case_id")[i]
                        detail_object.save()

                    if request.POST.getlist("category")[i] == u"业务流用例":
                        detail_object.name = request.POST.getlist('name')[i]
                        detail_object.case_nature = request.POST.getlist("case_nature")[i]
                        detail_object.category = request.POST.getlist("category")[i]
                        detail_object.business_id = request.POST.getlist("case_id")[i]
                        detail_object.save()
                except:
                    if request.POST.getlist("category")[i] == u"测试用例":
                        perform_obj.execution_detail_set.create(name=request.POST.getlist('name')[i],
                                                                case_nature=request.POST.getlist("case_nature")[i],
                                                                category=request.POST.getlist("category")[i],
                                                                case_id=request.POST.getlist("case_id")[i])

                    if request.POST.getlist("category")[i] == u"业务流用例":
                        perform_obj.execution_detail_set.create(name=request.POST.getlist('name')[i],
                                                                case_nature=request.POST.getlist("case_nature")[i],
                                                                category=request.POST.getlist("category")[i],
                                                                business_id=request.POST.getlist("case_id")[i])
        if req_length < detail_len:
            # POST数据长度小于数据库长度时，循环POST修改数据库。多处部分切片删除

            stp_id_tmp = []
            for nn in detail_val:
                get_id = nn.get("id")
                stp_id_tmp.append(get_id)
            for i in range(req_length):
                detail_object = Execution_detail.objects.get(pk=int(stp_id_tmp[i]))
                if request.POST.getlist("category")[i] == u"测试用例":
                    detail_object.name = request.POST.getlist('name')[i]
                    detail_object.case_nature = request.POST.getlist("case_nature")[i]
                    detail_object.category = request.POST.getlist("category")[i]
                    detail_object.case_id = request.POST.getlist("case_id")[i]
                    detail_object.save()

                if request.POST.getlist("category")[i] == u"业务流用例":
                    detail_object.name = request.POST.getlist('name')[i]
                    detail_object.case_nature = request.POST.getlist("case_nature")[i]
                    detail_object.category = request.POST.getlist("category")[i]
                    detail_object.business_id = request.POST.getlist("case_id")[i]
                    detail_object.save()

            # 切片计算差，得到多余的ID。遍历删除相应数据
            del_data = stp_id_tmp[req_length:detail_len]
            for i in del_data:
                del_dd = Execution_detail.objects.get(pk=int(i))
                del_dd.delete()

        return HttpResponse("修改成功")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        perform_id = request.GET.dict().keys()[0]
        perform_object = Test_execution.objects.get(pk=int(perform_id))
        perform_detail = perform_object.execution_detail_set.all()



        # 获取当前登录用户名，筛选改用户下所有项目中的所有用例和业务流
        user_name = request.user
        project_obj = Project.objects.filter(pro_user__contains=user_name)
        return render_to_response("modify_perform.html", {"perform_object": perform_object,
                                                          "perform_detail": perform_detail,
                                                          "project_obj": project_obj,
                                                          "perform_id": perform_id,
                                                          "project_name": project_name,
                                                          "is_superuser": is_superuser,
                                                          "first_name": first_name})


def user_management(request):
    if request.method == "POST":
        if request.POST.get("btn_add") == u"新增用户":
            add_user = request.POST["add_user"]
            password = request.POST["password"]
            first_name = request.POST["first_name"]
            status = request.POST["chest"]
            make_pw = make_password(password, None, hasher="default")
            User.objects.create(username=add_user, password=make_pw, first_name=first_name, is_staff=status,
                                is_active=status)

        if request.POST.get("btn_add") == u"重置密码":
            user_name = request.POST.get("user")
            get_user = request.user.username
            passwd = request.POST.get("passwd")
            user_obj = User.objects.get(username=user_name)
            user_obj.set_password(passwd)
            user_obj.save()
            if get_user == user_name:
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect(request.path)

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]


        # 获取用户表auth_user对象,并做分页功能
        user = User.objects.all()

        return render_to_response("user_management.html",
                                  {"user": user, "project_name": project_name, "is_superuser": is_superuser,
                                   "first_name": first_name}, context_instance=RequestContext(request))


def project_management(request):
    if request.POST:
        btn_name = request.POST.get("btn_name")

        if btn_name == u"新增项目":
            post_url = request.POST.get("url")
            post_pro_name = request.POST.get("pro_name")
            post_user_name = request.POST.get("user_name")
            post_select_val = request.POST.get("select_val")
            Project.objects.create(name=post_pro_name, url=post_url, pro_user=post_user_name,
                                   pro_status=post_select_val)

        if btn_name == u"删除项目":
            post_pro_id = request.POST.get("pro_id")
            Project.objects.get(pk=post_pro_id).delete()

        if btn_name == u"编辑项目":
            post_pro_id = int(request.POST.get("pro_id"))
            post_url = request.POST.get("url")

            print post_url
            post_pro_name = request.POST.get("pro_name")
            post_user_name = request.POST.get("user_name")
            post_check_status = request.POST.get("chest")
            # 通过ID获取到项目对象，对值做修改
            project_ob = Project.objects.get(pk=post_pro_id)
            # 多项赋值进行修改
            project_ob.name, project_ob.pro_user, project_ob.pro_status, project_ob.url = post_pro_name, post_user_name, post_check_status, post_url
            project_ob.save()

        project_list = Project.objects.all()
        user_list = User.objects.all()
        return render_to_response("project_management.html", {"project_list": project_list, "user_list": user_list})

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # 获取所有用户列表
        user_list = User.objects.all()
        # 获取所有项目列表，并做分页
        project_list = Project.objects.all()
        return render_to_response("project_management.html", {"project_list": project_list,
                                                              "user_list": user_list,
                                                              "project_name": project_name,
                                                              "is_superuser": is_superuser,
                                                              "first_name": first_name},
                                  context_instance=RequestContext(request))


def method_ajax(request):
    # 加载定位方法，用于维护页面的jquery页面加载事件。
    method_by = Method.objects.all()
    return render_to_response("method_ajax.html", {"method": method_by})


def action_ajax(request):
    # 加载定位方法，用于维护页面的jquery页面加载事件。
    Action_fun = Action.objects.all()
    return render_to_response("action_ajax.html", {"action": Action_fun})


def base(request):
    if request.method=="POST":
        print request.POST
        return HttpResponse("你现在给的是一个POST请求")

    return render_to_response("Base.html")


def report(request):
    if request.method == "GET":
        result_list = Test_report.objects.all()

        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]
        return render_to_response("result.html", {"result_list": result_list,
                                                  "project_name": project_name,
                                                  "is_superuser": is_superuser,
                                                  "first_name": first_name}, context_instance=RequestContext(request))


def report_html(request, html_name):
    if html_name.endswith(".png"):
        # 通过url获取到的动态参数，如果为png则打开图片
        img_path = os.getcwd() + "\\templates\\result\\" + html_name
        ime_date = open(img_path, "rb").read()
        return HttpResponse(ime_date, content_type="image/png")
    else:
        # 否则获取到的就是.html文件，则渲染html
        return render_to_response(u"result\%s" % html_name)


def perform_case_ajax(request):
    """新增执行中添加用例的ajax"""
    if request.method == "POST":
        case_type = request.POST.get("type")

        if case_type == "business":
            print "当前类型为 业务流"
            pro_id = request.POST.get("pro_id")
            case_list = Business.objects.filter(Project_id=pro_id)
            print "当前项目所有业务流是:%s" % case_list
        if case_type == "case":
            pro_id = request.POST.get("pro_id")
            case_list = Case.objects.filter(project_id=pro_id)

        return render_to_response("case_list_ajax.html", {"case_list": case_list})
    return render_to_response("case_list_ajax.html")

def add_element(request):

    if request.method == "POST":
        btn_name = request.POST.get("btn_name")
        # 取POST的值
        e_name = request.POST.get("name")
        e_function = request.POST.get("function")
        e_value = request.POST.get("value")
        e_page_url = request.POST.get("page_url")
        e_desc = request.POST.get("desc")

        if btn_name == u"删除元素":
            check_id = request.POST.getlist("check_id[]")
            for i in check_id:
                element.objects.get(pk=i).delete()

        if btn_name == u"修改元素":
            # 取当前项目为对象
            pro_name = request.POST.get("pro_name").strip()
            ele_id = request.POST.get("ele_id")
            ele_obj = Project.objects.get(name=pro_name).element_set.get(pk=ele_id)
            ele_obj.name = e_name
            ele_obj.fun = e_function
            ele_obj.values = e_value
            ele_obj.desc = e_desc
            ele_obj.page_url = e_page_url
            ele_obj.save()

        if btn_name == u"添加元素":
            print request.POST
            pro_name = request.POST.get("pro_name").strip()
            cur_pro_obj = Project.objects.get(name=pro_name)
            cur_pro_obj.element_set.create(name=e_name, fun=e_function, values=e_value, desc=e_desc, page_url=e_page_url)


        return HttpResponseRedirect("/add_element/?pro_name="+pro_name)

    if request.method == "GET":
        print request.GET
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]
        pro_name = request.GET.get("pro_name").strip()
        fun = Method.objects.all()

        if request.GET.get("tag") == "查询":
            sec_id = request.GET.get("sec_id")
            sec_name = request.GET.get("sec_name")
            sec_url = request.GET.get("sec_url")
            sec_val = request.GET.get("sec_val")
            pro_id = Project.objects.get(name=pro_name).id
            if sec_id:
                element_list =element.objects.filter(project_id=pro_id,pk=sec_id)
            else:
                element_list = element.objects.filter(project_id=pro_id,name__contains=sec_name,page_url__contains=sec_url,values__contains=sec_val)
        else:
            element_list = Project.objects.get(name=pro_name).element_set.all()

        return render_to_response("add_element.html", {"project_name": project_name, "is_superuser": is_superuser,
                                                       "first_name": first_name,
                                                       "current_pro_name":pro_name,
                                                       "fun":fun,
                                                       "element_list":element_list},context_instance=RequestContext(request))
def process_ajax(request):
    """增加步骤"""
    action = Action.objects.all()
    return render_to_response("process_ajax.html",{"action":action})

def element_msg(request):
    ele_id = request.POST.get("ele_id")
    element_obj =element.objects.get(pk=ele_id)
    return render_to_response("element_msg.html", {"element_obj":element_obj})

def element_list_ajax(request):
    cur_pro_name  = request.POST.get("current_pro_name")
    pro_id = Project.objects.get(name=cur_pro_name).id
    tag = request.POST.get("tag")
    sec_id = request.POST.get("sec_id")
    sec_name = request.POST.get("sec_name")
    sec_url = request.POST.get("sec_url")
    sec_val = request.POST.get("sec_val")


    if tag == u"查询":
        print u"开始查询元素列表功能"
        if sec_id:
            ele_list =element.objects.filter(project_id=pro_id,pk=sec_id)
        else:
            ele_list = element.objects.filter(project_id=pro_id,name__contains=sec_name,page_url__contains=sec_url,values__contains=sec_val)

        return render_to_response("element_list_ajax.html",{"ele_list":ele_list})

    else:
        # 根据不同的项目获取该项目下所有的元素列表
        ele_list = element.objects.filter(project_id=pro_id)
        return render_to_response("element_list_ajax.html",{"ele_list":ele_list})

def modify_process(request):
    if request.method == "POST":
        btn_name = request.POST.get("btn_name")
        if btn_name == u"保存用例":
            current_pro_name =request.POST.get("current_pro_name")
            case_name = request.POST.get("casename")
            case_nature = request.POST.get("nature")
            browser = request.POST.get("browser")
            desc = request.POST.getlist("desc")
            action = request.POST.getlist("action")
            value = request.POST.getlist("value")
            ele_id = request.POST.getlist("ele_id")
            case_id = request.POST.get("case_id")

            try:
                Case.objects.filter(pk=case_id).update(name=case_name, case_nature=case_nature, browser=browser)
                print "更新用例名称，性质，浏览器"
            except:
                return HttpResponse('名称重复')

            case_obj =Case.objects.get(pk=case_id)
            case_process_obj = Case.objects.get(pk=case_id).case_process_set.all()

            print "按照POST过来的数据长度为%s开始循环写入数据" %len(action)

            for i in range(len(action)):
                try:
                    ele_name = element.objects.get(pk=ele_id[i]).name
                except:
                    ele_name = u"添加元素"
                try:
                    case_process_obj.filter(pk=case_process_obj[i].id).update(desc=desc[i],action=action[i],value=value[i],ele_id=ele_id[i],ele_name=ele_name)
                except:
                    case_obj.case_process_set.create(desc=desc[i],action=action[i],value=value[i],ele_id=ele_id[i],ele_name=ele_name)


            if len(action) < case_process_obj.count():
                print "POST数据小于数据库长度，开始删除数据库中多余的数据"
                del_obj = case_process_obj[len(action):case_process_obj.count()]
                for i in del_obj:
                    print "开始删除步骤:%s" %i.desc
                    i.delete()
            return HttpResponse("用例修改成功")

        if btn_name ==u"添加元素":
            pro_name = request.POST.get("pro_name")
            ele_name = request.POST.get("name")
            ele_fun = request.POST.get("function")
            ele_value = request.POST.get("value")
            ele_desc = request.POST.get("desc")
            ele_url = request.POST.get("page_url")

            Project.objects.get(name=pro_name).element_set.create(name=ele_name,fun=ele_fun,values=ele_value,desc=ele_desc,page_url=ele_url)
            return HttpResponse("添加元素成功")


        if btn_name == u"修改元素":
            pro_name = request.POST.get("pro_name")
            ele_id = request.POST.get("ele_id")
            ele_name = request.POST.get("name")
            ele_fun = request.POST.get("fun")
            ele_value = request.POST.get("value")
            ele_desc = request.POST.get("desc")
            ele_url = request.POST.get("page_url")
            element_obj = Project.objects.get(name=pro_name).element_set.get(pk=ele_id)
            element_obj.name = ele_name
            element_obj.fun = ele_fun
            element_obj.values = ele_value
            element_obj.desc = ele_desc
            element_obj.page_url = ele_url
            element_obj.save()
            return HttpResponse("修改成功")

    if request.method == "GET":
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]
         # -----通过用例ID获取项目ID,并传到html中隐藏的button的value值----------
        # 获取用例ID
        case_id = request.GET.get("name")
        # 获取用例对象
        case_obj = Case.objects.get(pk=int(case_id))
        project_id = case_obj.project_id
        # 获取项目名称
        current_project_name = Project.objects.get(pk=project_id).name
        case_list = Project.objects.get(name=current_project_name).case_set.all()
        process_all = case_obj.case_process_set.all()
        fun = Method.objects.all()
        return render_to_response("modify_process.html",{"project_name":project_name,"is_superuser":is_superuser,
                                                         "first_name":first_name,"current_project_name":current_project_name,
                                                         "case_obj":case_obj,"process_all":process_all,"case_list":case_list,"fun":fun})


def case_process(request):
    if request.method == "POST":
        btn_name = request.POST.get("btn_name")
        if btn_name == u"保存用例":
            current_name = request.POST.get("current_name")

            case_name = request.POST.get("casename")
            case_nature = request.POST.get("nature")
            browser = request.POST.get("browser")
            desc = request.POST.getlist("desc")
            action = request.POST.getlist("action")
            value = request.POST.getlist("value")
            ele_id = request.POST.getlist("ele_id")

            # 写入用例
            try:
                Project.objects.get(name=current_name).case_set.create(name=case_name, browser=browser,category="测试用例",
                                                                 case_nature=case_nature)
            except:
                return HttpResponse("名称重复")

            for i in range(len(action)):
                if ele_id[i]:

                    ele_name = element.objects.get(pk=ele_id[i]).name
                    Case.objects.get(name=case_name).case_process_set.create(desc=desc[i], action=action[i], value=value[i],
                                                     ele_id=ele_id[i], ele_name=ele_name)
                else:
                    Case.objects.get(name=case_name).case_process_set.create(desc=desc[i], action=action[i], value=value[i],ele_id=ele_id[i], ele_name="元素为空")

            return HttpResponse("保存成功")


        if btn_name ==u"添加元素":
            pro_name = request.POST.get("pro_name")
            ele_name = request.POST.get("name")
            ele_fun = request.POST.get("function")
            ele_value = request.POST.get("value")
            ele_desc = request.POST.get("desc")
            ele_url = request.POST.get("page_url")

            Project.objects.get(name=pro_name).element_set.create(name=ele_name,fun=ele_fun,values=ele_value,desc=ele_desc,page_url=ele_url)
            return HttpResponse("添加元素成功")




        if btn_name == u"修改元素":
            pro_name = request.POST.get("pro_name")
            ele_id = request.POST.get("ele_id")
            ele_name = request.POST.get("name")
            ele_fun = request.POST.get("fun")
            ele_value = request.POST.get("value")
            ele_desc = request.POST.get("desc")
            ele_url = request.POST.get("page_url")
            element_obj = Project.objects.get(name=pro_name).element_set.get(pk=ele_id)

            element_obj.name = ele_name
            element_obj.fun = ele_fun
            element_obj.values = ele_value
            element_obj.desc = ele_desc
            element_obj.page_url = ele_url
            element_obj.save()
            return HttpResponse("修改成功")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        pro_name = request.GET.get("pro_name").strip()
        case_list = Project.objects.get(name=pro_name).case_set.all()
        element_list = element.objects.all()
        fun = Method.objects.all()

        return render_to_response("case_process.html", {"project_name":project_name,"is_superuser":is_superuser,
                                                       "first_name":first_name,
                                                       "current_pro_name":pro_name,
                                                       "element_list":element_list,
                                                       "fun":fun,"case_list":case_list})


def InMessCoKey1(request):
    # 加载报文组合定位方法，用于维护页面的jquery页面加载事件。
    mo = MessageObject.objects.all()
    print "Get messKey"

    # lenKey1 = len(MessObj)
    # k1List = []
    # for i in range(lenKey1):
    # key1 = MessObj[0].key1
    #     k1List.extend(key1)
    # return render_to_response("iMessCoKey1_ajax.html", {"MessObj": k1List})
    return render_to_response("iMessCoKey1_ajax.html", {"mo": mo})


def InMessCoKey2(request):
    # 加载报文组合定位方法，用于维护页面的jquery页面加载事件。
    mo = MessageObject.objects.all()
    print "Get messKey2"
    return render_to_response("iMessCoKey2_ajax.html", {"mo": mo})


def InMessCoKey3(request):
    # 加载报文组合定位方法，用于维护页面的jquery页面加载事件。
    mo = MessageObject.objects.all()
    print "Get messKey2"
    return render_to_response("iMessCoKey3_ajax.html", {"mo": mo})


def add_inter_case(request):
    # return render_to_response("add_inter_case.html")
    if request.method == 'POST':
        # cae_name= request.POST.get("casename")
        # InCaseList.objects.create()
        # ---当前项目名称---
        current_name = request.POST.get("current_name")
        # ---获取当前项目对象-----
        project_obj = Project.objects.get(name=current_name)
        # ----用例名称、用例性质---------
        caseName = request.POST.get("casename")
        caseType = request.POST.get("casetype")
        diffSelect = request.POST.get("diffSelect")
        # if diffSelect == "数据库对比":
        #     diffSelect = "dbdiff"
        # elif diffSelect == "特定字符串对比":
        #     diffSelect = "objdiff"
        try:
            # -----写入用例表------
            project_obj.incaselist_set.create(caseName=caseName, caseType=caseType, diffType=diffSelect)
            # return HttpResponse("保存成功")
        except:
            return HttpResponse("名称重复 addCaseInfo")

        # -----获取用例名称-------
        case_obj = InCaseList.objects.get(caseName=caseName)
        try:
            print request.POST, 'post'
            # -----获取步骤长度--------
            jms_messagedisin_length = len(request.POST.getlist('key1'))
            # obj_diff_length = len(request.POST.getlist('objdiff'))
            # ------循环写入步骤---------
            if jms_messagedisin_length != 0:
                for i in range(jms_messagedisin_length):
                    key1 = request.POST.getlist('key1')[i]
                    key2 = request.POST.getlist('key2')[i]
                    print "key2: ", str(key2)
                    val = request.POST.getlist('value')[i]
                    case_obj.incasedetail_set.create(key1=str(key1),
                                                     key2=str(key2),
                                                     keyValue=str(val))
        except:
            return HttpResponse("名称重复 addObjDiff")

        try:
            # -----获取步骤长度--------
            dbdiff_length = len(request.POST.getlist('dbkey1'))
            obj_diff_length = len(request.POST.getlist('objkey1'))

            # ------循环写入步骤---------
            if dbdiff_length != 0:
                for i in range(dbdiff_length):
                    Uname = request.POST.getlist('uname')[i]
                    Pword = request.POST.getlist('pword')[i]
                    address = request.POST.getlist('dbaddress')[i]
                    Exesql = request.POST.getlist('sql')[i]
                    DbKey1 = request.POST.getlist('dbkey1')[i]
                    DbKey2 = request.POST.getlist('dbkey2')[i]
                    DbKey3 = request.POST.getlist('dbkey3')[i]
                    case_obj.dbdiff_set.create(uName=str(Uname),
                                               pWord=str(Pword),
                                               dbAddress=str(address),
                                               sql=str(Exesql),
                                               key1=str(DbKey1),
                                               key2=str(DbKey2),
                                               key3=str(DbKey3))

            if obj_diff_length != 0:
                print 'objdiff %s' % obj_diff_length
                for i in range(obj_diff_length):
                    objkey1 = request.POST.getlist('objkey1')[i]
                    objkey2 = request.POST.getlist('objkey2')[i]
                    objkey3 = request.POST.getlist('objkey3')[i]
                    eValue = request.POST.getlist('execeptValue')[i]
                    print objkey1
                    print objkey2
                    print eValue

                    case_obj.objdiff_set.create(key1=str(objkey1),
                                                key2=str(objkey2),
                                                key3=str(objkey3),
                                                execeptValue=str(eValue))

            return HttpResponse("保存成功")
        except:
            print traceback.format_exc()
            return HttpResponse("名称重复 addDbDiff")

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]
        # MessObj = MessageObject.objects.all()
        # mKey1 = get
        # -------获取当前项目名称,并显示过去---------
        current_pro_name = request.GET.get("pro_name").strip()
        sql = """select * from webapp_case where project_id=(SELECT id from webapp_project where name="%s")""" % current_pro_name
        case_list = sql_commend(sql=sql)
        mo = MessageObject.objects.all()
        # dataHead = MessageObject.objects.filter(key1 == 'datagramHeader')
        # dataHead = MessageObject.objects.filter(key1 == 'datagramBody')
        # openJl = MessageObject.objects.filter(type == 'openJl')
        # mo = MessageObject.objects.filter(type == 'openJl')

        for i in range(len(mo)):
            print mo[i].key1
        return render_to_response("add_inter_case.html", {"project_name": project_name, "is_superuser": is_superuser,
                                                          "first_name": first_name, "mo": mo,
                                                          "current_pro_name": current_pro_name,
                                                          "case_list": case_list})


def modify_inter_case_list(request):
    if request.method == 'POST':
        if request.POST.get("btn_name") == u"删除用例":
            get_id = request.POST.getlist("get_id[]")
            for i in get_id:
                # 删除用例步骤
                del_objdiff = "DELETE from webapp_objdiff where caseName_id= %s" % i
                sql_commend(del_objdiff)
                del_dbdiff = "DELETE from webapp_dbdiff where caseName_id= %s" % i
                sql_commend(del_dbdiff)
                del_detail = "DELETE from webapp_incasedetail where caseName_id= %s" % i
                sql_commend(del_detail)

                # 删除测试用例
                del_case = "DELETE from webapp_incaselist where id= %s" % i
                sql_commend(del_case)
        else:
            # 取ID
            case_id = request.POST.get("case_id")  # 点击测试调试，返回用例的ID
            print u"执行的用例是： %s" % case_id

            # 取名称
            get_name = InCaseList.objects.get(pk=case_id)

            case_name = str(get_name.caseName)

            # 取IP
            regip = get_client_ip(request)
            # Need new void to exe case
            runTest(regip, 'intercase', case_id, case_name)

            # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
            function_object = get_project_name(request)
            project_name = function_object[0]
            is_superuser = function_object[1]
            first_name = function_object[2]

            # -----当前项目名称----------
            current_project = request.GET.get("pro_name").strip()

            # ------获取关联项目id--------
            project_id = Project.objects.get(name=current_project).id

            # 通过关联项目id获取所有的用例列表
            case_list = InCaseList.objects.filter(project_id=project_id)

            paginator = Paginator(case_list, 10)  # 每页显示10个数据
            page = request.GET.get("page")  # 获取页码
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                # 如果页面不是一个整数,交付第一页。
                contacts = paginator.page(1)
            except EmptyPage:
                # 如果页面的范围(例如9999),交付最后一页的搜索结果
                contacts = paginator.page(paginator.num_pages)

            return render_to_response("modify_inter_case_list.html",
                                      {"case_list": contacts, "project_name": project_name,
                                       "is_superuser": is_superuser,
                                       "first_name": first_name, "current_project": current_project},
                                      context_instance=RequestContext(request))

    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # -----当前项目名称----------
        current_project = request.GET.get("pro_name").strip()
        print "cp: %s" % current_project
        # ------获取关联项目id--------
        project_id = Project.objects.get(name=current_project).id
        print "pid: %s" % project_id
        # 通过关联项目id获取所有的用例列表
        case_list = InCaseList.objects.filter(project_id=project_id)

        paginator = Paginator(case_list, 10)  # 每页显示10个数据
        page = request.GET.get("page")  # 获取页码
        try:
            contacts = paginator.page(page)
            print "c: %s" % contacts
        except PageNotAnInteger:
            # 如果页面不是一个整数,交付第一页。
            contacts = paginator.page(1)
            print "c1: %s" % contacts
        except EmptyPage:
            # 如果页面的范围(例如9999),交付最后一页的搜索结果
            contacts = paginator.page(paginator.num_pages)
            print "c2: %s" % contacts

        return render_to_response("modify_inter_case_list.html",
                                  {"case_list": contacts, "project_name": project_name, "is_superuser": is_superuser,
                                   "first_name": first_name, "current_project": current_project},
                                  context_instance=RequestContext(request))


def modify_inter_case(request):
    if request.method == "POST":
        # 通过id获取项目对象
        project_obj = Project.objects.get(pk=int(request.POST.get("project_id")))

        # 取测试用例ID
        case_id = request.POST.get("case_id")

        # 获取用例对象和POST到的案例名称和性质
        case_obj = project_obj.incaselist_set.get(pk=case_id)
        name = request.POST.get("casename")
        diffSelect = request.POST.get("diffSelect")

        try:
            case_obj.caseName = name
            case_obj.diffType = diffSelect
            case_obj.save()
            print "<*****************>"
            print u'写入测试用例名称为：%s' % name
            print "<*****************>"
        except:
            print traceback.format_exc()
            return HttpResponse("名称重复 写入测试用例名称")

        # 删除casedetail,objdiff,dbdiff数据，重新写入
        del_objdiff = "DELETE from webapp_objdiff where caseName_id= %s" % case_id
        sql_commend(del_objdiff)
        del_dbdiff = "DELETE from webapp_dbdiff where caseName_id= %s" % case_id
        sql_commend(del_dbdiff)
        del_detail = "DELETE from webapp_incasedetail where caseName_id= %s" % case_id
        sql_commend(del_detail)

        # 重新提交表单数据
        try:
            print request.POST, 'post'
            # -----获取步骤长度--------
            jms_messagedisin_length = len(request.POST.getlist('key1'))
            # obj_diff_length = len(request.POST.getlist('objdiff'))
            print jms_messagedisin_length
            print "key1 is ok"
            # ------循环写入步骤---------
            if jms_messagedisin_length != 0:
                for i in range(jms_messagedisin_length):
                    key1 = request.POST.getlist('key1')[i]
                    key2 = request.POST.getlist('key2')[i]
                    val = request.POST.getlist('value')[i]
                    case_obj.incasedetail_set.create(key1=str(key1),
                                                     key2=str(key2),
                                                     keyValue=str(val))
        except:
            return HttpResponse("名称重复 写入报文信息")

        try:
            # -----获取步骤长度--------
            dbdiff_length = len(request.POST.getlist('dbkey1'))
            obj_diff_length = len(request.POST.getlist('objkey1'))
            print u"写入数据比较表 db: ", str(dbdiff_length)
            # ------循环写入步骤---------
            if dbdiff_length != 0:
                for i in range(dbdiff_length):
                    Uname = request.POST.getlist('uname')[i]
                    print Uname
                    Pword = request.POST.getlist('pword')[i]
                    address = request.POST.getlist('dbaddress')[i]
                    Exesql = request.POST.getlist('sql')[i]
                    DbKey1 = request.POST.getlist('dbkey1')[i]
                    DbKey2 = request.POST.getlist('dbkey2')[i]
                    DbKey3 = request.POST.getlist('dbkey3')[i]

                    case_obj.dbdiff_set.create(uName=str(Uname),
                                               pWord=str(Pword),
                                               dbAddress=str(address),
                                               sql=str(Exesql),
                                               key1=str(DbKey1),
                                               key2=str(DbKey2),
                                               key3=str(DbKey3))

            if obj_diff_length != 0:
                print 'objdiff %s' % obj_diff_length
                for i in range(obj_diff_length):
                    objkey1 = request.POST.getlist('objkey1')[i]
                    objkey2 = request.POST.getlist('objkey2')[i]
                    objkey3 = request.POST.getlist('objkey3')[i]
                    eValue = request.POST.getlist('execeptValue')[i]
                    case_obj.objdiff_set.create(key1=str(objkey1),
                                                key2=str(objkey2),
                                                key3=str(objkey3),
                                                execeptValue=str(eValue))

            return HttpResponse("修改成功")
        except:
            print traceback.format_exc()
            return HttpResponse("名称重复")

    if request.method == "GET":

        # 获取用例ID
        case_id = ''.join(dict(request.GET).keys())
        print "cid: %s" % case_id
        # 获取用例对象
        case_obj = InCaseList.objects.get(pk=int(case_id))

        diffSelect = case_obj.diffType
        print "cobj: %s" % case_obj
        # 获取用例步骤
        casedet = case_obj.incasedetail_set.all()
        caseobjd = case_obj.objdiff_set.all()
        casedbd = case_obj.dbdiff_set.all()
        if len(casedbd) > 0:
            casedb0 = casedbd[0]
        elif len(casedbd) == 0:
            casedb0 = {"uName": " ", "pWord": " ", "dbAddress": " ", "sql": " "}
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]
        # -----通过用例ID获取项目ID,并传到html中隐藏的button的value值----------
        project_id = case_obj.project_id

        # 获取项目名称
        current_project_name = Project.objects.get(pk=project_id).name
        sql = """select * from webapp_incaselist where project_id=(SELECT id from webapp_project where name="%s")""" % current_project_name
        case_list = sql_commend(sql=sql)

        return render_to_response("modify_inter_case.html",
                                  {"casename": case_obj, "casestep": casedet, "project_name": project_name,
                                   "diffSelect": case_obj,
                                   "caseobj": caseobjd, "casedb": casedbd, "casedb0": casedb0,
                                   "is_superuser": is_superuser,
                                   "first_name": first_name,
                                   "project_id": project_id,
                                   "current_project_name": current_project_name,
                                   "case_list": case_list,
                                   })


def interfaceParamManager(request):
    # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
    function_object = get_project_name(request)
    project_name = function_object[0]
    is_superuser = function_object[1]
    first_name = function_object[2]
    if request.method == "POST":
        if request.POST.get('subBtn') == '删除元素':
            print u"delete obj"
            pid = request.POST.get('pro_id')
            po = MessageObject.objects.get(pk=str(pid))
            try:
                po.delete()
                return HttpResponse('删除元素成功')
            except:
                return HttpResponse('删除元素失败')

        elif request.POST.get('subBtn') == 'mdyObj':
            print u"mdy_obj"
            objId = request.POST.get('mdy_objId')
            print(objId)
            mo = MessageObject.objects.get(pk=str(objId))
            try:
                mo.objName = request.POST.get('objName')
                mo.key1 = request.POST.get('key1')
                mo.key2 = request.POST.get('key2')
                mo.key3 = request.POST.get('key3')
                mo.type = request.POST.get('type')
                mo.save()
                return HttpResponse('修改报文参数成功')
            except:
                return HttpResponse('修改报文参数失败')

        else:
            #     ---当前项目名称---
            current_name = request.POST.get("addProName")
            # ---获取当前项目对象-----
            project_obj = Project.objects.get(name=current_name)
            try:
                objName = request.POST.getlist('objName')[0]
                key1 = request.POST.getlist('key1')[0]
                key2 = request.POST.getlist('key2')[0]
                key3 = request.POST.getlist('key3')[0]
                type = request.POST.getlist('type')[0]
                project_obj.messageobject_set.create(objName=str(objName),
                                                    key1=str(key1),
                                                    key2=str(key2),
                                                    key3=str(key3),
                                                    type=str(type),)
                return HttpResponse("保存报文参数成功")
            except:
                return HttpResponse("保存报文参数失败")
    if request.method == "GET":
        # -----通过用例ID获取项目ID,并传到html中隐藏的button的value值----------
        proName = Project.objects.all()
        mo = MessageObject.objects.all()
        return render_to_response("interfaceParamManager.html",
                                  {"project_name": project_name, "is_superuser": is_superuser,
                                   "first_name": first_name, "proName": proName,
                                   "mo": mo})

def data_base_manager(request):
    # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
    function_object = get_project_name(request)
    project_name = function_object[0]
    is_superuser = function_object[1]
    first_name = function_object[2]
    if request.method =="POST":
        print str(request.POST)
        print "POST"
        if request.POST.get('subBtn') == 'addNewEnv':
            print u"参数保存"
            proName = request.POST.get('proName')
            address = request.POST.get('address')
            username = request.POST.get('username')
            password = request.POST.get('password')
            interFaceType = request.POST.get('interFaceType')
            chest = request.POST.get('radiobutton')
            if str(chest) == '1':
                is_used = 1
            else:
                is_used = 0
            envName = request.POST.get('envName')
            try:
                project_obj = Project.objects.get(name=proName)
                if is_used == 1:
                    project_obj.prosetting_set.update(is_used=0)
                project_obj.prosetting_set.create(
                    address=str(address),
                    userName=str(username),
                    passWord=str(password),
                    interfaceType=str(interFaceType),
                    is_used=is_used,
                    envName=str(envName)
                )
                return HttpResponse("保存环境参数成功")
            except :
                return HttpResponse("保存环境参数失败")

        elif request.POST.get('subBtn') == '删除环境配置':
            print u"delete envSetting"
            pid = request.POST.get('pro_id')
            print pid, "is pid"
            po = ProSetting.objects.get(pk=str(pid))
            try:
                po.delete()
                return HttpResponse('删除环境参数成功')
            except:
                return HttpResponse('删除环境参数失败')

        elif request.POST.get('subBtn') == 'mdyEnv':
            print u"edit envSetting"
            pid = request.POST.get('pro_id1')
            print pid, "is pid"
            proName = request.POST.get('proName')
            address = request.POST.get('address')
            username = request.POST.get('username')
            password = request.POST.get('password')
            interFaceType = request.POST.get('interFaceType')
            chest = request.POST.get('radiobutton')
            if str(chest) == '1':
                is_used = 1
            else:
                is_used = 0
            envName = request.POST.get('envName')
            project_obj = Project.objects.get(name=proName)
            if is_used == 1:
                    project_obj.prosetting_set.update(is_used=0)
            po = ProSetting.objects.get(pk=str(pid))
            try:
                po.address = str(address)
                po.userName = str(username)
                po.passWord = str(password)
                po.interfaceType = str(interFaceType)
                po.is_used = is_used
                po.envName = str(envName)
                po.save()
                return HttpResponse('修改环境参数成功')
            except:
                return HttpResponse('修改环境参数失败')



    if request.method == "GET":
        project = Project.objects.all()
        proInfo = []
        for i in project:

            proName = i.name
            proSet = i.prosetting_set.all()
            for j in proSet:
                proId = j.id
                envName = j.envName
                address = j.address
                uName = j.userName
                pWord = j.passWord
                iType = j.interfaceType
                is_used = str(j.is_used)
                proSetList = {'proName': proName,
                              'proId': proId,
                              'address': address,
                              'uName': uName,
                              'pWord': pWord,
                              'iType': iType,
                              'is_used': is_used,
                              'envName': envName
                              }
                proInfo.append(proSetList)


        # -----通过用例ID获取项目ID,并传到html中隐藏的button的value值----------
        return render_to_response("DataBaseManager.html",
                              {"project_name": project_name, "is_superuser": is_superuser,
                               "first_name": first_name, "project": project,
                               "proInfo": proInfo
                               })
def addNewEnvAjax(request):
    if request.method == "POST":
        mo = Project.objects.all()
        return render_to_response("add_new_env.html", {"mo": mo})
def envListAjax(request):
    if request.method == "POST":
        return render_to_response("env_list_ajax.html")

def search_ajax(request):
    if request.method == "POST":
        print "Post"
        pid = request.POST.get('proName')
        po = Project.objects.get(name=pid)
        mo = po.messageobject_set.all()
        print mo
        return render_to_response("search_ajax.html",
                                  {"mo": mo})

def add_new_messageObj_ajax(request):
    if request.method == "POST":
        return render_to_response("add_new_messageObj_ajax.html")

def add_new_diffObj_ajax(request):
    if request.method == "POST":
        return render_to_response("add_new_diffObj_ajax.html")

def InDataGaramHead(request):
    mo = MessageObject.objects.filter(key1 == 'datagramHeader')
    return render_to_response("iDataGaramHead_ajax.html", {"mo": mo})

def InDataGaramBody(request):
    mo = MessageObject.objects.filter(key1 == 'datagramBody')
    return render_to_response("iDataGaramBody_ajax.html", {"mo": mo})