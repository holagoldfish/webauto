# -.- coding:utf-8 -.-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from webapp import views

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'django.contrib.auth.views.login'),
                       url(r'^index/$', views.index),
                       url(r'^add_case/$', views.add_case),
                       url(r'^case_list/$', views.case_list),
                       url(r'^modify_case/$', views.modify_case),
                       url(r'^base/$', views.base),
                       url(r'^case_list/$', views.case_list),
                       url(r'^add_business/$', views.add_business),
                       url(r'^case_ajax/$',views.case_ajax),
                       url(r'^business_ajax/$', views.business_ajax),
                       url(r'^business_list/$', views.business_list),
                       url(r'^modify_business/$', views.modify_business),
                       url(r'^use_case_management/$', views.use_case_management),
                       url(r'^add_perform/$', views.add_perform),
                       url(r'^perform_ajax/$', views.perform_ajax),
                       url(r'^perform_list/$', views.perform_list),
                       url(r'^modify_perform/$', views.modify_perform),
                       url(r'^user_management/$', views.user_management),
                       url(r'^project_management/$', views.project_management),
                       url(r'^method_ajax/$', views.method_ajax),
                       url(r'^action_ajax/$', views.action_ajax),
                       url(r'^report/$', views.report),
                       url(r'^report_html/(.+)$',views.report_html),
                       url(r"^perform_case_ajax/$",views.perform_case_ajax),
                       url(r'^add_element/$', views.add_element),
                       url(r'^case_process/$', views.case_process),
                       url(r'^modify_process/$', views.modify_process),
                       url(r'^process_ajax/$', views.process_ajax),
                       url(r'^ele_list_ajax/$', views.element_list_ajax),
                       url(r'^element_msg/$', views.element_msg),




                       url(r'interfaceParamManager/', views.interfaceParamManager),
                       url(r'add_inter_case/', views.add_inter_case),
                       url(r'modify_inter_case_list/', views.modify_inter_case_list),
                       url(r'data_base_manager/', views.data_base_manager),
                       url(r'^modify_inter_case/$', views.modify_inter_case),
                       url(r'^iMessCoKey1_ajax/', views.InMessCoKey1),
                       url(r'^iMessCoKey2_ajax/', views.InMessCoKey2),
                       url(r'^iMessCoKey3_ajax/', views.InMessCoKey3),
                       url(r'^iDataGaramHead_ajax/', views.InDataGaramHead),
                       url(r'^iDataGaramBody_ajax/', views.InDataGaramBody),
                       url(r'^add_new_env_ajax/', views.addNewEnvAjax),
                       url(r'^env_list_ajax/', views.envListAjax),
                       url(r'^search_ajax/', views.search_ajax),
                       url(r'add_new_messageObj_ajax/', views.add_new_messageObj_ajax),
                       url(r'add_new_diffObj_ajax/', views.add_new_diffObj_ajax)

                       )
