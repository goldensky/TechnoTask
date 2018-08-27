# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404


from .forms import TaskForm, Task_Solved_By_UserForm, CommentForm, DateForm, CustomUserForm, CustomUser_ProfileForm, RegisterForm , RegistrationForm, SolutionForm
from django.shortcuts import redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

 
from reportlab.pdfgen import canvas
from django.http import HttpResponse 
from django.core.mail import send_mail, mail_admins,  BadHeaderError
from django.contrib.messages import constants as message


from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


from django.contrib.auth import authenticate, login


from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token, ensure_csrf_cookie

from .models import *   #  Task, Language, Data_Type, Language_Construct,  Task_Solved_By_User, Comment
# http://ustimov.org/posts/17/
# http://job-blog.bullgare.ru/2010/11/работа-со-стандартной-авторизацией-в-dja/
# https://habrahabr.ru/post/74165/

#    sudo cat /var/log/apache2/error.log
#    sudo cat /var/log/nginx/error.log
#     сча правильно sudo reboot -f
#     отдельное окно терминала. Перезапуск :
#   sudo killall gunicorn
#   sudo service lgraph start & 
#   sudo service nginx restart                  ------- nginx - только в случае замены статических файлов

#_____________________________________________________________________________________________________________________________________________________________________________________________
def index(request):
    return render(request, 'graphs/index.html', {})
    


def debug_toolbar(request):
    return render(request, 'graphs/debug_toolbar.html', {})    
    
    

def languages_l(request):
    return render(request, 'graphs/languages_l.html', {})




def l0(request):
    return render(request, 'graphs/l0.html', {})

def l1(request):
    return render(request, 'graphs/l1.html', {})
    
    
def l2_1(request):
    return render(request, 'graphs/l2_1.html', {})
    
    
def l2_2(request):
    return render(request, 'graphs/l2_2.html', {})

    
def l3(request):
    return render(request, 'graphs/l3.html', {})
    
    
def post_list(request):
    return render(request, 'graphs/post_list.html', {})
    



	
def regular_language(request):
    return render(request, 'graphs/regular_language.html', {})	

def ks_language(request):
    return render(request, 'graphs/ks_language.html', {})
    
    
def kz_language(request):
    return render(request, 'graphs/kz_language.html', {})


def lgraphs(request):
    return render(request, 'graphs/lgraphs.html', {})
    



    
#def tasks (request):
#    all_tasks = Task.objects.order_by('name')                            
#    return render(request, 'graphs/tasks.html', {'all_tasks': all_tasks} )
    
    
def tasks (request):
    tasks_list = Task.objects.all()
    paginator = Paginator (tasks_list,10)
    
    page = request.GET.get('page')
    try:
        tasks =  paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        tasks = paginator.page(1)
    except EmptyPage:
        #if page is out of range (9999), deliver last page of results
        tasks = paginator.page(paginator.num_pages)
    
    return render(request, 'graphs/tasks.html', {'tasks': tasks} )
    
    
def all_users(request):
    all_users =  CustomUser.objects.all()
    #total_amount = CustomUser.objects.count() 
    paginator =  Paginator (all_users, 10)
    
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render (request, 'graphs/all_users.html', {'users': users})  #  , 'total_amount': total_amount
 
 
 
 
#   work        
def user (request, usr_name):
    user = get_object_or_404(CustomUser, username = usr_name)
    user.view = user.view +1 
    user.save()
    last_solved_task = Task_Solved_By_User.objects.filter(user = user).filter(date_task_solved__lte = timezone.now()).order_by('-date_task_solved')[:10]
    last_comments = Comment.objects.filter(user = user).filter(id__lte = Comment.objects.count()).order_by('-id')[:10]
    
    #user.view = user.view + 1
    
        
    #last_comments = Comment.objects.filter(user = user).filter(user = user).filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:10]     
    return render (request, 'graphs/user.html', {'user': user, 'last_solved_task': last_solved_task, 'last_comments': last_comments}) 







 
