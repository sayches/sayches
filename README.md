<div align="center">
        <img src="https://user-images.githubusercontent.com/61336552/145426931-9b431526-e7db-4fe7-ac97-b2d9e117c056.png" alt="drawing" width="400px"/>
</div>

# Sayches 🐠

Sayches is an anonymous social media platform that champions the free flow of information by taking anti-surveillance measures and resisting censorship.

## 📺 Screenshots

| Feed | Profile | DMs |
| --- | --- | --- |
| ![Screenshot](/.github/media/Feed.png) | ![Screenshot](/.github/media/Profile.png) | ![Screenshot](/.github/media/DMs.png) |

## 🚀 Key Features
Anonymous Pub 👻 Direct Messages 💬 Feed 📰 Flair 🏷️ Hashtag #️⃣ Mention 🤏 Pin 📌 Ping 👋 Pop ✍️ Profile 🆔 QR 📱 Reactions ❤️ Trends 📈 Warrant Canary 🛡️ Watch 👁️

## 👪 Contributing
* Test the app with different devices
* Report issues in the [issue tracker](https://github.com/Sayches/Sayches/issues)
* Create a [Pull Request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)

## 🔗 Requirements

* Backend: [Python 3](https://www.python.org/download/releases/3.0/)
* Backend Framework: [Django](https://docs.djangoproject.com/)
* Frontend: [HTML](https://github.com/Sayches/Sayches/search?l=html), [JavaScript](https://github.com/Sayches/Sayches/search?l=javascript) & [CSS](https://github.com/Sayches/Sayches/search?l=css)
* Web Template Engine: [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
* UI Framework: [Bootstrap](https://getbootstrap.com/)
* Database: [PostgreSQL](https://www.postgresql.org/docs/)
* Web Server: [Gunicorn](https://gunicorn.org/)
* Web APIs: [Django REST Framework](https://www.django-rest-framework.org/)
* Container: [Docker](https://docs.docker.com/)
* HTTP Client: [Ajax](https://www.w3schools.com/whatis/whatis_ajax.asp), [Fetch](https://javascript.info/fetch)
* Visual Style: [Neumorphic](https://uxdesign.cc/neumorphism-in-user-interfaces-b47cef3bf3a6)
* Icon Set: [Remix Icon](https://remixicon.com/)

## 📍 Thid-Party APIs

| Email Delivery Service | Storage Service | Relational Database Service | Challenge Response | Bitcoin Exchange Rate & Wallet
| --- | --- | --- | --- | --- |
| [Amazon SES](https://aws.amazon.com/ses/) | [Amazon S3](https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-s3.html) | [Amazon RDS](https://aws.amazon.com/rds/) | [hCaptcha](https://python.plainenglish.io/how-to-add-hcaptcha-to-your-django-crispy-form-and-be-more-privacy-conscious-273e7f39bbfd) | [Coinbase](https://developers.coinbase.com/api/v2?python#get-exchange-rates)

## 🐳 Docker Images

| Production ``production.yml`` | Local ``local.yml`` |
| --- | --- |
| Django, Redis, Celery Worker, Celery Beat, Flower  | Django, Redis, Celery Worker, Celery Beat, Flower, Postgres |


## 💻 Deployment

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) on the server & clone the project from GitHub.

2. Build the project:
```
make build
```

3. Deploy the project:
```
make up
```

4. Create SuperAdmin account:
```
docker-compose -f local.yml run django python manage.py createsuperuser
```
        
5. Creat new migrations based on the changes you have made to your models:
```
docker-compose -f local.yml run django python manage.py makemigrations
```
6. Synchronises the database state with the current set of models and migrations:
```
docker-compose -f local.yml run django python manage.py migrate
```
7. Collects the static files:
```
sudo docker-compose -f local.yml run django python manage.py collectstatic
```

## 📓 License
Sayches is free, open-source software licensed under AGPLv3.
