# -*- coding: utf-8 -*-

import sys
import os 
import MySQLdb
import random
import time
import datetime
from django.utils import timezone
from django.db.models import F


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechnoTask.settings')

import django
django.setup()

from graphs.models import *
#CustomUser, Language,  Task, Data_Types, Language_Constructs, Task_Solved_By_User, Comments

#  python script.py -u10 -t10 



def create_users(q_users_0, q_users_1):
    #print "from {0} to {1}".format(q_users_0, q_users_1)
    
    for person_num in range(q_users_0, q_users_1):
        #    User_"person_num"_"u2"
        u2 =  str(int(time.time() *100))
        user_uniq_traice = "_" + str(person_num) + "_" + u2
        user_uniq_name = "User" + user_uniq_traice
        user_uniq_firstname = "first_name" + user_uniq_traice
        user_uniq_lastname = "last_name" + user_uniq_traice

        user_uniq_email = str(person_num) + "@" + u2 + random.choice([".com", ".ru", ".org", ".net"])
        user_uniq_password = str(person_num) + user_uniq_traice
        user_date_joined = timezone.now()
                    
        #  CustomUser   
        k = CustomUser( username = user_uniq_name,
        email = user_uniq_email,
        first_name = user_uniq_firstname,
        last_name = user_uniq_lastname,
        password = user_uniq_password,
        date_joined = user_date_joined,
        last_login = timezone.now()  #datetime.datetime
        )
        user_uniq_list.append(k)            
    CustomUser.objects.bulk_create(user_uniq_list)




def create_tasks(total_tasks_before_exec, task_quantity):
    """
    Сначала создаем список задач  и заносим их целым списком  в базу данных.
    Затем проходим по всему списку задач, для каждой задачи выбираем случайным образом язык, 
    с помощью  которого  возможно эту задачу решить. Вносим в поле lang для этой задачи 
    выбранный язык и все языки, которые в иерархии расположены  выше выбранного языка.
    """ 
    q_tasks_0 =  total_tasks_before_exec + 1	# начальный номер id при этой генерации
    q_tasks_1 =  q_tasks_0 + task_quantity 		# конечный номер id
    all_lang_list =  Language.objects.all()		# список всех языков
    #print all_lang_list

    
    for cur_task_num in range(q_tasks_0, q_tasks_1):
        a =  str(cur_task_num)
        b =   "task_description_for_task_" + a
                    
        k = Task(name = a,
        description = b,
        pub_date = timezone.now(),                           
        )
        task_unique.append(k)
                
    Task.objects.bulk_create(task_unique)
    #print "task_unique "
    #print task_unique
    
    
    all_tasks = Task.objects.all()
    for cur_task_id in range(q_tasks_0, q_tasks_1):
        
        t = Task.objects.get(id = cur_task_id)
        #print "t = {0}".format(t)
        random_lang_id = random.randint(0, 4)
        random_lang = all_lang_list[random_lang_id]
        #print "random_lang.id = {0}".format(random_lang.id)
        #print "Language.objects.count() = {0}".format(Language.objects.count())
        #print "cur_task = {0}, lang  ={1}".format(t, random_lang)        
        
        if random_lang == all_lang_list[0]:
            #print "random_lang ==  L0"
            t.lang.add(all_lang_list[0], all_lang_list[1], all_lang_list[2], all_lang_list[3], all_lang_list[4])
                       
        elif random_lang == all_lang_list[1]:
            #print "random_lang ==  L1"
            t.lang.add(all_lang_list[1],  all_lang_list[2], all_lang_list[3], all_lang_list[4])
            
        elif random_lang == all_lang_list[2]:
            #print "random_lang ==  L2_1"
            t.lang.add(all_lang_list[2], all_lang_list[3], all_lang_list[4])    
            
        elif random_lang == all_lang_list[3]:
            #print "random_lang ==  L2_2"
            t.lang.add(all_lang_list[3], all_lang_list[4])
            
        elif random_lang == all_lang_list[4]:
            #print "random_lang ==  L3"
            t.lang.add(all_lang_list[4])

            
            
        
    
def user_chooses_task_and_solves_it ():
    """
    Юзер выбирает задачу из списка всех имеющихся - случайно - и пишет решение - 
    текст решения сохраняем в Task_Solved_By_User.
    пока решает задачу, может поставить ей лайк
    
    """ 
    all_tasks = Task.objects.all()
    all_users = CustomUser.objects.all()
    #print all_tasks
    
    for usr in all_users:
        rand_task = random.choice(all_tasks)
        solution = "begin " + str(usr.username) + " solved " + str(rand_task.id) + " end"

        solved_task = Task_Solved_By_User(solution_text = solution)
        solved_task.save()
        solved_task.task.add(rand_task)
        solved_task.user.add(usr)
               
        rand_task.times_was_solved = F('times_was_solved') + 1
        rating = (0,1)
        like = random.choice(rating)
        #print like
        
        if like:
            rand_task.vote = F('vote') + 1
        rand_task.save()
        
        usr.quantity_of_solved_tasks = F('quantity_of_solved_tasks') + 1
        usr.save()
                    
        
 




