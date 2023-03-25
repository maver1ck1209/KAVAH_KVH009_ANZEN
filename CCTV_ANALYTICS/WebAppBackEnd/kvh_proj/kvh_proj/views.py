from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
import string
import pyrebase
import datetime
import pandas as pd
import json
from gtts import gTTS
import os
from playsound import playsound
  

config={
"apiKey": "AIzaSyCDAGglBwh-7NEU4lAFTS7f5tbGacUXdMA",
  "authDomain": "kvh-proj.firebaseapp.com",
  "projectId": "kvh-proj",
  "storageBucket": "kvh-proj.appspot.com",
  "messagingSenderId": "348476571342",
  "appId": "1:348476571342:web:9aa8f6c522c33a2f171a9f",
  "measurementId": "G-FW36366BN7",
  "databaseURL": "https://kvh-proj-default-rtdb.firebaseio.com"
}

db=pyrebase.initialize_app(config)
store=db.storage()

rl_db=db.database()
@login_required(login_url='/login')
def index(request):
    return render(request, "index.html")

def login_user(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            otp = str(random.randint(1000,9999)) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) 
            otp = ''.join(random.sample(otp,len(otp)))
            request.session['otp'] = otp
            messages.success(request, f' welcome {username} !!')
            return redirect('home')
        else:
            messages.error(request, f'account does not exit plz register')
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})
def incidents(request):
    if request.method=="GET":
        vals=rl_db.child("incidents").get().val()
        loc_vals=rl_db.child("location").get().val()
        tmp={}
        tmp['IncidentId']=[]
        tmp['IncidentType']=[]
        tmp['CamId']=[]
        tmp['District']=[]
        tmp['Latitude']=[]
        tmp['Longitude']=[]
        tmp['Time']=[]
        tmp['gmap']=[]
        s = ""
        for i in vals:
            tmp["IncidentId"].append(i)
            tmp["IncidentType"].append(vals[i]["incident_type"])
            tmp["CamId"].append(vals[i]['cam_id'])
            tmp["Time"].append(vals[i]['incident_time'])
            tmp["District"].append(loc_vals[vals[i]['cam_id']]['district'])
            tmp["Latitude"].append(loc_vals[vals[i]['cam_id']]['latitude'])
            tmp["Longitude"].append(loc_vals[vals[i]['cam_id']]['longitude'])
            tmp["gmap"].append(loc_vals[vals[i]['cam_id']]['gmap'])
            s = "Crime of type " + vals[i]["incident_type"] + "has occured in " + str(loc_vals[vals[i]['cam_id']]['district']) + "with coordinates " + str(loc_vals[vals[i]['cam_id']]['latitude']) + str(loc_vals[vals[i]['cam_id']]['longitude'])
        
        lang = ['en', 'hi', 'ta']
        for i in range(2):
            for i in lang:
                myobj = gTTS(text=s, lang=i, slow=False)
                myobj.save("detected.mp3")
                os.system("mpg321 detected.mp3")
                playsound('detected.mp3')
                os.remove('detected.mp3')


        df=pd.DataFrame(tmp)
        json_recs=df.reset_index().to_json(orient='records')
        data=json.loads(json_recs)
        context={'d':data}
        return render(request,"incidents.html",context)
    
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            #EMAIL
            htmly = get_template('Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            #Redirect to login
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form":form})

def submit(request):
    inc_id=rl_db.generate_key()
    inc_name=request.GET("name")
    inc_type=request.GET("type")
    inc_time=datetime.now()
    inc_time=inc_time.strftime("%H:%M:%S")

    return render(request,"")

def incidentinfo(request):
    if request.method=='GET':
        vals=rl_db.child("incidents").get().val()
        image_name = list(vals.items())[0][1]['img_url']
        #image_name=image_name[7:]
        link=f"https://firebasestorage.googleapis.com/v0/b/kvh-proj.appspot.com/o/images%2F"+image_name+"?alt=media&token=46e51640-9a61-4080-9901-873eb60424e1"
        #print(image_name)
        context = {'incid':list(vals.items())[0][0],
            'imgurl':link}
        return render(request, 'incidentinfo.html',context)