from dockerApp.models import Instance
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.models import User

def get_from_db(user):
    userInstances = []
    if Instance.objects.filter(user=user).all() != []:
        for x in Instance.objects.filter(user=user):
            userInstances.append({"task_id":x.task_id, "name": x.name, "image":x.image, "date":x.date, "status":x.status})
    return userInstances

def add_to_db(user, task_id, name, image, status):
    Instance.objects.create(user=user, task_id=task_id, name=name, image=image, status=status)

def update_status_db(user, task_id, status):
    Instance.objects.filter(user=user).filter(task_id=task_id).update(status=status)

def delete_from_db(user, name): 
    # avoid IDOR vulnerabilty by filtering by User first
    _ = Instance.objects.filter(user=user).filter(name=name)
    _.delete()

def check_username(username):
    return (len(username) > 3) and (not User.objects.filter(username__iexact=username).exists())# this is a test envirement , so we check just for the length

def check_email(email):
    try:
        v = validate_email(email)
        return v
    except EmailNotValidError:
        return False

def check_password(pwd1, pwd2):
    return pwd1 == pwd2

def validate_form(data):
    response = {"valid": False}
    errors = []
    username = data.get('username')
    email    = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')
    is_username_valid = check_username(username)
    is_email_valid = check_email(email)
    is_password_valid = check_password(password1, password2)
    if not is_username_valid:
        errors.append("username is already exists")
    if not is_email_valid:
        errors.append("email is not valid")
    if not is_password_valid:
        errors.append("password doesn't match")
    if (is_username_valid and is_email_valid and is_password_valid):
        response["valid"] = True
    else:
        response["errors"] = errors
    return response