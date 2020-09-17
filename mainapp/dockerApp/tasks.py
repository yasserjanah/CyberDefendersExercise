from celery import shared_task
import docker, requests

def init():
    try:
        client = docker.from_env()
    except docker.errors.DockerException as err:
        return False
    
    return client

@shared_task(bind=True)
def create_container(self, xname, ximage):
    client = init()
    if client == False:
        self.update_state(state="FAILURE")
        return "Docker service is not running"
    try:
        client.containers.run(image=ximage, name=xname, detach=True, tty=True)
        return f"{xname} created"
    except requests.exceptions.ConnectionError:
        self.update_state(state="FAILURE")
        return "Connection aborted"

@shared_task(bind=True)
def remove_container(self, xname):
    client = init()
    if client == False:
        self.update_state(state="FAILURE")
        return "Docker service is not running"
    try:
        cn = client.containers.get(xname)
        cn.remove(force=True)
        return f"{xname} removed"
    except requests.exceptions.ConnectionError:
        self.update_state(state="FAILURE")
        return "Connection aborted"