DATA_DIR='/home/zdimon/Desktop/students/student-board/init_data'
ALL_FREE=True 
VIDEO_DIR = '/home/zdimon/Videos/course-data'
DOMAIN='http://localhost:8001'


import os
from .settings import BASE_DIR


'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

'''

''' 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pressa',                                   # Or path to database file if using sqlite3.
        'USER': 'root',                                   # Not used with sqlite3.
        'PASSWORD': '1q2w3e',                             # Not used with sqlite3.
        'HOST': 'localhost',                              # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                                         # Set to empty string for default. Not used with sqlite3.
    }
}
'''


LIQPAY_PUBLIC_KEY   = '...'
LIQPAY_PRIVATE_KEY  = '...'
LIQPAY_PROCESS_URL  = 'https://learning.webmonstr.com/liqpay/process'
EMAIL_BACKEND = ‘django.core.mail.backends.smtp.EmailBackend’
EMAIL_HOST = ‘smtp.gmail.com’
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ‘your_account@gmail.com’
EMAIL_HOST_PASSWORD = ‘your account’s password’