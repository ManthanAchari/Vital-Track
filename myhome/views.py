from django.shortcuts import render
from .models import Signup,HealthRecord 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_sys
from django.shortcuts import redirect
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib import messages

# Create your views here.
def login(request):
    return render(request,"myhome/login.html")

def home(request):
    return render(request,"myhome/home.html")

def entry(request):
    return render(request,"myhome/entry.html")

def dashboard(request):
    return render(request,"myhome/dashboard.html")

def signup(request):
    return render(request,"myhome/signup.html")

def loginentry(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["pass"]

        user=authenticate(
            username=email,
            password=password
        )

        if user:
            login_sys(request,user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
    else:
        return render(request,"myhome/login.html")

def signupentry(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        passw=request.POST['passw']
        age=request.POST['age']
        sex=request.POST['sex']

        user=User.objects.create_user(
            username=email,
            email=email,
            password=passw
        )

        Signup.objects.create(
            user=user,
            name=name,
            age=age,
            sex=sex
        )
        return redirect("loginentry")
    else:
        return render(request,"myhome/signup.html")

def submit(request):
    if request.method=='POST':
        data=request.POST
        bp=data.get("bp")
        sugar=data.get("sugar")
        oxy=data.get("oxy")
        pulse=data.get("pulse")
        temperature=data.get("temp")

        HealthRecord.objects.create(
                user=request.user,
                bp=bp,
                sugar=sugar,
                oxy=oxy,
                pulse=pulse,
                temperature=temperature
        )
        return redirect('dashboard')
    
    return redirect('entry')

def graph(request):
    records=HealthRecord.objects.filter(user=request.user).order_by('date')
    if not records.exists():
        message="No records found"
    DATE=[r.date.strftime("%d-%m") for r in records]
    BP=[r.bp for r in records]
    SUGAR=[r.sugar for r in records]
    OXYGEN=[r.oxy for r in records]
    PULSE=[r.pulse for r in records]
    TEMPERATURE=[r.temperature for r in records]

    fig,axes=plt.subplots(2,2,figsize=(12,10))

    axes[0][0].plot(DATE,BP,marker='o',markerfacecolor="red")
    axes[0][0].set_title("Bp Analysis",fontsize=15)
    axes[0][0].set_xlabel("Date",color='blue')
    axes[0][0].set_ylabel("Bp",color='blue')

    axes[0][1].plot(DATE,SUGAR,marker='o',markerfacecolor='red')
    axes[0][1].set_title("Sugar Analysis",fontsize=15)
    axes[0][1].set_xlabel("Date",color='blue')
    axes[0][1].set_ylabel("Sugar",color='blue')

    axes[1][0].plot(DATE,OXYGEN,marker='o',markerfacecolor="red")
    axes[1][0].set_title("Oxygen Analysis",fontsize=15)
    axes[1][0].set_xlabel("Date",color='blue')
    axes[1][0].set_ylabel("Oxygen",color='blue')

    axes[1][1].plot(DATE,PULSE,marker='o',markerfacecolor="red")
    axes[1][1].set_title("Pulse-Rate Analysis",fontsize=15)
    axes[1][1].set_xlabel("Date",color='blue')
    axes[1][1].set_ylabel("Pulse_Rate",color='blue')

    plt.tight_layout()

    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image=buffer.getvalue()
    graph=base64.b64encode(image).decode('utf-8')
    buffer.close()
    plt.close('all')

    return render(request,"myhome/dashboard.html",{"graph":graph})

def pushdata(request):
    data=HealthRecord.objects.filter(user=request.user).order_by('date')
    if not data.exists():
        message="No records found"

    recog=Signup.objects.get(user=request.user)

    return render(request,"myhome/userrecords.html",{"data":data, "recog":recog})
    