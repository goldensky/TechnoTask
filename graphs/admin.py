from django.contrib import admin

from graphs.models import AbstractUser,CustomUser, Language, Task, Data_Type, Language_Construct,  Task_Solved_By_User, Comment , Message, LikeEvent ,  CustomUser_Profile

#admin.site.register(User)
#admin.site.unregister(AbstractUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',)
    search_field = ('first_name', 'last_name' , 'username',)
    
class CustomUser_ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )

class TaskAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id','name' ,  )
    search_field = ('name', 'lang',)
    list_filter = ('id', 'name',) 

class LanguageAdmin (admin.ModelAdmin):
    list_display =  ('name',)
    search_field = ('name',)



class Language_ConstructAdmin(admin.ModelAdmin):
    list_display =  ('name',)
    search_field = ('name')

class Data_TypeAdmin(admin.ModelAdmin):
    list_display =  ('name',)
    search_field = ('name')

admin.site.register(CustomUser, CustomUserAdmin )
admin.site.register(CustomUser_Profile, CustomUser_ProfileAdmin)


admin.site.register(Language, LanguageAdmin )
admin.site.register(Task, TaskAdmin)
admin.site.register(Data_Type, Data_TypeAdmin)
admin.site.register(Language_Construct, Language_ConstructAdmin)

admin.site.register(Task_Solved_By_User)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(LikeEvent)

#class ArticleAdmin(admin.ModelAdmin):
#    prepopulated_fields = {"slug": ("title",)}



#admin.site.register(User_Current_Environment)



# Register your models here.
