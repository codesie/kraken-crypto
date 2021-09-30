# Project init
```
sij@codesie:/mnt/linuxData/01_Joel/02_Freizeit/Kryptowährungen/kraken-crypto/server$ python3 -m venv ven
sij@codesie:/mnt/linuxData/01_Joel/02_Freizeit/Kryptowährungen/kraken-crypto/server$ source venv/bin/activate
sij@codesie:/mnt/linuxData/01_Joel/02_Freizeit/Kryptowährungen/kraken-crypto/server$ pip install django djangorestframework django-cors-headers
```

# Project conf

```
django-admin startproject backend
python manage.py startapp api
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## settings.py
We need to extend the file `server/backend/settings.py` in the section `INSTALLED_APPS` with:
* api
* rest_framework

## Enabling CORS
[https://www.geeksforgeeks.org/how-to-enable-cors-headers-in-your-django-project/]()