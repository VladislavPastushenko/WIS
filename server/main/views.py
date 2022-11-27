from atexit import register
from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
import json
import base64

# Create your views here.


def page404(request, exceptio):
    return

def authorize_by_request(request):
    authorization_header = request.META['HTTP_AUTHORIZATION']
    base64_bytes = authorization_header.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    credentials = message.split(' ')
    user = authenticate(request,username=credentials[0],password=credentials[1])
    if user is not None:
        login(request, user)
        return user
    else:
        return HttpResponse(status=401)

def get_courses(request):
    courses = list(Course.objects.values())
    
    for course in courses:
        count = Student_Course.objects.filter(id_course=course['id_course']).count()
        course['count'] = count
        course['garant'] = list(Person.objects.filter(id_person=course['garant_id']).values())[0]
        course['lectors'] = list(Teacher_Course.objects.filter(id_course=course['id_course']).values())
    return JsonResponse(courses, safe = False)

def get_users(request):
    role = request.GET.get('role')
    if role != None:
        person = list(Person.objects.filter(role=role).values())
        if role == 'l':
            person = person + list(Person.objects.filter(role='g').values())
    else:
        person = list(Person.objects.values())

    person_list = list()
    for item in person:
        user = User.objects.filter(email=item['email']).first()
        item['username'] = user.username
        item['password'] = user.password
        person_list.append(item)
    return JsonResponse(person_list, safe = False)

def get_users_in_course(request, id):
    person_list = list()
    students = list(Student_Course.objects.filter(id_course=id))
    for item in students:
        person = Person.objects.filter(id_person=item['id_student']).first()
        user = User.objects.filter(email=person.email).first()
        person['username'] = user.username
        person['password'] = user.password
        person_list.append(person)
    return JsonResponse(person_list, safe = False)

def get_course_by_id(request, id):
    course = Course.objects.filter(id_course=id).values()[0]
    return JsonResponse(course, safe = False)

def get_logged_user(request):
    user = authorize_by_request(request=request)
    person_instance = list(Person.objects.filter(user=request.user).values())[0]
    return JsonResponse({**person_instance, 'username': user.get_username()}, safe = False)


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)

            username = json_data['username']
            firstName = json_data['firstName']
            lastName = json_data['lastName']
            email = json_data['email']
            password = json_data['password']


            user_instance = User.objects.create_user(username=username, email=email, password=password)
            user = Person.objects.create(user=user_instance, firstname=firstName, surname=lastName, email=email, role='s')

            print(username)
            if user is not None:
                return HttpResponse('ok')
            else:
                return HttpResponse(status=500)
        except:
            return HttpResponse(status=500)

@csrf_exempt
def profile_edit(request, id):
    if request.method == 'POST':
        user = authorize_by_request(request=request)
        try:
            person_instance = Person.objects.filter(id_person=id).first()
            json_data = json.loads(request.body)

            user_instance = User.objects.filter(email=person_instance.email).first()
            username = json_data.get('username') if json_data.get('username') != None else user_instance.username
            password = json_data.get('password') if json_data.get('password') != None else user_instance.password
            firstname = json_data.get('firstname') if json_data.get('firstname') != None else person_instance.firstname
            firstname = json_data.get('firstname') if json_data.get('firstname') != None else person_instance.firstname
            surname = json_data.get('surname') if json_data.get('surname') != None else person_instance.surname
            address = json_data.get('address') if json_data.get('address') != None else person_instance.address
            email = json_data.get('email') if json_data.get('email') != None else person_instance.email
            telephone = json_data.get('telephone') if json_data.get('telephone') != None else person_instance.telephone
            role = json_data.get('role') if json_data.get('role') != None else person_instance.role

            active_person = Person.objects.filter(user=request.user).first()
            if role != None and active_person.is_admin == False:
                return HttpResponse(status=500)
            elif active_person.is_admin == False and person_instance.id_person != active_person.id_person:
                return HttpResponse(status=500)

            User.objects.filter(email=person_instance.email).update(username=username, email=email, password=password)

            Person.objects.filter(id_person=person_instance.id_person).update(firstname=firstname,
                                                                              surname=surname,
                                                                              address=address,
                                                                              telephone=telephone,
                                                                              email=email,role=role)
            return HttpResponse('ok')
        except:
            return HttpResponse(status=500)