#def last_reg_users(request):
#    all_users = CustomUser.objects.all()
#    last_users = all_users.filter()
#    return render (request, ) 
    


def last_registered_users(request):
    last_users = CustomUser.objects.filter(id__lte = CustomUser.objects.count()).order_by('-id')[:10]
    ####last_users = CustomUser.objects.filter(date_joined__lte = timezone.now()).order_by('-date_joined')[:10]   ###work
    #s_tasks = Task_Solved_By_User.objects.filter(user = )
    return render(request, 'graphs/last_registered_users.html', {'last_users': last_users})

def last_added_tasks(request):
    last_tasks = Task.objects.filter(id__lte = Task.objects.count()).order_by('-id') [:10]  
    # last_tasks = Task.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date') [:10]
    return render(request, 'graphs/last_added_tasks.html', {'last_tasks': last_tasks})
    
    
#def last_registered_users  (request):
#    last_reg_users = CustomUser.objects.filter(date_joined__lte = timezone.now()).order_by('-date_joined')[:10]
#    return render (request, 'graphs/last_registered_users.html', {'last_reg_users': last_reg_users} )  


def last_comments(request):
    last_comments = Comment.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:10]
    users = CustomUser.objects.all()
    return render (request, 'graphs/last_comments.html', {'last_comments': last_comments})    


    
def last_solved_tasks(request):
    last_tasks =  Task_Solved_By_User.objects.filter( date_task_solved__lte = timezone.now()).order_by('-date_task_solved') [:10]  
    return render (request, 'graphs/last_solved_tasks.html', {'last_tasks': last_tasks})
    















