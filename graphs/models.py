# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import F
from TechnoTask.settings import ALLOWED_HOSTS


# http://smhfanda.blogspot.ru/2016/03/django-substitute-user-model.html
   
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.mail import send_mail



# http://stackoverflow.com/questions/3994060/django-full-url-in-get-absolute-url
#class Notification(models.Model):
#    cur_task = 
#    def get_full_absolute_url(self):
#        domain(ALLOWED_HOSTS[0])
#        
#        return 'http://%s%s' % (domain, self.get_absolute_url()) 

class  UserTypes(object):
    ADMIN = "Admin"
    USER = "User"
    CHOICES = (
        (ADMIN, 'Admin'), (USER, 'User')
        )
        
USER_TYPES = [UserTypes.ADMIN, UserTypes.USER]
    
class Language(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 255)
    pub_date = models.DateTimeField(auto_now_add = True)           #time
   
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Language'



class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,  default = 1 )
    slug = models.SlugField(default = 'name')
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    lang = models.ManyToManyField(Language)
    pub_date = models.DateTimeField(auto_now_add = True)           #time
    times_was_solved = models.IntegerField(default = 0)
    views = models.IntegerField(default=0)
    #solution_text = models.TextField(default = '')
    vote = models.IntegerField(default = 0)  # rating      ------------------------------- like
    
    
    def  get_absolute_url(self):
        #path = reverse ('task_content', args = [self.id]) #  2
        #return 'http://%s%s' %   (self.site, path)  # 2
        
        #return reverse ('task_content', [str(self.id)])
        return reverse ('task_content', args =  [str(self.id)])
    
    def get_full_absolute_url(self):
        domain(ALLOWED_HOSTS[0]) 
        return 'http://%s%s' % (domain, self.get_absolute_url())        
        
        
    def __unicode__(self):
        return '{0}'.format(self.name)
        
    class Meta:
        verbose_name = 'Task'
    
    
    
