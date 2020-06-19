from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
import pyrebase


config={
    'apiKey': "AIzaSyABz0n3otYpBXuPF8q_pS-N0rSwwL98gxc",
    'authDomain': "journal-61748.firebaseapp.com",
    'databaseURL': "https://journal-61748.firebaseio.com",
    'projectId': "journal-61748",
    'storageBucket': "journal-61748.appspot.com",
    'messagingSenderId': "711085520514",
    'appId': "1:711085520514:web:7c55b77245e54aeca9269b"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()


# Create your views here.
def home(request):
    return render(request,'home.html')
'''def signup(request):
    if request.method == "POST":
        # create user
        if request.POST['password1'] == request.POST['password2']:#both the password checked
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'register.html', {'error': "Username  has been already taken"})

            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email'])
                auth.login(request, user) #createdvand login
                return redirect(home)
        else:
            return render(request,'register.html',{'error':"Password don't match"})
    else:
        return render(request,'register.html')
        '''''


def signup(request):
    return render(request,"register.html")


def post_signup(request):
    name = request.POST.get('username')
    email = request.POST.get('email')
    passw = request.POST.get('password')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})
    uid = user['localId']
    data = {"name": name, "status": "1"}
    db.child("users").child(uid).child("details").set(data)
    return render(request, "home.html")


def logout(request):
    auth.logout(request)
    return render(request, 'home.html')


def login(request):

        #check if a user exists
        #with thr username and password
        email = request.POST.get("email")
        pwd = request.POST.get("password")
        try:
            user = authe.sign_in_with_email_and_password(email,pwd)
        except:
            message="Invalid Credentials"
            return render(request, 'home.html',{"mssg": message})
        print(user)
        print(user['idToken'])
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        return render(request, 'showdiary.html')

def add(request):
    return render(request,'addstudent.html')


def create(request):

    return render(request,'journal.html')


def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    video = request.POST.get('video')
    description =request.POST.get('descript')
    visibility=request.POST.get('visible')
    title=request.POST.get('title')
    suggestion=request.POST.get('suggestion')
    Checklist = request.POST.get('checklist')
    Age = request.POST.get('age')
    category=request.POST.get('category')
    Level= request.POST.get('level')

    Prompt = request.POST.get('Prompt')
    step_1=request.POST.get('text')
    step_2=request.POST.get('text')
    step_3=request.POST.get('text')

    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        'Title': title,
        'Description': description,
        'Visibility': visibility,
        'category': category,
        'age':Age,
        "video":"YUdsgQGHSR8",
        "Level":Level,
        "Prompt":Prompt,
        "Suggestion": suggestion,
        "Checklist":Checklist,
        "Instructions":
        {
            "Step1" : step_1,
            "Step2":step_2,
            "Step3":step_3,
        }
    }

    db.child('users').child('homeplan').set(data)
    return render(request,'journal.html')







def name(request):

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    child_name =request.POST.get('message')
    return render(request, 'name.html',{child_name: child_name})


def home_view(request):
    print(request.GET)
    return render(request, "home.html")



def check(request):

    import time
    from datetime import datetime, timezone
    import pytz

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    child_name = request.POST.get('message')
    print(a)
    print(child_name)

    users1 = db.child("Vibhu").shallow().get()
    print(users1.key())
    users=[]
    info=[]
    for j in users1.val():
       # users.append(db.child("tim").child(j).shallow().get().val())
        info.append(db.child("Vibhu").child(j).child().get().val())
    print(info)
    #print("########################################################")
    #print(users)
    '''
    comp_list = list(zip(users, info))
    print(comp_list)
    '''
    k=[]
    v=[]
    for i in info:
        for key,value in i.items():
            k.append(key)
            v.append(value)

    comp_list=zip(k,v)

    return render(request, 'check.html', {'comp_list':comp_list})


















''' lis_time=[]
    for i in timestamps:

        lis_time.append(i)

    lis_time.sort(reverse=True)

    print(lis_time)
    work = []
    fo=[]


    for i in lis_time:

        wor=db.child('users').child(a).child('reports').child(i).child('Activity').get().val()
        food=db.child('users').child(a).child('reports').child(i).child('food').get().val()
        work.append(wor)
        fo.append(food)
    print(work)

    date=[]
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    print(date)

    comb_lis = zip(lis_time,date,work,fo)
    name = db.child('users').child(a).child('details').child('email').get().val()
    

    return render(request,'check.html',{'comb_lis':comb_lis,'e': child_name})'''