def register1 (request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            x = models.CustomUser()
            x = user_form.save(commit = False)
            obj = CustomUser.objects.create_user(username = x.username,
            				email = x.email,
            				password = x.password)
            obj.first_name = x.first_name
            obj.last_name = x.last_name
            obj.is_staff = True
            obj.is_active = True
            obj.date_joined = datetime.datetime.now()
            obj.save()
            return HttpResponseRedirect('graphs/success')
    else:
        form = RegisterForm()
    return render (request, 'graphs/register.html', {'form': form})
        
            
def register_duplicate(request):
    pass  # написать для случая повторения почты            

    
#http://tango.pythoff.com/chapters/login.html
def register (request):
    # Логическое значение, указывающее шаблону прошла ли регистрация успешно.
    # В начале ему присвоено значение False. 
    # Код изменяет значение на True, если регистрация прошла успешно.
    registered  = False
    if request.method == 'POST':
        # Попытка извлечь необработанную информацию из формы.
        user_form = CustomUserForm(data =  request.POST)
        profile_form = CustomUser_ProfileForm(data = request.POST)
    
        # Если в две формы введены правильные данные...    
        if user_form.is_valid: # and profile_form.is_valid:
            # Сохранение данных формы с информацией о пользователе в базу данных.
            
            user = user_form.save(commit = False)
            if 'headshot' in request.FILES:
                user.headshot = request.FILES['headshot']
        
        
            # Теперь мы хэшируем пароль с помощью метода set_password.
            # После хэширования мы можем обновить объект "пользователь".
            user.set_password(user.password)
            user.save()
        
        
            # Теперь разберемся с экземпляром CustomUser_Profile.
            # Поскольку мы должны сами назначить атрибут пользователя, необходимо приравнять commit=False.
            # Это отложит сохранение модели, чтобы избежать проблем целостности.
            profile = profile_form.save(commit = False)
            profile.user = user  
        
            # Проверить, предоставлено ли изображение для профиля? 
            # Если да, необходимо извлечь его из  формы и поместить в модель  CustomUser_Profile
            #if 'headshot' in request.FILES:
            #    profile.headshot = request.FILES['headshot']
        
        
            # Теперь сохраним экземпляр модели CustomUser_Profile
            profile.save()
        
            # Обновляем нашу переменную, чтобы указать, что регистрация прошла успешно.
            registered = True
            #return redirect ('graphs.views.success')
        
        # Неправильная формы или формы - ошибки или ещё какая-нибудь проблема?
        # Вывести проблемы в терминал.
        # Показать пользователю.
        else:
            print user_form.errors, profile_form.errors
    # Не HTTP POST запрос -  выводим  форму CustomUserForm()
    # Эта форма  не заполнена и готова к вводу данных от пользователя.
    else:
        user_form = CustomUserForm()
        profile_form = CustomUser_ProfileForm()
        
    return render ( request,   
        'graphs/register.html', 
        {'user_form':user_form, 'profile_form': profile_form, 'registered': registered}
        )

    #return render (request, 'graphs/register.html', {})	
    #return HttpResponseRedirect ('/success/')
    
    
    
def registered (request):
    return render (request, 'graphs/registered.html', {})    
    

def login (request):

    return render (request, 'graphs/login.html', {})








def user_login(request):
    print ("function ok")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print ("function ertttt")
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/graphs/')
            else:
                return HttpResponse('Ваш профиль неактивен.')
        else:
            print "Неверные данные {0} , {1}".format(username, password)
            return HttpResponse("Invalid login details supplied")
    else:
        return render (request, 'graphs/login.html', {})
    










































def success(request):
    return render (request, 'graphs/success.html', {})    
    
def author(request):
    return  render(request, 'graphs/author.html', {})
    
#def contacts(request):
#    return  render(request, 'graphs/contacts.html' , {})

def contact_form(request):
    return render (request, 'graphs/contact.html', {})

#def contact (request):
#    #form = ContactForm()
#    if request.POST:
#        form = ContactForm(request.POST)
#        if form.is_valid():
#            cd = form.cleaned_data
#            return HttpResponse(
#                'Name: %s, Email: %s , Message: %s' %
#                (cd['name'], cd['email'], cd['message'])          
#                )
#        else: 
#            form = ContactForm()
#        return render (request , 'contact.html', {'form': form})
            
#send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
        
def contact (request):
    errors = []
    form = ContactForm()
    if form.is_valid():
        subject = 'from l-graph'
        sender = form.cleaned_data['sender']
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']
        recipient_list = ['tanya.generalova@gmail.com']
    send_mail(subject, message, sender, recipient_list, name , fail_silently = False )
            
#mail_admins(subject, message, fail_silently=False, connection=None, html_message=None)[fuente]            
        

def contacts(request):
    errors = []
    form = {}
    subject = 'from l-graph'
    recipient_list = ['tanya.generalova@gmail.com']
    if request.POST:
        form['name'] = request.POST.get('name','')
        form['sender'] = request.POST.get('sender', '')
        form['message'] = request.POST.get('message','')
        
        if not form['name']:
            errors.append('Заполните имя')
        if not '@' in form['sender']:
            errors.append('Введите корректный e-mail')
        
        if not form ['message']:
            errors.append('Введите сообщение')
        if not errors:
            try:
                send_mail(subject, message, sender, recipient_list)
            except BadHeaderError:
                return HttpResponse ('Invalid header found')
            #return HttpResponseRedirect ('/contact/thanks/')
            
            # сохранение данных в базу
            #message = Message(request.POST)
            #message.sender_name = request.name
            #message.sender_email = request.email
            #message.text = request.message
            #message.date_pub = timezone.now()
            #message.save()
            return HttpResponse("Спасибо за Ваше сообщение")
    return render (request, 'graphs/contacts.html', {'errors': errors, 'form': form })

#  http://stackoverflow.com/questions/19132210/what-does-request-method-post-mean-in-django


def contacts2(request):
    errors = []
    form = {}
    subject = 'from l-graph'
    recipient_list = ['tanya.generalova@gmail.com']
    if request.POST:
        form['name'] = request.POST.get('name','')
        form['sender'] = request.POST.get('sender','')
        form['message'] = request.POST.get('message', '')
        
        
        if not form['name']:
            errors.append('Заполните имя')
        if not '@' in form['sender']:
            errors.append('Введите корректный e-mail')
        if not form['message']:
            errors.append('Введите сообщение')       
        
        if not errors:
            
            # сохранение данных в базу
            #message = Message(request.POST)
            #message.sender_name = request.name
            #message.sender_email = request.email
            #message.text = request.message
            #message.date_pub = timezone.now()
            #message.save()
            return HttpResponse("Спасибо за Ваше сообщение")
    return render (request, 'graphs/contacts.html', {'errors': errors, 'form': form })









#def task_new(request):
#    form = TaskForm()
#    return render(request, 'graphs/task_edit.html', {'form': form})
    







def post_list(request):    #  ?????????????????????????????????????????????????????????
    if request.method == "POST":
        form = Task_Solved_By_UserForm(request.POST)
        if form.is_valid:
            post = form.save(commit = False)
            post.user = request.user 
            post.task = request.task
            post.date_task_solved = timezone.now()
            post.solution_text = request.solution_text
            post.save()
            form.save_m2m()
            return redirect ('graphs.views.post_task_content', pk = post.pk)
        else:
            print form.errors
    form = Task_Solved_By_UserForm()


#date_task_solved = models.DateTimeField (auto_now_add = True)           #time
#    user = models.ManyToManyField(CustomUser)
#    task = models.ManyToManyField(Task, blank = True)
#    solution_text = models.TextField (default = '')



#def solution_publish(request):
#    if request.method == 'POST':
#        form = Task_Solved_By_UserForm()
        #solution_text = 













    
    
    

def task_new(request):
    # HTTP POST?
    if request.method == "POST":
        form = TaskForm(request.POST)
        
        # Все поля формы были заполнены правильно?
        if form.is_valid():
            # Сохранить новую категорию в базе данных, добавив доп поля.
            task = form.save(commit = False)
            task.author = request.user
            task.pub_date = timezone.now()
            task.save()
            form.save_m2m()
            # Теперь вызвать представление
            # будет показана   страница с задачей.
            return redirect ('graphs.views.task_content', pk = task.pk)  # name = task.name
        else:
            # Обрабатываемая форма содержит ошибки - вывести их в терминал.
            print form.errors
    else:
        # Если запрос был не POST, вывести форму, чтобы можно было ввести в неё данные.
        form = TaskForm()    
    # Форма с ошибкой (или ошибка в данных), форма не была получена...
    # Вывести форму с сообщениями об ошибках (если они были).
    return  render (request, 'graphs/task_edit.html' , {'form': form})

   


#def task_content (request, task_name):
#    task = get_object_or_404(Task, name = task_name)
#    return render (request, 'graphs/task_content.html', {'task': task}) 



# _______________________________________________________________________________________________________________________
def task_solve(request):
    # HTTP POST?
    if request.method == "POST":
        form = SolutionForm(request.POST)

    
    if form.is_valid():
        solution_post = form.save(commit=False)
        solution_post.user = request.user
        solution_post.task = request.task
        solution_post.date_task_solved = timezone.now()
        
        
        solution_post.save()
        form.save_m2m()
        return redirect('graphs.views.task_solve_edit', pk=task.pk)
    
    
    return render ( request, 'graphs/task_solve_edit.html', {'form': form})



def task_solve_____(request):
    return render ( request, 'graphs/solve.html', {})

















def task_content (request, pk):
    task = get_object_or_404(Task, pk = pk)
    task.views = task.views +1 
    print (task.views)
    task.save()
    return render (request, 'graphs/task_content.html', {'task': task}) 
 




# http://kutaloweb.com/jeff_forcier_glava_6/formy/
def add_solution(request, task_name_slug, **kwargs):
    try:
        task = Task.objects.get(slug = task_name_slug) 
    except Task.DoesNotExist:
        task = None 
        
    if request.method == 'POST':
        form = Task_Solved_By_UserForm(request.POST)
        if form.is_valid():
            if task:
                solution = form.save(commit = False)
                solution.solution_text = solution_text
                
                solution.user = user
                solution.task = task
                solution.views = 0
                solution.vote = 0
                
                new_solution = form.save()
                form.save_m2m()
                return HttpResponseRedirect(new_solution.get_absolute_url())
          
        else:
            relative = get_object_or_404(Task_Solved_By_User, pk = kwargs['id'])
            form = Task_Solved_bY_Userform(initial = {'last': relative.last})
        return render_to_response('graphs/form.html', {'form': form} )
            


def page403(request):
    return render (request, '403.html', {} , status = 403)
    
    

def page404(request):
    return render (request, '404.html', {} , status = 404)
    


def page500(request):
    return render(request, '500.html', {}, status = 500)
        
    
    
#def task_content (request, task_id = "1"): 
#	return render(request, 'graphs/task_content.html', {} )


#def task_content (request, id):
#    task = get_object_or_404(Task, id = id)
#    return render (request, 'graphs/task_content.html', {'task': task}) 


#   equivalent


#def task_content(request, pk):
#    try:
#        task = Task.objects.get(pk = task_id)
#    except Task.DoesNotExists:
#        raise Http404("Task does not exists")
#    return render (request, 'graphs/task_content.html', {'task': task}) 





	
"""

def tasks (request):
    tasks_list = Task.objects.all()
    paginator = Paginator (tasks_list,10)
    
    page = request.GET.get('page')
    try:
        tasks =  paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    
    return render(request, 'graphs/tasks.html', {'tasks': tasks} )

"""
	
	
"""
#http://tango.pythoff.com/chapters/login.html
def register (request):
    # Логическое значение, указывающее шаблону прошла ли регистрация успешно.
    # В начале ему присвоено значение False. 
    # Код изменяет значение на True, если регистрация прошла успешно.
    registered  = False
    if request.method == 'POST':
        # Попытка извлечь необработанную информацию из формы.
        user_form = CustomUserForm(data =  request.POST)
        profile_form = CustomUser_ProfileForm(data = request.POST)
    
        # Если в две формы введены правильные данные...    
        if user_form.is_valid: # and profile_form.is_valid:
            # Сохранение данных формы с информацией о пользователе в базу данных.
            
            user = user_form.save()
        
        
            # Теперь мы хэшируем пароль с помощью метода set_password.
            # После хэширования мы можем обновить объект "пользователь".
            user.set_password(user.password)
            user.save()
        
        
            # Теперь разберемся с экземпляром CustomUser_Profile.
            # Поскольку мы должны сами назначить атрибут пользователя, необходимо приравнять commit=False.
            # Это отложит сохранение модели, чтобы избежать проблем целостности.
            profile = profile_form.save(commit = False)
            profile.user = user  
        
            # Проверить, предоставлено ли изображение для профиля? 
            # Если да, необходимо извлечь его из  формы и поместить в модель  CustomUser_Profile
            if 'picture' in request.FILES:
                profile.headshot = request.FILES['picture']
        
        
            # Теперь сохраним экземпляр модели CustomUser_Profile
            profile.save()
        
            # Обновляем нашу переменную, чтобы указать, что регистрация прошла успешно.
            registered = True
        
        # Неправильная формы или формы - ошибки или ещё какая-нибудь проблема?
        # Вывести проблемы в терминал.
        # Показать пользователю.
        else:
            print user_form.errors, profile_form.errors
    # Не HTTP POST запрос -  выводим  форму CustomUserForm()
    # Эта форма  не заполнена и готова к вводу данных от пользователя.
    else:
        user_form = CustomUserForm()
        profile_form = CustomUser_ProfileForm()
    return render ( request,   
        'graphs/register.html', 
        {'user_form':user_form, 'profile_form': profile_form, 'registered': registered}
        )

    #return render (request, 'graphs/register.html', {})	
    
    










"""



































	
	
	
	
    #return HttpResponse ("detail for task %s" % task_id)   
    
#def detail (request, task_id):
#    return render (request,  'graphs/ task_id)    
 
 
 #  https://habrahabr.ru/post/181556/  
 
#  https://docs.djangoproject.com/en/1.9/howto/outputting-pdf/
