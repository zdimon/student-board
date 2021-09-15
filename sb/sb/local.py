DATA_DIR='/home/zdimon/Desktop/work/hntu-material'
ALL_FREE=True 
VIDEO_DIR = '/home/zdimon/Videos/course-data'
DOMAIN='http://localhost:8001'

import os
from .settings import BASE_DIR
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

