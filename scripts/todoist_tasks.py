"""
Todoist is a ToDo List app and Task manager.

Advantages :
- Apps for all platforms
- One of the best todo widgets for Android I've used
- Gamifies task completion with Karma points
- IFTTT Integrations. Sync tasks with Google Calendar (events -> tasks)
- Easy-to-use API
- Dark Mode

API Requirements :
- API Key. Obtain here : https://todoist.com/prefs/integrations#
(stored as your_token below)
"""
import requests, uuid, json, datetime
import fire
import yaml
from pathlib import Path
import os

with open(os.path.join(Path(__file__).resolve().parents[1],'creds.yml')) as creds_file:
    creds = yaml.load(creds_file.read(),Loader=yaml.FullLoader)

your_token = creds['todoist']['token'] #https://todoist.com/prefs/integrations#
headers={"Authorization": "Bearer %s" % your_token}
URL = "https://beta.todoist.com/API/v8"

def getProjects():
    resp = requests.get(URL + "/projects",headers=headers)
    return resp.json()

def getProjectDetails():
    resp = requests.get(URL + "/projects/1234", headers=headers)
    return resp.json()

def getProjectTasks(projID):
    resp = requests.get(URL + "/tasks",params={"project_id": projID},headers=headers)
    return resp.json()

def addTask(title="Appointment with Maria",when="tomorrow at 12:00",priority=3):
    print (title+" --> "+when)
    task_json = {
        "content": title,
        "due_string": when,
        "due_lang": "en",
        "priority": priority
    }
    resp = requests.post(URL+"/tasks",data=json.dumps(task_json),
    headers={
        "Content-Type": "application/json",
        "X-Request-Id": str(uuid.uuid4()),
        "Authorization": "Bearer %s" % your_token
    })
    print (resp)

def getBatchTitle(i):
    interval = 6
    return "Read pages %d to %d" % (104+i*interval,104+(i+1)*interval)

def deleteTasks(taskIDs):
    for tid in taskIDs:
        print ("Deleted : ")
        requests.delete(URL+"/tasks/"+str(tid), headers=headers)

def addBatchTasks(n=30,hour=12,minute=00):
    """Use this to add a batch of tasks.
    Modify getBatchTitle to get the title for each interation.
    Alternatively modify the timedelta to change the interval between 2 tasks.

    For example :
    - Making sure you read a certain number of pages of a book everyday
    """
    init = datetime.datetime.now().replace(hour=hour,minute=minute)
    for i in range(n):
        task_time = init+datetime.timedelta(days=i)
        addTask(title=getBatchTitle(i),when=str(task_time))

def getFilteredTaskIDs(sub_string,proj_id):
    t = getProjectTasks(proj_id)
    return dict([(i['id'],i) for i in t if sub_string in i['content']])

if __name__ == "__main__":
    fire.Fire({"addTask":addTask})