@csrf_exempt
def add_lector_func(id_person,id_course):
    print('id_person', id_person)
    print('id_course', id_course)
    lector = Person.objects.filter(id_person=id_person).first()
    if lector.role != 'l':
        return HttpResponse('is not lector',status=500)

    course = Course.objects.filter(id_course=id_course).first()

    try:
        Teacher_Course.objects.create(id_teacher=lector,id_course=course)
        return HttpResponse('ok')
    except:
        return HttpResponse('error create teacher_course object',status=500)



@csrf_exempt
def course_edit(request, id):
    if request.method == 'POST':
        try:
            user = authorize_by_request(request=request)
            person_instance = Person.objects.filter(user=request.user).first()
            if person_instance.is_garant == False:
                return HttpResponse(status=500)

            course_instance = Course.objects.filter(id_course=id).first()
            json_data = json.loads(request.body)

            abbrv = json_data.get('abbrv') if json_data.get('abbrv') != None else course_instance.abbrv
            title = json_data.get('title') if json_data.get('title') != None else course_instance.title
            description = json_data.get('description') if json_data.get('description') != None else course_instance.description
            credits = json_data.get('credits') if json_data.get('credits') != None else course_instance.credits
            max_persons = json_data.get('max_persons') if json_data.get('max_persons') != None else course_instance.max_persons
            approved = json_data.get('approved') if json_data.get('approved') != None else course_instance.approved
            type = json_data.get('type') if json_data.get('type') != None else course_instance.type
            lectors = json_data.get('lectors_id')
            for item in lectors:
                 add_lector_func(item, id)

            Course.objects.filter(id_course=course_instance.id_course).update(abbrv=abbrv,
                                                                              title=title,
                                                                              description=description,
                                                                              max_persons=max_persons,
                                                                              credits=credits,
                                                                              approved=approved, 
                                                                              type=type)
            return HttpResponse('ok')
        except:
            return HttpResponse(status=500)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            username = json_data['username']
            password = json_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                person_instance = list(Person.objects.filter(user=request.user).values())[0]
                return JsonResponse({**person_instance, 'username': user.get_username()}, safe = False)
            else:
                return HttpResponse(status=401)
        except:
            return HttpResponse(status=500)



def logout_user(request):
    logout(request)
    messages.success(request,"You Were logout")
    return redirect("/")


def check_room_time(classroom,time_start,time_end,date):
    termins = list(Termin.objects.filter(classroom=classroom).all())

    for item in termins:
        
        if((time_start > item.time_start and time_start < item.time_end)
            or 
            (time_end >item.time_start and time_end < item.time_end)): return True

    return False
        

@csrf_exempt
def create_termin(request, id):
    if request.method == 'POST':
        try:
            active_person = Person.objects.filter(user=request.user).first()
            if active_person.is_garant == False:
                return HttpResponse(status=500)

            json_data = json.loads(request.body)

            name = json_data['name']  
            repeted = json_data['repeted']  
            time_start = json_data['time_start']  
            time_end = json_data['time_end']  
            date = json_data['date']  
            weekday = json_data['weekday'] 
            max_points = json_data['max_points'] 
            classroom = json_data['classroom'] 
            type = json_data['type']
            description = json_data['description']
            
            
            auto_register = json_data['auto_register']
            
            capacita = json_data['capacita']

            classroom_instance = Classrooms.objects.filter(name=classroom).first()
            course_instance = Course.objects.filter(id_course=id).first()

            try:
                Termin.objects.create(name=name,repeted=repeted,time_start=time_start,
                                        time_end=time_end,date=date,
                                        weekday=weekday,max_points=max_points,
                                        type=type, id_course=course_instance,
                                        id_classroom=classroom_instance, description=description,capacita=capacita,auto_register=auto_register)
            except:
                print("error create course")    

            return HttpResponse('ok')

        except:
            return HttpResponse(status=500)

