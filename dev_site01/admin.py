from django.contrib import admin
from .models import List,Projects,UserProfile,Group_project,Task,Collaborators
# Register your models here.


admin.site.register(List)
admin.site.register(Projects)
admin.site.register(UserProfile)
admin.site.register(Group_project)
admin.site.register(Task)
admin.site.register(Collaborators)