from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,Projects,List,Group_project,Task,Collaborators


class UserProfileForm(forms.ModelForm):
	class Meta():
		model = UserProfile
		fields = ('image','email','bio')

class ProjectForm(forms.ModelForm):
	class Meta():
		model = Projects
		fields = ('title',)

class ProjectUrlForm(forms.ModelForm):
	class Meta():
		model = Projects
		fields = ('project_url','website_owner','outstanding_requirements','challenges')


class ListForm(forms.ModelForm):
	class Meta():
		model = List
		fields = ('activity',)



class Group_projectForm(forms.ModelForm):
	class Meta():
		model = Group_project
		fields = ('project_title',)
				

class Group_userForm(forms.ModelForm):
	class Meta():
		model = Group_project
		fields = ('add_collaborator',)


class TaskForm(forms.ModelForm):
	class Meta():
		model = Task
		fields = ('task','assign_collaborator_to_task')

