Description:

The Social Networking API is a Django Rest Framework-based backend solution for social networking applications. It offers user authentication, friend interactions, user search, and more, providing a seamless experience for users to connect and engage within the platform.

## Requirements

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- SQLite (default, but can be changed to any other database)

## Installation

   ## Prerequisites

         Before you begin, ensure you have met the following requirements:

         1. Python 3.8+
         2. pip package manager
   ## Installation Steps
          1. git clone <repository-url>
          2. cd <repository-directory>
          3. Install all the requirements from REQUIREMENTS.txt
         
## Configuration
   1. Database : Default database is used

## Migrate Database
   1. Migrate Database: python manage.py makemigrations & python manage.py migrate
## Create Superuser : python manage.py createsuperuser
## Running the server : python manage.py runserver

## API ENDPOINTS

## 1. User Authentication
   ## Signup:
       URL: /api/signup/
       Method: POST
       Payload: {"email": "email@example.com", "password": "password123"}
   ## Login:
       URL: /api/login/
       Method: POST
       Payload: {"email": "email@example.com", "password": "password123"}

## 2. User Search
   ## Search User:
      URL: /api/search/?q=<search_query>
      
      Method: GET

      Headers: Authorization: Bearer <token>


## 3. Friend Requests
   ## Send Friend Request:
      URL: /api/friend-request/send/
   
      Method: POST

      Headers: Authorization: Bearer <token>

      Payload: {"receiver_id": <receiver_user_id>}

   ## Respond to Friend Request:

      URL: /api/friend-request/respond/<request_id>/

      Method: POST

      Headers: Authorization: Bearer <token>

      Payload: {"status": "accepted"} or {"status": "rejected"}

## 4. Friends List
    ## List Friends:

      URL: /api/friends/

      Method: GET

      Headers: Authorization: Bearer <token>

   ## List Pending Friend Requests:

      URL: /api/friend-requests/pending/

      Method: GET

      Headers: Authorization: Bearer <token>

## 5.Testing

     You can use Postman or any other API client to test the endpoints.

## License
   This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
   Django   
   Django Rest Framework
## Contact
   For inquiries, issues, or contributions, please contact viplovesinghrathore@gmail.com.




