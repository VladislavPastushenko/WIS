from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView,PasswordChangeDoneView



#basic
urlpatterns = [

    path('login', views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('profile_edit/<int:id>', views.profile_edit, name='profile_edit'),
    path('create-termin', views.create_termin, name='create-termin'),
    path('get-termins-by-course-id/<int:id>', views.get_termins_by_course_id, name='get-termins-by-course-id'),
    path('get-points-for-all-termins/<int:id_person>/<int:id_course>', views.get_points_for_all_termins, name='get-points-for-all-termins'),
    path('points-of-termin/<int:id>', views.points_of_termin, name='points-of-termin'),

    path('course-edit/<int:id>', views.course_edit, name='course_edit'),
    path('create-course',views.create_course, name='create_course'),
    path('get-courses-by-user-id/<int:id>',views.get_course_user,name='get-course-user'),
    path('get-courses', views.get_courses, name='get-courses'),

    path('get-all-users', views.get_users, name='get-all-users'),
    path('get-course-by-id/<int:id>', views.get_course_by_id, name='get-course-by-id'),
    path('get-logged-user', views.get_logged_user, name='get-logged-user'),

    path('add-user-to-course/<int:id_person>/<int:id_course>', views.add_user_to_course, name='add-user-to-course'),
    path('remove-user-from-course/<int:id_person>/<int:id_course>', views.remote_user_from_course, name='remove-user-from-course'),
    path('add-user-to-termin/<int:id_person>/<int:id_termin>', views.add_user_to_termin, name='add-user-to-termin'),
    path('remote-user-from-termin/<int:id_person>/<int:id_termin>', views.remote_user_from_termin, name='remote-user-from-termin'),
    
    path('remove-user/<int:id_persone>',views.remove_user,name='remove-user'),
    path('remove-course/<int:id_course>',views.remove_course,name='remove-course'),
    path('update-termin/<int:id_termin>',views.update_termin,name='update_termin'),
    
    #room path
    path('add-room',views.add_room,name='add-room'),
    path('get-all-classrooms',views.get_classrooms,name='get-all-classrooms'),
    path('delete-room/<int:id_room>',views.delete_room,name='delete-room'),
    
    path('add-lector-to-course',views.add_lector_to_course,name='add-lector-to-course'),
    path('delete-lector-to-course',views.delete_lector_course,name='delete-lector-to-course'),
    
    path('get_garant_courses/<int:id_person>',views.get_garant_courses,name='get_garant_courses')
    
    
]

handler404 = "main.views.page404"