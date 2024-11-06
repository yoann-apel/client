from client import worker

import os
import requests

from gpao.builder import Builder
from gpao.project import Project
from gpao.job import Job
import socket
import uuid
import stat

TAG = "docker"

def send_project(filename: str):
    headers = {
        'Content-type': 'application/json',
    }
    data = open(filename, 'rb')
    response = requests.put(worker.GPAO_API_URL+ "project", headers=headers, data=data)
    return response

def linux_content(url, id):
    return "curl -X 'POST' '" + url + "jobs/setTags?tags=docker' \\\n" + \
    """ -H 'accept: */*' \\
    -H 'Content-Type: application/json' \\
    -d '{ 
        "ids": [ 
    """ +  str(id) + "]\n" + \
    "}'"


def test_1_create_gpao():

    FILENAME = "test_project1.json"

    myuuid = str(uuid.uuid4())[:4]
    pause_name = f"PAUSE {myuuid}"


    # create jobs
    job1 = Job("job1", "echo simple job 1")
    job2 = Job(pause_name, "echo simple job 2",tags=["PAUSE"])

    job3 = Job("job3", "echo job3 should be done after job1 and job2", tags=[TAG])

    project1 = Project("project1_interactive", [job1, job2])
    project2 = Project("project2_interactive", [job3])
    project2.add_dependency(project1)
 
    builder = Builder([project1, project2])
    builder.save_as_json(FILENAME)
    assert os.path.isfile(FILENAME)

    response = send_project(FILENAME)
    assert response.status_code == 200

    req = worker.send_request(worker.GPAO_API_URL + "jobs",
                             "GET",
                             json={},
                             str_thread_id=0)
    if req and req.json:      
        pause_job_id = -1
        for row in req.json():
            # print(row)
            if row['job_name'] == pause_name:
                pause_job_id = row["job_id"]
        print("##################### " + str(pause_job_id))

        filename = "unpause.sh"
        with open(filename, "w") as shell_file:
            shell_file.write( linux_content(worker.GPAO_API_URL,pause_job_id))
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IEXEC)



def execute_gpao_client_multithreaded():

    parameters = {
        'url_api': worker.GPAO_API_URL,
        'hostname': socket.gethostname(),
        'tags': TAG,
        'autostart': '3',
        'mode_exec_and_quit': True,
        'suffix': ""
    }


    worker.exec_multiprocess(3, parameters)
