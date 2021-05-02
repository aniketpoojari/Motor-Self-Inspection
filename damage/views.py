from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.files.storage import FileSystemStorage
import os, json
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Claims
from django.db.models import Count

def index(request):
    claim_no = ""
    emailID = request.user
    print(request.user.is_superuser)
    if(str(emailID) == "AnonymousUser" ):   
        return HttpResponseRedirect(reverse('login'))
    name = User.objects.get(username = emailID)
    name = name.first_name + " " + name.last_name
    if request.method == 'POST':
        c = Claims.objects.count() + 1
        front = request.FILES['front'] 
        left = request.FILES['left']
        back = request.FILES['back']
        right = request.FILES['right']
        fs = FileSystemStorage(location = "static/IMAGES")
        frontn = fs.save("front" + str(c) + ".jpg", front)
        leftn = fs.save("left" + str(c) + ".jpg", left)
        backn = fs.save("back" + str(c) + ".jpg", back)
        rightn = fs.save("right" + str(c) + ".jpg", right)
        claim = Claims(userid = str(emailID), claimno = c, status = 0, description = "Images are being processed")
        claim.save()
        claim_no = str(c)
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('claims'))
    else:
        return render(request, 'damage/index.html', {'claimno': claim_no, 'name': name})

def detection(request, claim):
    if(str(request.user) == "AnonymousUser"):   
        return HttpResponseRedirect(reverse('login'))
    os.system(os.getcwd() + "/damage/DETECTION/new.py " + str(claim))
    return HttpResponse() 
        
def result(request):
    emailID = request.user
    if(str(emailID) == "AnonymousUser"):   
        return HttpResponseRedirect(reverse('login'))
    name = User.objects.get(username = emailID)
    name = name.first_name + " " + name.last_name
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('claims'))
    c = Claims.objects.filter(userid = request.user).order_by('-date')[0].claimno    
    images = [
        "OUTPUTS/output_front" + str(c) + ".jpg",
        "OUTPUTS/output_left" + str(c) + ".jpg",
        "OUTPUTS/output_back" + str(c) + ".jpg",
        "OUTPUTS/output_right" + str(c) + ".jpg"
    ]
    return render(request, 'damage/result.html', {'claim': c, 'images': images, 'name': name})

def check_file(request, claim):
    # if(str(request.user) == "AnonymousUser"):   
        # return HttpResponseRedirect(reverse('login'))
    if(os.path.exists(os.getcwd()+"/static/OUTPUTS/output_right"+str(claim)+".jpg")):
        claimdetails = Claims.objects.get(claimno = claim)
        claimdetails.description = "Not seen yet";
        claimdetails.save()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return HttpResponse(json.dumps(response), content_type="application/json")

def user_login(request):
    status = ""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username = email, password = password)
        if user:
            if request.path == "/adminlogin/":
                if user.is_superuser == True:
                    login(request, user)
                    return HttpResponseRedirect(reverse('claims'))
                else:
                    status = "PROVIDE VALID ADMIN CREDENTIALS"
                    return render(request, 'damage/adminlogin.html', {'status': status})
            else:
                if user.is_superuser == False:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    status = "PROVIDE VALID CUSTOMER CREDENTIALS"
                    return render(request, 'damage/login.html', {'status': status})
        else:
            status = "PROVIDE VALID CREDENTIALS"
            if request.path == "/adminlogin/":
                return render(request, 'damage/adminlogin.html', {'status': status})
            else:
                return render(request, 'damage/login.html', {'status': status})
    else:
        if(str(request.user) == "AnonymousUser"):
            string = str(request.get_full_path());
            if string == "/login/":
                return render(request, 'damage/login.html', {'status': status})
            else:
                return render(request, 'damage/adminlogin.html', {'status': status})
                 
        else:
            return HttpResponseRedirect(reverse('index'))

def user_logout(request):
    status = ""
    if request.method == "POST":
        status = request.user.is_superuser;
        logout(request)
        if status:
            return HttpResponseRedirect('/adminlogin/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponse("GO BACK AND PRESS THE LOGOUT BUTTON")

def claims(request):
    emailID = request.user
    if(str(emailID) == "AnonymousUser"):   
        return HttpResponseRedirect(reverse('login'))
    name = User.objects.get(username = emailID)
    name = name.first_name + " " + name.last_name
    if(request.user.is_superuser):
        d = {}
        users = list(User.objects.all().exclude(is_superuser=True))
        for user in users:
            user = str(user)
            d[user] = [0, 0, 0 ,0]
        claims = list(Claims.objects.values('userid').annotate(Count('status')))
        claims0 = list(Claims.objects.filter(status=0).values('userid').annotate(Count('status')))
        claims1 = list(Claims.objects.filter(status=1).values('userid').annotate(Count('status')))
        claims2 = list(Claims.objects.filter(status=2).values('userid').annotate(Count('status')))
        for claim in claims:
            d[claim['userid']][0] = claim['status__count']
        for claim in claims0:
            d[claim['userid']][1] += claim['status__count']
        for claim in claims1:
            d[claim['userid']][2] += claim['status__count']
        for claim in claims2:
            d[claim['userid']][3] += claim['status__count'] 
        return render(request, 'damage/allclients.html', {'d': d, 'name': name})        
    else:
        status = ""
        claims = Claims.objects.filter(userid = emailID)
        count = claims.count()
        if count == 0:
            status = "NO CLAIMS YET"
        return render(request, 'damage/individuals_claims.html', {'stat': status,'claims': claims, 'name': name})        

def individuals_claims_from_superuser(request, individual):
    stat = ""
    emailID = request.user
    if(str(emailID) == "AnonymousUser" or emailID.is_superuser == False):   
        return HttpResponseRedirect(reverse('login'))
    name = User.objects.get(username = emailID)
    name = name.first_name + " " + name.last_name
    claims = Claims.objects.filter(userid = individual)
    count = claims.count()
    if count == 0:
            stat = "NO CLAIMS YET FROM " + individual
    return render(request, 'damage/individuals_claims.html', {'stat': stat,'claims': claims, 'name': name, 'individual': individual})

def individualclaim(request, claim):
    if request.method == "POST":
        claimdetails = Claims.objects.get(claimno = claim)
        claimdetails.status = int(request.POST['status'])
        claimdetails.description = request.POST['description']
        claimdetails.save()
        return HttpResponseRedirect(reverse('individualclaim', kwargs={'claim': claim}))
    else:
        emailID = request.user
        if(str(emailID) == "AnonymousUser"):   
            return HttpResponseRedirect(reverse('login'))
        name = User.objects.get(username = emailID)
        name = name.first_name + " " + name.last_name
        claimdetails = Claims.objects.get(claimno = claim)
        if( ( emailID.is_superuser ) or ( emailID.is_superuser == False and str(emailID) == str(claimdetails.userid) ) ):
            images = [
                "OUTPUTS/output_front" + str(claim) + ".jpg",
                "OUTPUTS/output_left" + str(claim) + ".jpg",
                "OUTPUTS/output_back" + str(claim) + ".jpg",
                "OUTPUTS/output_right" + str(claim) + ".jpg"
            ]
            return render(request, 'damage/individualclaim.html', {'claimdetails': claimdetails, 'name': name, 'images': images})
        else:
            return HttpResponseRedirect(reverse('claims'))

def download(request, claim):
    path = os.getcwd() + "/static/JSON/data_" + str(claim) + ".txt"
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404