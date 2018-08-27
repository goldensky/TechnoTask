# -*- coding: utf-8 -*-

from django import forms
from .models import Task, Task_Solved_By_User, Comment, CustomUser, Language, CustomUser_Profile
import datetime
from django.core import validators
from django.core.validators import RegexValidator

from django.contrib.auth.forms import UserCreationForm
#from django.cotrib.auth import forms as auth_form    ?????? Toh

# http://tango.pythoff.com/chapters/forms.html


class CustomUserForm (forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'headshot')



class CustomUser_ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser_Profile
        fields = ('lang', 'task', 'data_type', 'lang_construct')
        
        
        
        
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required =  True, widget = forms.TextInput(attrs = {'placeholder':'E-mail'}))
    first_name = forms.CharField(required = True)
    last_name = forms.CharField (required = True)
    
    class Meta: 
        model = CustomUser 
        fields = ('email', 'first_name', 'last_name')  
        





        
class RegisterForm(forms.ModelForm):   #blog
    class Meta:
        model = CustomUser
        fields = ('username' , 'first_name', 'last_name', 'email', 'password')  
    
    def validate (self, value):
        if len(value) == 0 and self.required:
            raise ValidationError(self.error_message['required'])      
        
        
        
class UserViewForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username',)        
        
        
        
        

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 100)
    sender = forms.EmailField()    
    message = forms.CharField(min_length = 1, max_length = 500, 
    	widget = forms.Textarea(attrs = {'class': 'form-control', 'type':'text', 'rows': 10}))
    #subject = forms.CharField(max_length = 100)
#    
    #cc_myself  = forms.BooleanFiels(required = False) 


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(max_length = 500, help_text="Please enter the commentary.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    username = forms.CharField(min_length = 1, max_length = 30, error_messages = { 'required': "Please enter your name"})
    class Meta:
        model = Comment
        fields = ('comment_text', 'username', 'likes', )
        


        
class DateForm(forms.Form):
    day = forms.DateField(initial = datetime.date.today)
    class Meta:
        fields = ('day')    
        
         

class TaskForm (forms.ModelForm):   
    name = forms.CharField(max_length = 200, help_text = 'Название задачи') #   , placeholder = 'Название задачи')
    description = forms.CharField(max_length = 500,  help_text = 'Условие задачи')  #, placeholder = 'Условие задачи'
    lang = forms.ModelMultipleChoiceField (queryset = Language.objects.all())
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    
    class Meta:
        model = Task
        fields = ('name', 'description', 'lang',)   # fields = ('name', 'description',)


    
   

class Task_Solved_By_UserForm(forms.ModelForm):
    solution_text =  forms.CharField(widget=forms.Textarea(attrs = 
        {'class': "form-control", 'type': "text", 'rows': '15'}))
    
    task = forms.ModelMultipleChoiceField(queryset=Task.objects.all())
    user = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all())
    
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    times_was_solved = forms.IntegerField(widget=forms.HiddenInput(), initial=0)   # (default = 0)
    vote = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    
    class Meta:
        model = Task_Solved_By_User
        fields = ('solution_text', )

  


class SolutionForm(forms.ModelForm):
    solution_text =  forms.CharField(widget=forms.Textarea(attrs = 
        {'class': "form-control", 'type': "text", 'rows': '15'}))
    class Meta:
        model = Task_Solved_By_User
        fields = ('solution_text',)
    
   


















        
        
      
    
