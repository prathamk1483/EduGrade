from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import StudentMarks as sm
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

def home(request):
    page=''
    context={'page' : page}
    return render(request,'base/home.html',context)


def insert(request):
    if request.user.username != 'pratham':
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        roll = request.POST.get('loginroll')
        studname = request.POST.get('Loginname')
        marks = request.POST.get('Loginpassword')
        ls = sm.objects.all().using("new")
        for i in ls:
            print(i)
            if i.id == int(roll):
                return  HttpResponse('Roll no should be unique')
        sm.objects.using("new").create(id =roll, name = studname , marks = marks)
        messages.add_message(request,messages.INFO , 'Inserted Successfully')
    return render(request,'insert.html')


def update(request):
    Slist = sm.objects.all().using("new")
    context = {'Thelist' : Slist}
    print('hellow rold')
    if request.user.username != 'pratham':
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':

        studname = request.POST.get('updatename')
        marks1 = request.POST.get('updatepassword1')
        marks2 = request.POST.get('updatepassword2')
        print(studname, marks1,marks2 , 'This is what i got ')

        person = sm.objects.using("new").get(id = studname)
        print(person)
        person.marks = marks2
        person.save(using = "new")
        messages.add_message(request,messages.INFO , 'updated Successfully')    
        return redirect('update')
    return render(request,'dis_up_del.html',context)


def delete(request):
    Slist = sm.objects.all().using("new")
    context = {'Thelist' : Slist}
    if request.user.username != 'pratham':
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        studname = request.POST.get('updatename')
        person = sm.objects.using("new").get(id = studname)   
        person.delete() 
    return render(request,'dis_up_del.html',context)


def display(request):
    if request.user.username == 'pratham':
        Slist = sm.objects.all().using("new")
        context = {'Thelist' : Slist}
    else:
        Slist = sm.objects.all().using("new")
        for i in Slist:
            if i.name == request.user.username :
                id = i.id
        Slist = sm.objects.using("new").filter(id = id)
        Slist = list(Slist)
        context = {'Thelist' : Slist}
    return render(request,'dis_up_del.html',context)

# Create your views here.
def home(request):
    return render(request,'home.html')

def LoginPage(request):
    page_title = "Login"
    if request.method == "POST":
        postdata = request.POST.copy()
        username = postdata.get('username', '')
        password = postdata.get('password', '')
        print(username,password,'printed data')
        try:
            user = User.objects.get(username=username , email=password)
            print(user)
            if user is not None:
                login(request, user)
                print('User logged in')
                return redirect('home')
            else:
                print('User not logged in')
                error = True
        except:
            print('User not logged in')
            error = True

    return render(request, 'login.html', {'page_title': page_title})


def SignupPage(request):
    if request.method == "POST":
        postdata = request.POST.copy()
        username = postdata.get('username', '')
        password = postdata.get('password1', '')
        print(username,password)
        # check if user does not exist
        if User.objects.filter(username=username).exists():
            username_unique_error = True


        else :
            create_new_user = User.objects.create_user(username, password)
            create_new_user.save()
            user = authenticate(username=username, password=password)
            print(user)
            login(request, user)
            print('User Logged In by signing in ')
            if create_new_user is not None:
                if create_new_user.is_active:  
                    return redirect('home')
                else:
                    print("The password is valid, but the account has been disabled!")



    return render (request,'signup.html')



def LogoutPage(request):
    logout(request)
    print('user logged out')
    return redirect('home')