def get_termins_by_course_id(request, id):
    course_instance = Course.objects.filter(id_course=id).first()
    termins = list(Termin.objects.filter(id_course=course_instance).values())
    return JsonResponse(termins, safe = False)

def get_points_for_all_termins(request, id_person, id_course):
    course_instance = Course.objects.filter(id_course=id_course).first()
    termins = list(Termin.objects.filter(id_course=course_instance).values())
    person_instance = Person.objects.filter(id_person=id_person)
    termin_points = list()
    for item in termins:
        termin = User_Termin.objects.filter(id_student=id_person,id_termin = item['id_termin']).values()[0]
        item.update({'points' : termin.get('points')})
        termin_points.append(item)
    return JsonResponse(termin_points, safe = False)

def points_of_termin(request, id):
    termin_instance = Termin.objects.filter(id_termin=id).first()
    user_termin = list(User_Termin.objects.filter(id_termin=id).values())

    person_points = list()
    for item in user_termin:
        person_instance = Person.objects.filter(id_person=item['id_student_id']).values()[0]
        user = User.objects.filter(email=person_instance.email).first()
        person_instance['username'] = user.username
        person_instance['password'] = user.password
        person_instance['points'] = item['points']
        person_points.append(person_instance)
    return JsonResponse(person_points, safe = False)

def create_course(request):
    if request.method == 'POST':
        try:
            active_person = Person.objects.filter(user=request.user).first()
            if active_person.is_garant == False:
                return HttpResponse(status=500)

            json_data = json.loads(request.body)

            abbrv = json_data['abbrv']  
            title = json_data['title']  
            description = json_data['description']  
            credits = json_data['credits']  
            max_persons = json_data['max_persons']  
            garant = json_data['username'] 

            user_instance = User.objects.filter(username=garant).first()
            person_instance = Person.objects.filter(user=user_instance).first()

            try:
                Course.objects.create(abbrv=abbrv,title=title,description=description,
                                        credits=credits,max_persons=max_persons,
                                        garant_id=person_instance,approved=0)
            except:
                print("error create course")    

            return HttpResponse('ok')

        except:
            return HttpResponse(status=500)


#@login_required
def get_course_user(request,id):
    if request.user.is_authenticated:
        student_course = list(Student_Course.objects.filter(id_student = id).values())
        course_list = list()
        for item in student_course:
            course = Course.objects.filter(id_course = item['id_course_id']).values()[0]
            course_list.append(course)
        return JsonResponse(course_list, safe = False)
    else:
       return HttpResponse(status=500)


def add_user_to_course(request, id_person, id_course):
    # if request.method == 'POST':
        course = Course.objects.filter(id_course=id_course).first()
        person = Person.objects.filter(id_person=id_person).first()
        Student_Course.objects.create(id_student=person, id_course=course)
        termins = list(Termin.objects.filter(id_course=course).values())
        for item in termins:
            termin = Termin.objects.filter(id_termin=item['id_termin']).first()
            User_Termin.objects.create(id_student=person, id_termin=termin, points=0)
        return HttpResponse('ok')

def remote_user_from_course(request, id_person, id_course):
    # if request.method == 'POST':
        course = Course.objects.filter(id_course=id_course).first()
        person = Person.objects.filter(id_person=id_person).first()
        Student_Course.objects.filter(id_student=person,id_course=course).delete()
        termins = list(Termin.objects.filter(id_course=course).values())
        for item in termins:
            User_Termin.objects.filter(id_student=person, id_termin=item['id_termin']).delete()
        return HttpResponse('ok')
    
def remove_user(request,id_persone):
    try:
        Course.objects.filter(garant_id=id_persone).update(garant_id = '')
        
        teacher_course_list = list(Teacher_Course.objects.filter(id_teacher=id_persone).all())
        student_course_list = list(Student_Course.objects.filter(id_student=id_persone).all())
        user_termin_list = list(User_Termin.objects.filter(id_student=id_persone).all())

        for item in teacher_course_list: item.delete()
        for item in student_course_list: item.delete()
        for item in user_termin_list: item.delete()

        User.objects.filter(id_persone=id_persone).delete()
        Person.objects.filter(id_persone=id_persone).delete()
        return HttpResponse('ok')
    
    except:
        return HttpResponse('error')
 
