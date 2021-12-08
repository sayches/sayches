import os
import uuid
from datetime import datetime


def uuid_profilepicture(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    now = datetime.now()
    return os.path.join(f'profilepicture/{now.year}/{now.month}/{now.day}/', filename)


def uuid_userid(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    now = datetime.now()
    return os.path.join(f'userid/{now.year}/{now.month}/{now.day}/', filename)


def uuid_highlight(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    now = datetime.now()
    return os.path.join(f'highlight/{now.year}/{now.month}/{now.day}/', filename)


def uuid_ad(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    now = datetime.now()
    return os.path.join(f'advertisement/{now.year}/{now.month}/{now.day}/', filename)


def uuid_media(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    now = datetime.now()
    return os.path.join(f'_media/{now.year}/{now.month}/{now.day}/', filename)


def uuid_newsroom(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    now = datetime.now()
    return os.path.join(f'newsroom/{now.year}/{now.month}/{now.day}/', filename)


def uuid_bitcoinaddress(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    now = datetime.now()
    return os.path.join(f'bitcoinaddress/{now.year}/{now.month}/{now.day}/', filename)