def user_chooses_some_solution_and_comments_it ():
    """
    юзер выбирает решение к задаче, которую решал не  он,  и пишет к ней комментарий.
    увеличиваем счетчик комментариев в решенных задачах.
    
    """
    all_solved_tasks = Task_Solved_By_User.objects.all()    
    all_users = CustomUser.objects.all()     
    
    for usr in all_users:
        rand_solved_task = random.choice(all_solved_tasks.exclude(user = usr)) 
       
        cur_comment_text= str(usr.username) + " _comments_ " + str(rand_solved_task)
        
        comment_obj = Comment.objects.create(comment_text = cur_comment_text )
        comment_obj.user.add(usr)          
        comment_obj.task.add(rand_solved_task)
        comment_obj.quantity_of_comments = F('quantity_of_comments') + 1
        comment_obj.save()
        rand_solved_task.quantity_of_comments_for_this_solved_task = F('quantity_of_comments_for_this_solved_task') + 1
        rand_solved_task.save()
        usr.quantity_of_commented_tasks = F('quantity_of_commented_tasks') + 1
        usr.save()
        
        
                   





if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Please, give parameters! For example: python script_0.py -u10 -t10 -c -s"
        #for param in sys.argv:
        #    print(param)


    
    time1 = time.clock()
    db = MySQLdb.connect(host = 'localhost', user = 'root', 
                    passwd = 'goldensky', db = 'db_L', charset = 'utf8')
    
    cursor = db.cursor()
    print "Success connect to database!"


    for param in sys.argv[1:]:
        if param[0] != '-':
            print "Please, give parameters, for example: python scr.py -u10 -t10 "
        else:
            if param[1] == 'u':
                user_quantity = int(param[2:])		# количество пользователей для создания
                user_uniq_list = []			# список для записи сгенерированных пользователей
        
        
                total_users_before_exec = CustomUser.objects.count()	#сколько юзеров уже есть в базе
                print "1 total_users_before_exec = {0}".format(total_users_before_exec)
                
                total_task_before_exec = Task.objects.count()
                print "1 total_task_before_exec = {0}".format(total_task_before_exec)


                q_users_0 =  total_users_before_exec + 1			#начальный номер id при этой генерации
                q_users_1 =  q_users_0 + user_quantity 			#конечный номер id
        
        
                create_users(q_users_0, q_users_1) #def
    
                total_users_after_exec = CustomUser.objects.count()
                print "total_users_after_exec = {0}".format(total_users_after_exec)

        
            elif param[1] == 't':					    	# name , description, 
                task_quantity = int(param[2:])					#количество задач для создания
                 
                task_unique = []    						# список для записи сгенерированных задач
   
                total_tasks_before_exec = Task.objects.count()
                print "total_task_before_exec = {0}".format(total_tasks_before_exec)

                create_tasks(total_tasks_before_exec, task_quantity)  #def
            
                total_tasks_after_exec = Task.objects.count()
                print "total_tasks_after_exec = {0}".format(total_tasks_after_exec) 
              
            elif param[1] == 's':
                user_chooses_task_and_solves_it ()	
            
            
            elif param[1] == 'c':	
                user_chooses_some_solution_and_comments_it ()
            
            else:
                print "Please, give correct parameters, for example: python script_0.py -u5 -t5 -c -s"

      
    print "Quantity of Users = {0}".format(CustomUser.objects.count())
    print "Quantity of tasks = {0}".format(Task.objects.count())
    print "Quantity of solved tasks = {0}".format(Task_Solved_By_User.objects.count())
    print "Quantity of comments = {0}".format(Comment.objects.count())
    #print "Quantity of likes = {0}".format(Task.objects.filter(task.vote>0))

                
    db.commit()
    db.close()
    time2 = time.clock()
    delta_time =  time2 - time1
    print "delta_time = {0}".format(delta_time)
 
 
 
 
  
 
 
 
 
    """ 
       
        
      

	def user_chooses_task_and_solves_it_1 ():
    """
    #Проходим по всем имеющимся в базе задачам - пишем  к ней решение, 
    #потом для каждого решения выбираем юзера, который эту задачу типа решил 
    #и заполняем все необходимые поля в модели Task_Solved_By_User - так используем 
    #bulk_create
    
    """
    all_tasks = Task.objects.all()
    all_users = CustomUser.objects.all()
    #print all_tasks
 

 
 
 
 
	""" 


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
     			
    			