def remove_course(request,id_course):
    try:
        termin_list = list(Termin.objects.filter(id_course=id_course).all())
        student_course_list = list(Student_Course.objects.filter(id_course=id_course).all())
        teacher_course_list = list(Teacher_Course.objects.filter(id_course=id_course).all())
        
        for item in termin_list: item.delete()
        for item in student_course_list: item.delete()
        for item in teacher_course_list: item.delete()

        
        Course.objects.filter(id_course=id_course).delete()
        return HttpResponse('ok')   

    except:
        return HttpResponse('error')

def update_termin(request,id_termin):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            termin_instance = Termin.objects.filter(id_termin=id_termin).first()

            name = json_data.get('name') if json_data.get('name') != None else termin_instance.name
            repeted = json_data.get('repeted') if json_data.get('repeted') != None else termin_instance.repeted 
            time_start = json_data.get('time_start') if json_data.get('time_start') != None else termin_instance.time_start 
            time_end = json_data.get('time_end') if json_data.get('time_end') != None else termin_instance.time_end 
            date = json_data.get('date') if json_data.get('date') != None else termin_instance.date  
            weekday = json_data.get('weekday') if json_data.get('weekday') != None else termin_instance.weekday
            max_points = json_data.get('max_points') if json_data.get('max_points') != None else termin_instance.max_points
            classroom = json_data.get('classroom') if json_data.get('classroom') != None else termin_instance.classroom
            type = json_data.get('type') if json_data.get('type') != None else termin_instance.type
            description = json_data.get('description') if json_data.get('description') != None else termin_instance.description
            
            
            classroom_instance = Classrooms.objects.filter(name=classroom).first()

            try:
                Termin.objects.filter(id_termin=id_termin).update(name=name,repeted=repeted,time_start=time_start,
                                            time_end=time_end,date=date,
                                            weekday=weekday,max_points=max_points,
                                            type=type,id_classroom=classroom_instance, description=description)
            except:
                return HttpResponse(status=500)            
            return HttpResponse('ok')

        except:
            return HttpResponse(status=500)
        
        

def check_room(name):
    if(Classrooms.objects.filter(name=name).first()): return True
    return False

def get_classrooms(request):
    classrooms = list(Classrooms.objects.values())
    return JsonResponse(classrooms, safe = False)

@csrf_exempt
def add_room(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        name = json_data['name']

        try:
            if(check_room(name) == False):
                Classrooms.objects.create(name=name)
            else:
                return HttpResponse('Error: name exist',status=500)
        except: 
            return HttpResponse(status=500)

        return HttpResponse('ok')
    
    return HttpResponse('error')

def delete_room(request,id_room):
    try:
        Classrooms.objects.filter(id_classroom=id_room).delete()
        return HttpResponse('ok')
    except:
         return HttpResponse(status=500)


@csrf_exempt   
def add_lector_to_course(request):
    
    if request.method == 'POST':
        json_data = json.loads(request.body)
        
        id_person = json_data['id_person']
        id_course = json_data['id_course']

    
        lector = Person.objects.filter(id_person=id_person).first()
        if lector.role != 'l':
            return HttpResponse('is not lector',status=500)

        course = Course.objects.filter(id_course=id_course).first()
        
        try:
            Teacher_Course.objects.create(id_teacher=lector,id_course=course)
            return HttpResponse('ok')
        except:
            return HttpResponse('error create teacher_course object',status=500)


@csrf_exempt   
def delete_lector_course(request):
    if request.method == "POST":
        
        json_data = json.loads(request.body)
        
        id_person = json_data['id_person']
        id_course = json_data['id_course']
        
        try:
            Teacher_Course.objects.filter(id_teacher=id_person,id_course=id_course).delete()
            return HttpResponse('ok')
        except:
            return HttpResponse('error delete teacher_course object',status=500)


def get_garant_courses(request,id_person):
    courses = list(Course.objects.filter(garant_id=id_person).values())
    return courses
