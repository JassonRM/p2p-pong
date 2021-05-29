import requests

def send_host_info(host_connection_info):
    data = host_connection_info.to_string()
    r = requests.post("localhost:8000/host",data= data)
    print(r.text)

def receive_host_lists():
    r = requests.get("localhost:8000/")
    if r.status_code == 200:
        return  r.text

def delete_host(host_connection_info):
    data = host_connection_info.to_string()
    r = requests.post("localhost:8000/remove", data=data)
    print(r.text)
