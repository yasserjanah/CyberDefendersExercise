from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from dockerApp.tasks import create_container, remove_container
from dockerApp.models import Instance
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt
from dockerApp.func import get_from_db, add_to_db, update_status_db, delete_from_db, validate_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.middleware.csrf import CsrfViewMiddleware
from django.utils import timezone
import json
# Create your views here.

@login_required(login_url='/accounts/login')
def index(request):
    return render(request, "dockerApp/index.html")

def RegisterUser(request):
    if not request.user.is_authenticated: # check if user already logged in, if true if true he doesn't need to register
        if request.method == "POST":
                check = validate_form(request.POST)
                if check['valid']:
                    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                    return redirect('login')
                else:
                    return render(request, "dockerApp/register.html", {"errors": check["errors"]})
            
        else:
            return render(request, "dockerApp/register.html")
    else:
        return redirect("/") # redirect user who already login

def LoginUser(request):
    if request.user.is_authenticated: # check if user already logged in, if true he doesn't need to login again
        return redirect("/")
    if request.method == "POST":
        # this is a test envirement , we will not validate username and password
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "dockerApp/login.html", {"errors":["Username or Password Incorrect"]})
    else:
        return render(request, "dockerApp/login.html")

@login_required(login_url='/accounts/login')
def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/accounts/login')
def GetUserInfo(request):
    response_data = {"username":""}
    try:
        user = get_object_or_404(User, pk=request.user.id)
        response_data["username"] = user.username
    except Exception as err:
        print(err)

    return HttpResponse(json.dumps(response_data), content_type='application/json')

    
@login_required(login_url='/accounts/login')
@csrf_exempt
def LaunchContainer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name  = data.get('name')
            image = data.get('image')
            task = create_container.delay(name, image)
            add_to_db(user=request.user, task_id=task.task_id, name=name, image=str(image), status="PENDING")
            return HttpResponse(json.dumps({"task_id":task.task_id, "name":name, "image":image, "date": timezone.now(), "status":"PENDING"}, default=str), content_type='application/json')
        except Exception as err:
            raise (err)
            return HttpResponse("Internal Server Error")
    else:
        return HttpResponse('Method not allowed')

@login_required(login_url='/accounts/login')
@csrf_exempt
def GetTaskStatus(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            result = AsyncResult(task_id)
            update_status_db(user=request.user, task_id=task_id, status=result.state)
            response_data = {
                'status': result.state,
                'message': str(result.info)
            }
            if "Conflict" in str(result.info):
                response_data["message"] = "name already in use"
                response_data["error"] = True
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except Exception as err:
            raise err
            return HttpResponse("Internal Server Error (500) "+str(err))
    else:
        return HttpResponse('Method not allowed')

@login_required(login_url='/accounts/login')
@csrf_exempt
def GetAvailableImages(request):
    from dockerApp.tasks import init
    client = init()
    response_data = {"error":""}
    if client == False:
        response_data["error"] = "Docker is not running"
    else:
        images = [im.tags[0] for im in client.images.list()]
        response_data['images'] = images
    return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required(login_url='/accounts/login')
@csrf_exempt
def RemoveContainer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        # Avoid IDOR by filtering by user first
        if Instance.objects.filter(user=request.user).filter(name=name):
            task = remove_container.delay(name)
        delete_from_db(user=request.user, name=name)
        return HttpResponse(json.dumps({"deleted":True}), content_type='application/json')
    else:
        return HttpResponse('Method not allowed')

@login_required(login_url='/accounts/login')
@csrf_exempt
def GetUserInstances(request):
    try:
        userInstances = get_from_db(user=request.user)
    except Exception as err:
        print(err, "|||||||")
        userInstances = []
    return HttpResponse(json.dumps({"instances":userInstances}, default=str), content_type='application/json')
