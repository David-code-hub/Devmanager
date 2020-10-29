from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.forms import models
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm,ProjectForm,ListForm,ProjectUrlForm,Group_projectForm,Group_userForm,TaskForm
from .models import Projects,List,UserProfile,Group_project,Collaborators,Task


# Create your views here.


def signup(request):
	context={
	 "form":UserCreationForm(),
	}
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']

		#check if passwords match
		if password == password2:
			#if user exists in database
			if User.objects.filter(username=username).exists():
				messages.warning(request, 'Sorry that username is already taken.')
				return redirect('signup')
			else:
				#if doesnt exist create user and profile
				user = User.objects.create_user(username=username, password=password)
				user.save()
				UserProfile.objects.create(user=user)
				login(request, user)
				messages.success(request,'Successfully created account.')
				return redirect('project_home')
		else:
			messages.warning(request,'Passwords do not match.')
			return redirect('signup')
	else:
		return render(request,'signup.html',context)





def login_index(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			username = User.objects.get(username=username)
			messages.success(request, 'Welcome ' + str(username))
			return redirect('project_home')
		else:
			if User.objects.filter(username=username):
				messages.warning(request,'Invalid password')
				return redirect('home')
			else:
				messages.warning(request, 'Invalid username')
				return redirect('home')
	else:
		return render(request, 'index.html')





def signout(request):
	logout(request)
	return redirect('home')

#end signup and login





#start home

def project_home(request):
	project = Group_project.objects.filter(lead=request.user)[0:2]
	projects = Projects.objects.filter(user=request.user,project_url=None).order_by('-id')[0:2]
	users  = User.objects.all().count()
	sites	= Projects.objects.all().count()
	groups = Group_project.objects.all().count()
	context = {
		"projects":projects,
		"project":project,
		"users":users,
		"sites":sites,
		"groups":groups,
		"form":ProjectForm(),
		"forms": Group_projectForm(),
	}
	form = ProjectForm(request.POST)
	if form.is_valid():
		save = form.save(commit=False)
		save.user = request.user
		save.start_date = timezone.now()
		save.save()
		profile = UserProfile.objects.get(user=request.user)
		profile.projects.add(save)

		pro = Projects.objects.get(user=request.user,id=save.id)
		for p in Projects.objects.filter(user=request.user,title=pro.title):
			return redirect('activity', id=p.id)
	
	if request.method == 'POST':
		forms = Group_projectForm(request.POST)
		if forms.is_valid():
			name = forms.save(commit=False)
			name.lead = request.user
			name.save()
			return redirect('user_select',id=name.id)
	else:
		return render(request,'project.html',context)

#end home






#start group project

def user_select(request,id):
	project = Group_project.objects.get(id=id)

	context = {
	 "form": Group_userForm(),
	}

	if request.method == 'POST':
		form = Group_userForm(request.POST,instance=project)
		if form.is_valid():
			save = form.save(commit=False)
			save.save()
			if User.objects.filter(username=save.add_collaborator):
				user = User.objects.get(username=save.add_collaborator)
				collab = Collaborators.objects.create(collaborator = user,project=project,label_colour='primary')
				lead_collab = Collaborators.objects.create(collaborator =request.user,project=project)
				project.collaborators.add(lead_collab)
				project.collaborators.add(collab)

				profile = UserProfile.objects.get(user=user)
				collab.profile = profile
				collab.save()
				profile.group_project.add(collab.project)

				profiles = UserProfile.objects.get(user=request.user)
				lead_collab.profile = profiles
				lead_collab.save()
				profiles.group_project.add(lead_collab.project)
				return redirect('group-project' ,id=id)
			else:
				messages.warning(request,'The user specified does not exist.')
				return redirect('user_select' ,id=id)
	else:
		return render(request,'invite_user.html',context)



def group_project(request,id):
	project = Group_project.objects.get(id=id)
	collabs = Collaborators.objects.filter(project=project)
	task = Task.objects.filter(group_project=project)
	user_collab=Collaborators.objects.get(project=project,collaborator=request.user)

	#for cmpleted tasks
	new = Task.objects.filter(group_project=project)

	user_task = Task.objects.filter(assign_collaborator_to_task=user_collab)

	form = TaskForm(request.POST)
	form.fields["assign_collaborator_to_task"] = models.ModelChoiceField(queryset=Collaborators.objects.filter(project=project))
	if form.is_valid():
		save = form.save(commit=False)
		save.group_project = project
		save.save()
		project.task.add(save)

		return redirect('group-project' ,id=id)

	context = {
		"project":project,
		"collabs":collabs,
		"task":task,
		"form":form,
		"new":new,
		"user_task":user_task,
	}

	
	return render(request,'group_project.html',context)

def update_task(request,id):
	task = Task.objects.get(id=id)
	project = Group_project.objects.get(id=task.group_project.id)

	form = TaskForm(request.POST, instance=task)
	form.fields["assign_collaborator_to_task"] = models.ModelChoiceField(queryset=Collaborators.objects.filter(project=project))
	if request.method == 'POST':
		if form.is_valid():
			save = form.save(commit=False)
			save.group_project = project
			save.save()
			project.task.add(save)
			return redirect('group-project' ,id=project.id)
		else:
			messages.error(request,'Sorry an error occured.')

	context = {
		"project":project,
		"task":task,
		"form":form,
	}

	
	return render(request,'update_task.html',context)

def complete(request,id):
	task = Task.objects.get(id=id)
	project = Group_project.objects.get(id=task.group_project.id)

	#change collaborator label color when task complete
	
	'''collaborator = Collaborators.objects.get(collaborator=request.user,project=project)
	collaborator.label_colour = 'success'
	collaborator.save()'''

	task.done = True
	task.completed_at = timezone.now()
	task.save()
	return redirect('group-project' ,id=project.id)



def add_collab(request,id):
	project = Group_project.objects.get(id=id)
	collaborator = Collaborators.objects.filter(project=project)

	context = {
	 "form": Group_userForm(),
	 "collaborator":collaborator,
	 "project":project,
	}

	if request.method == 'POST':
		form = Group_userForm(request.POST,instance=project)
		if form.is_valid():
			save = form.save(commit=False)
			save.save()
			if User.objects.filter(username=save.add_collaborator):
				user = User.objects.get(username=save.add_collaborator)
				collab = Collaborators.objects.create(collaborator = user,project=project)

				#giving each collabrator different label color
				if Collaborators.objects.filter(project=project,label_colour='warning'):
					collab.label_colour = 'primary'
					if  Collaborators.objects.filter(project=project,label_colour='primary'):
						collab.label_colour = 'dark'
					if Collaborators.objects.filter(project=project,label_colour='dark'):
						collab.label_colour = 'info'
					if  Collaborators.objects.filter(project=project,label_colour='info'):
						collab.label_colour = 'secondary'
					if  Collaborators.objects.filter(project=project,label_colour='secondary'):
						collab.label_colour = 'danger'
					if  Collaborators.objects.filter(project=project,label_colour='danger'):
						collab.label_colour = 'light'
				else:
					collab.save()
				#end label_colour 

				project.collaborators.add(collab)

				profile = UserProfile.objects.get(user=user)
				collab.profile = profile
				collab.save()
				profile.group_project.add(collab.project)
				return redirect('add_collab' ,id=id)
			else:
				messages.warning(request,'The user specified does not exist.')
				return redirect('add_collab' ,id=id)
	else:
		return render(request,'add_collab.html',context)



def remove_collab(request,id):
	collab = Collaborators.objects.get(id=id)
	project = Group_project.objects.get(id=collab.project.id)
	collab.delete()
	messages.info(request,'Collaborator removed from project.')
	return redirect('add_collab' ,id=project.id)


def close_project(request,id):
	project = Group_project.objects.get(id=id)
	project.status = True
	project.save()
	return redirect('group-project' ,id=id)

def open_project(request,id):
	project = Group_project.objects.get(id=id)
	project.status = False
	project.save()
	return redirect('group-project' ,id=id)

	
#end group project





def activity(request,id):
	project = Projects.objects.filter(id=id)
	project_id = Projects.objects.get(id=id)
	activity = project_id.activities.all()
	context =  {
		"form":ListForm(),
		"formurl":ProjectUrlForm(),
		"activity":activity,
		"project":project,
	}
	if request.method == 'POST':
		if project_id.end_date:
			formurl = ProjectUrlForm(request.POST,instance=project_id)
			if formurl.is_valid():
				url = formurl.save(commit=False)
				url.save()
				messages.success(request," And we're off to the next website!")
				return redirect('project_home')

	if request.method == 'POST':
		form = ListForm(request.POST)
		if form.is_valid():
			save = form.save(commit=False)
			save.user = request.user
			save.save()
			project_id.activities.add(save)
			for p in Projects.objects.filter(id=id):
				messages.info(request,'You can add more tasks to your ' + p.title + ' website.')
			return redirect('activity', id=id)
	else:
		return render(request,'activity.html',context)



def done(request,id):
	done =List.objects.get(id=id)
	done.done = True
	done.save()
	pro = Projects.objects.get(activities=done)

	return redirect('activity', id=pro.id)


def delete(request,id):
	delete =List.objects.get(id=id)
	pro = Projects.objects.get(activities=delete)
	delete.delete()

	return redirect('activity', id=pro.id)

def project_complete(request,id):
	project = Projects.objects.get(id=id)
	p = Projects.objects.get(id=id)

	if p.activities.exists():
		if p.activities.filter(done=False):
			messages.warning(request, 'You have not completed all the tasks for your ' + p.title + ' website.')
			return redirect('activity', id=id)
		else:
			project.end_date =  timezone.now()
			project.complete = True
			project.duration = timesince(project.start_date)
			project.save()
			messages.success(request,'Project completed. Please add url for ' + p.title)
			return redirect('activity', id=id)
	else:
		messages.warning(request, 'No tasks were added to this website.')
		return redirect('activity', id=id)










#dev profile
		
def profile(request):
	project = Projects.objects.filter(user=request.user).order_by('-id')
	count = Projects.objects.filter(user=request.user).count()
	p = UserProfile.objects.get(user=request.user)
	profile_group_project = p.group_project.all().order_by('-id')
	group_project = p.group_project.all().count()

	form = UserProfileForm(request.POST,instance=p)
	if request.method == 'POST':
		if form.is_valid():
			save = form.save(commit=False)
			save.update = False
			if 'image' in request.FILES:
					print('found it')
					save.image = request.FILES['image']
			save.save()
			messages.success(request,' Profile Updated.')

	context = {
		"project":project,
		"p":p,
		"form":form,
		"count":count,
		"group_project":group_project,
		"profile_group_project":profile_group_project,

	}

	return render(request,'profile.html',context)


def leave_project(request,id):
	p = UserProfile.objects.get(user=request.user)
	profile_group_project = p.group_project.get(id=id)
	profile_group_project.delete()
	p.save()
	return redirect('profile')

def close_project_owner(request,id):
	project = Group_project.objects.get(id=id)
	project.delete()
	return redirect('profile')





def update(request):
	project = Projects.objects.filter(user=request.user)
	p = UserProfile.objects.get(user=request.user)
	form = UserProfileForm(request.POST,instance=p)
	p.update = True
	p.save()

	context = {
		"form":form,
	}

	return redirect('profile')

def delete_single_project(request,id):
	project = Projects.objects.get(id=id)
	project.delete()
	messages.info(request,'Project was deleted.')
	return redirect('profile')

#end dev profile