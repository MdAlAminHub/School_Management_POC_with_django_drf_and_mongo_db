"""
## School_Management_POC with Django, Django Rest Feamework and MongoDB

"""
The project is dockerized so there is two pre prerequisite requirments 

1.Docker
2.Docker Compose 

## To Run this Project with docker follow below:

"docker-compose up --build"

the project will run at 
http://localhost:7000/

## To Run this Project without docker follow below:
```
for windows:
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
```
for Linux:
python3 -m venv env
sudo apt source 
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### There is a File link to "http://localhost:7000/api/docs/?fbclid=IwAR1M1rLXyxHO_nSYN4kneDO6Kdf41fn0L7elpTosnRQENfd3kwY0rFzsQZ4#/" which has the swagger Collection of API's which are mainly all the API's for the project 



