# Dancina

## How To Setup
```
git clone git@github.com:shahdhesham5/Dancina.git
```
```
cd Dancina
```
```
docker compose up --build
```

## To Create super user

```
docker exec -it django_dancina bash
```
```
python manage.py createsuperuser
```


## To Create Database 

```
docker exec -it django_dancina_db bash
```
```
psql -U postgres
```
```
createdb dancina_db 
```
