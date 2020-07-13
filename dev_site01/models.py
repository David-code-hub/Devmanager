from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	image = models.ImageField(blank=True,null=True,upload_to='image/')
	projects = models.ManyToManyField('Projects')
	group_project = models.ManyToManyField('Group_project')
	email = models.EmailField(blank=True,null=True)
	update = models.BooleanField(default=False)
	bio = models.TextField(max_length=300,null=True,blank=True)


	def __str__(self):
		return str(self.user)

class Projects(models.Model):
	start_date = models.DateField()
	end_date = models.DateTimeField(blank=True,null=True)
	duration = models.CharField(max_length=50,null=True,blank=True)
	title = models.CharField(max_length=100)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	activities = models.ManyToManyField('List',blank=True)
	project_url = models.URLField(blank=True,null=True)
	complete = models.BooleanField(default=False)
	website_owner = models.CharField(max_length=70,null=True,blank=True) 
	outstanding_requirements = models.CharField(max_length=200,null=True,blank=True)
	challenges = models.TextField(max_length=500,null=True,blank=True)



	def __str__(self):
		return str(self.user) + ' : ' +  self.title + ' (' + ' Project ' + ')'


class List(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	project = models.ForeignKey(Projects,on_delete=models.CASCADE,null=True)
	activity = models.TextField(max_length=10000)
	done = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user) + ' ' + str(self.activity)


class Group_project(models.Model):
	project_title = models.CharField(max_length=90)
	lead = models.ForeignKey(User,on_delete=models.CASCADE,related_name="lead_of_project",null=True)
	collaborators = models.ManyToManyField('Collaborators',blank=True,
		related_name="collaborator_working_on_group_project")
	task = models.ManyToManyField('Task',blank=True,related_name="task_related_to_project")
	add_collaborator = models.CharField(max_length=80,null=True,blank=True)
	status = models.BooleanField(default=False)

	def __str__(self):
		return str(self.project_title)

class Collaborators(models.Model):
	project = models.ForeignKey(Group_project,on_delete=models.CASCADE,null=True,related_name="collaborator_in_project")
	profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
	collaborator = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	label_colour = models.CharField(max_length=90,choices=( 
		('primary','primary'),
		('dark','dark'),
		('warning','warning'),
		('info','info'),
		('secondary','secondary'),
		('danger','danger'),
		('light','light'),),default='warning')
	active = models.BooleanField(default=True)


	def __str__(self):
		return str(self.collaborator)




class Task(models.Model):
	assign_collaborator_to_task = models.ForeignKey(Collaborators,on_delete=models.CASCADE)
	group_project = models.ForeignKey(Group_project,on_delete=models.CASCADE,null=True,related_name="project_related_to_task")
	task = models.TextField(max_length=10000)
	done = models.BooleanField(default=False)
	in_progress = models.BooleanField(default=False)
	completed_at = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return str(self.assign_collaborator_to_task) + ' ' + str(self.task)