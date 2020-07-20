from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.login_index,name="home"),
	path('signup/', views.signup,name="signup"),
	path('signout/', views.signout,name="signout"),
	path('home/', views.project_home,name="project_home"),


	#single project urls
	path('activity/<int:id>/', views.activity,name="activity"),
	path('done/<int:id>/', views.done,name="done"),
	path('delete_list/<int:id>/', views.delete,name="delete_list"),
	path('complete/<int:id>/', views.project_complete,name="complete_project"),
	path('delete-single-project/<int:id>/', views.delete_single_project,name="delete_single_project"),


	#profile urls
	path('profile/', views.profile,name="profile"),
	path('update/', views.update,name="update"),
	path('leave_project/<int:id>/', views.leave_project,name="leave_project"),
	path('close_project_owner/<int:id>/', views.close_project_owner,name="close_project_owner"),


	#group project urls
	path('user/<int:id>/', views.user_select,name="user_select"),
	path('group-project/<int:id>/', views.group_project,name="group-project"),
	path('add-collab/<int:id>/', views.add_collab,name="add_collab"),
	path('complete_task/<int:id>/', views.complete,name="complete"),
	path('remove_collab/<int:id>/', views.remove_collab,name="remove_collab"),
	path('close_project/<int:id>/', views.close_project,name="close_project"),
	path('open_project/<int:id>/', views.open_project,name="open_project"),
	path('update-task/<int:id>/', views.update_task,name="update_task"),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

