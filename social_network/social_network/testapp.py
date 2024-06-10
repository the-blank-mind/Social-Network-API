import requests

BASE_URL = "http://127.0.0.1:8000/api"

def register_user():
    url = f"{BASE_URL}/register/"
    data = {
        "username": "amitpateldsdf",
        "email": "amitpatel12@example.com",
        "password": "password123",
        "first_name": "amitt",
        "last_name": "patell"
    }
    response = requests.post(url, json=data)
    print("Register Response:", response.json())
    

def login_user():
    url = f"{BASE_URL}/login/"
    data = {
        "email": "amitpatel12@example.com",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    print("Login Response:", response.json())
    return response.json().get("access")

def search_users(access_token):
    url = f"{BASE_URL}/search/?q=newuser"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    print("Search Users Response:", response.json())

def send_friend_request(access_token):
    url = f"{BASE_URL}/friend-request/send/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "receiver_id": 4
    }
    response = requests.post(url, json=data, headers=headers)
    print("Send Friend Request Response:", response.json())

def respond_friend_request(access_token, request_id, status):
    url = f"{BASE_URL}/friend-request/respond/{request_id}/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "status": status
    }
    response = requests.post(url, json=data, headers=headers)
    try:
        print("Respond Friend Request Response:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Respond Friend Request Response is not valid JSON. Raw response:")
        #print(response.text)
def list_friends(access_token):
    url = f"{BASE_URL}/friends/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    print("List Friends Response:", response.json())


def pending_requests(access_token):
    url = f"{BASE_URL}/friend-requests/pending/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    print("Pending Friend Requests Response:", response.json())

if __name__ == "__main__":
    #register_user()
    token = login_user()
    if token:    
        search_users(token)
        send_friend_request(token)
        respond_friend_request(token, request_id=4, status='accepted')  
        list_friends(token)
        pending_requests(token)
    
    
 
    
    
    
    
