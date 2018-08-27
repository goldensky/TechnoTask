# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from . import views



    
    
urlpatterns = [
    # ex:    
    url(r'^$', views.index, name = 'index'),
    
    # ex: /l0/
    url(r'^L0|l0/$', views.l0, name = 'l0'),    
    url(r'^L1|l1/$', views.l1, name = 'l1'),
    
    url(r'^L|l2.1/$', views.l2_1, name = 'l2_1'),
    url(r'^L|l2.2/$', views.l2_2, name = 'l2_2'),
    url(r'^L|l3/$', views.l3, name = 'l3'),
    
    url(r'^post_list/$', views.post_list, name = 'post_list'),
    
    
    url(r'^tasks/$', views.tasks, name = 'tasks'), 
    
    url(r'^task/new/$', views.task_new, name = 'task_new'),
    
    # ex: /task/5         
    #url(r'^tasks/(?P<task_id>\d+)/$' ,  views.task, name = 'task'),
    
    #url(r'^tasks/(?P<task_name>[a-zA-Z0-9_ ]+)/$' ,  views.task_content, name = 'task_content'),
    url(r'^tasks/(?P<pk>\d+)/$' ,  views.task_content, name = 'task_content'),
    #url(r'^tasks/(?P<pk>\d+)/solve/$',  views.solve, name = 'solve' ),
    
    
        
    
    
    #url(r'^tasks/(?P<pk>\[0-9]+)/solve/$', views.task_solve, name = 'task_solve'),  #   post_new
    
    url(r'^tasks/(?P<pk>\[0-9]+)/solve$', views.task_solve, name = 'task_solve'),  #   post_new
    
    
    
    
        

        

    url(r'^regular_language/$', views.regular_language, name = 'regular_language' ),
    url(r'^ks_language/$', views.ks_language, name = 'ks_language'),
    url(r'^kz_language/$', views.kz_language, name = 'kz_language'),
    url(r'^lgraphs/$', views.lgraphs, name = 'lgraphs'),
    
    
    url(r'^login/$', views.user_login, name = 'login'),
       
    url(r'^register/$', views.register, name = 'register'),
    
    url(r'^registered/$', views.registered, name = 'registered'),
        
        
        
    url(r'^all_users/$', views.all_users, name = 'all_users'),
    
    url(r'^all_users/(?P<usr_name>[a-zA-Z0-9_]+)/$', views.user, name = 'user' ),
    url(r'^author/$', views.author, name = 'author'),
    url(r'^contacts/$', views.contacts, name = 'contacts'),
    
    #url(r'^auth/login/$', views.contacts, name = 'login_c'),
    
    url(r'^page404/$' , views.page404, name =  'page404' ), 
    url(r'^page500/$', views.page500, name = 'page500'), 
    
    url(r'^last_added_tasks/$' , views.last_added_tasks, name = 'last_added_tasks'),
    url(r'^last_comments/$', views.last_comments, name =   'last_comments'), 
    url(r'^last_registered_users/$', views.last_registered_users, name = 'last_registered_users'),
    url(r'^last_solved_tasks/$', views.last_solved_tasks, name = 'last_solved_tasks'), 
    url(r'^success/$', views.success, name = 'success'),
    
    
    
    #url(r'^like_task/$', views.like_task, name='like_task'),
    #url(r'^dislike_task/$', views.dislike_task, name='dislike_task'),
   
#    url(r'^contact/$', views.contact, name = 'contact'),
    
    ]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""    
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += url(r'^__debug__/', include(debug_toolbar.urls),
    )
"""
    
