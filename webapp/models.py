# -.- coding:utf-8 -.-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)
    pro_user = models.CharField(max_length=200)
    pro_status = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    def __unicode__(self):
        return self.name


class Case(models.Model):
    name = models.CharField(max_length=200,unique=True)
    browser = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    case_nature = models.CharField(max_length=500)
    category = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    def __unicode__(self):
        return self.name


class Method(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Business(models.Model):
    name = models.CharField(max_length=200,unique=True)
    date = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=200)
    Project = models.ForeignKey(Project)
    def __unicode__(self):
        return self.name

class Business_stp(models.Model):
    name = models.CharField(max_length=200)
    case_id = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    case_nature = models.CharField(max_length=200)
    business = models.ForeignKey(Business)
    def __unicode__(self):
        return self.name

class Test_execution(models.Model):
    # 用例执行名称表
    name = models.CharField(max_length=200,unique=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class Execution_detail(models.Model):
    # 用例执行名称下面的测试用例和测试业务流，Perform_Case外链表
    name = models.CharField(max_length=200)
    case_nature = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    case_id = models.CharField(max_length=200)
    business_id = models.CharField(max_length=200)
    perform = models.ForeignKey(Test_execution)
    def __unicode__(self):
        return self.name

class Test_report(models.Model):
    name = models.CharField(max_length=200)
    Execution_id = models.CharField(max_length=20)
    date = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class element(models.Model):
    name = models.CharField(max_length=200)
    fun = models.CharField(max_length=200)
    values = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)
    page_url = models.CharField(max_length=500)
    project = models.ForeignKey(Project,null=True)
    def __unicode__(self):
        return self.name

class case_process(models.Model):
    desc = models.CharField(max_length=500)
    action = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    ele_id = models.CharField(max_length=20)
    ele_name = models.CharField(max_length=200)
    case = models.ForeignKey(Case)
    def __unicode__(self):
        return self.desc


class InterMethod(models.Model):
    type = models.CharField(max_length=20)
    def __unicode__(self):
        return self.type

# 接口测试用例列表，caseType区分jms报文或者开放平台用例,diffType区分数据比对方式
class InCaseList(models.Model):
    # caseId = models.IntegerField(unique=True,null=True)
    project = models.ForeignKey(Project)
    caseName = models.CharField(max_length=200, unique=True)
    caseType = models.CharField(max_length=10)
    diffType = models.CharField(max_length=10)
    createDate = models.DateTimeField(auto_now_add=True)
    modifyDate = models.DateTimeField(auto_now=True)

# jms报文存储,key1区分位于Head或者Body,key2区分特定的字段，keyValue是字段值
class InCaseDetail(models.Model):
    caseName = models.ForeignKey(InCaseList)
    key1 = models.CharField(max_length=40)
    key2 = models.CharField(max_length=40, null=True)
    keyValue = models.CharField(max_length=200)

class DbDiff(models.Model):
    caseName = models.ForeignKey(InCaseList)
    uName = models.CharField(max_length=20)
    pWord = models.CharField(max_length=20)
    dbAddress = models.CharField(max_length=200)
    sql = models.CharField(max_length=500)
    key1 = models.CharField(max_length=20)
    key2 = models.CharField(max_length=20, null=True)
    key3 = models.CharField(max_length=20, null=True)
    dbkey1 = models.CharField(max_length=20)
    dbkey2 = models.CharField(max_length=20, null=True)

class ObjDiff(models.Model):
    caseName = models.ForeignKey(InCaseList)
    key1 = models.CharField(max_length=40)
    key2 = models.CharField(max_length=40, null=True)
    key3 = models.CharField(max_length=40, null=True)
    key4 = models.CharField(max_length=40, null=True)
    execeptValue = models.CharField(max_length=200)

class MessageObject(models.Model):
    proName = models.ForeignKey(Project)
    objName = models.CharField(max_length=40, null=True)
    key1 = models.CharField(max_length=40, null=True)
    key2 = models.CharField(max_length=40, null=True)
    key3 = models.CharField(max_length=40, null=True)
    type = models.CharField(max_length=40, null=True)

class ProSetting(models.Model):
    proName = models.ForeignKey(Project)
    envName = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    userName = models.CharField(max_length=30, null=True)
    passWord = models.CharField(max_length=30, null=True)
    interfaceType = models.CharField(max_length=20, null=True)
    is_used = models.BooleanField(default=False)