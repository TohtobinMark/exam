from django.conf import settings
from django.contrib.auth.hashers import make_password
settings.configure()
password = "gynQMT"
hashed_password = make_password(password)
print(hashed_password)