class Data_Type(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    lang = models.ManyToManyField(Language)
    pub_date = models.DateTimeField(auto_now_add = True)           #time
        
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Data Type'


class Language_Construct(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    lang = models.ManyToManyField(Language)
    date_creation = models.DateTimeField(auto_now_add = True)           #time
        
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Language Construct'


class CustomUser(AbstractBaseUser, PermissionsMixin):

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    email = models.EmailField(
        _('Email Address'), unique = True,
        error_messages = {
            'unique': _("A user with that email already exists."),
        }
    )
    
    username = models.CharField( _('username'), max_length = 30, unique = True, blank = True, null = True,
        help_text = _('Required. 30 characters or fewer. Letters, digits and '
                      '@/./+/-/_ only.' ),
        validators = [
            validators.RegexValidator(r'^[\w.@+-]+$',
                                        _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.' ), 'invalid'), 
            ],
            error_messages = {
                'unique' : _('A user with that username already exists.'),
            
            }
    
    )
    
    first_name = models.CharField(_('first name'), max_length = 30, blank = True)
    last_name = models.CharField(_('last name'), max_length = 30, blank = True)
    is_staff = models.BooleanField(_('staff status'), default = False,
        help_text = _('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'),  default = True, 
        help_text = _('Designates whether this user should be treated  as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default = timezone.now)
    view =  models.IntegerField(default=0)
            
    objects = UserManager()
    
    timezone = models.CharField(max_length = 50, default = 'Europe/Moscow')
    lang =  models.OneToOneField(Language, blank = True, null = True)
    data_type = models.ManyToManyField(Data_Type, blank = True, null = True)
    lang_construct = models.ManyToManyField(Language_Construct, blank = True, null = True)
    session_date_reg = models.DateTimeField(auto_now_add = True, blank = True)        #time
    
    headshot = models.ImageField(upload_to = 'tmp/',default = 'tmp/None/no-img.jpg')
    quantity_of_solved_tasks = models.IntegerField(default = 0)
    quantity_of_commented_tasks = models.IntegerField(default = 0)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class  Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __unicode__(self):
        return '{}'.format(self.username)
            
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with the space in between.
        """
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()
        
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
            
    def email_user (self, subject, message,  from_email =  None,  **kwards):
        """
        Sends  an  email to  this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwards)
    
    @property    
    def is_admin(self):
        self.type == UserType.ADMIN
            
            
    
    
    #  https://docs.djangoproject.com/en/1.9/ref/contrib/auth/
    
    #username                           r
    #email
    #password                           r
    #last_login
    #date_joined
    



    
class Task_Solved_By_User(models.Model):
    date_task_solved = models.DateTimeField (auto_now_add = True)           #time
    user = models.ManyToManyField(CustomUser)
    task = models.ManyToManyField(Task, blank = True)
    solution_text = models.TextField (default = '')
    quantity_of_comments_for_this_solved_task = models.IntegerField(default = 0) 
       
    def __unicode__(self):
        return '{}'.format(self.task)
    
    def get_solution_text(self):
        return '{}'.format(self.solution_text)
        
    class Meta:
        verbose_name = 'Solved Task'
        

# http://ru.stackoverflow.com/questions/71620/Создание-профиля-пользователя-одновременно-с-самим-пользователем
# http://webnewage.org/2008/07/12/yuzer-ili-profil/
#   http://softwaremaniacs.org/blog/2007/03/07/auto-one-to-one-field/




class CustomUser_Profile(models.Model):
    user = models.OneToOneField(CustomUser)
    lang = models.OneToOneField(Language , blank = True, null = True)
    task = models.ManyToManyField(Task , blank = True, null = True)
    data_type = models.ManyToManyField(Data_Type, blank = True, null = True)  
    lang_construct = models.ManyToManyField(Language_Construct, blank = True, null = True)
    solution = models.TextField(default = '')  
    #solved_task = models.OneToOneField(Task_Solved_By_User)
    
    def __unicode__(self):
        return  '{0}'.format (self.user.username) 
    class Meta:
        verbose_name = 'CustomUser_Profile'
    
        
        
        
    
class Comment(models.Model):
    comment_text = models.CharField(max_length = 500)
    task = models.ManyToManyField (Task_Solved_By_User)
    user = models.ManyToManyField(CustomUser)
    pub_date = models.DateTimeField(auto_now_add  =True, blank = True)           #time
    quantity_of_comments = models.IntegerField(default = 0)    # total quantity
   
    
    def __unicode__(self):
        return self.comment_text
    
    class Meta:
        verbose_name = 'Comment'



class Message(models.Model):
    sender_name = models.CharField(max_length = 30)
    sender_email = models.EmailField(max_length = 40)
    date_pub = models.DateTimeField(auto_now_add = True)           #time
    text = models.TextField(default = "")
    
    def __unicode__(self): 
        return self.text
    
    class Meta:
        verbose_name = 'Message'


class LikeEvent(models.Model):
    liker = models.ForeignKey(CustomUser)
    liked_task = models.ForeignKey(Task)
    liked_date_pub = models.DateTimeField(auto_now_add = True)
    
    
    def __unicode__(self):
        return str(self.liker) + " liked " + self.liked_task.description
    class Meta:
        verbose_name = "Likes"








    
'''
mysql> show tables;
+------------------------------------+
| Tables_in_TT                       |
+------------------------------------+
| auth_group                         |
| auth_group_permissions             |
| auth_permission                    |
| django_admin_log                   |
| django_content_type                |
| django_migrations                  |
| django_session                     |
| graphs_comment                     |
| graphs_comment_task                |
| graphs_comment_user                |
| graphs_customuser                  |
| graphs_customuser_data_type        |
| graphs_customuser_groups           |
| graphs_customuser_lang_construct   |
| graphs_customuser_user_permissions |
| graphs_data_type                   |
| graphs_data_type_lang              |
| graphs_language                    |
| graphs_language_construct          |
| graphs_language_construct_lang     |
| graphs_task                        |
| graphs_task_lang                   |
| graphs_task_solved_by_user         |
| graphs_task_solved_by_user_task    |
| graphs_task_solved_by_user_user    |
+------------------------------------+
25 rows in set (0.00 sec)


'''
 
 
 

# Create your models here.

# http://djbook.ru/rel1.7/ref/models/instances.html#django.db.models.Model.get_FOO_display
# http://djbook.ru/rel1.7/ref/models/fields.html


