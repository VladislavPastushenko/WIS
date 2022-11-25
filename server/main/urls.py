from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView,PasswordChangeDoneView



#basic
urlpatterns = [
    path('404', views.page404, name='page_404'),
    path('access_failed', views.access_failed, name='access_failed'),

    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('study', views.study_view, name='study'),
    path('logged', views.logged_view, name='loggend_on'),
    path('profile', views.profile_view, name='profile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('<int:id>', views.courses_view, name='courses-view'),
    path('admin_view', views.admin_view, name='admin_view'),
    path('user_update/<int:id>', views.user_update, name='user_update'),
    path('user_delete/<int:id>', views.user_delete, name='user_delete'),
    
    path('create-termin', views.create_termin, name='create-termin'),
    path('get-termins-by-course-id/<int:id>', views.get_termins_by_course_id, name='get-termins-by-course-id'),
    path('get-points-for-all-termins/<int:id_person>/<int:id_course>', views.get_points_for_all_termins, name='get-points-for-all-termins'),
    path('points-of-termin/<int:id>', views.points_of_termin, name='points-of-termin'),

    path('create-course',views.create_course, name='create_course'),
    path('get-courses-by-user-id/<int:id>',views.get_course_user,name='get-course-user'),
    path('get-courses', views.get_courses, name='get-courses'),

    path('get-all-users/', views.get_users, name='get-all-users'),
    path('get-course-by-id/<int:id>', views.get_course_by_id, name='get-course-by-id'),
    path('get-logged-user', views.get_logged_user, name='get-logged-user'),

    path('add-user-to-course/<int:id_person>/<int:id_course>', views.add_user_to_course, name='add-user-to-course'),
    path('remove-user-from-course/<int:id_person>/<int:id_course>', views.remote_user_from_course, name='remove-user-from-course'),
    
    
    path('remove-user/<int:id>',views.remove_user,name='remove-user'),
    path('remove-course/<int:id>',views.remove_course,name='remove-course'),
    
    path('update-termin/<int:id>',views.update_termin,name='update_termin'),
    
]

handler404 = "main.views.page404"