#!/usr/bin/env python
# -*- coding: UTF-8 -*-
DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'oldphoto.sqlite3'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

OLD_PHOTO_ROOT = ''

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

SITE_AVATAR = './media/avatar'
SITE_STYLE = './media/style'
SITE_IMAGES = './media/images'
AUTH_PROFILE_MODULE = 'userpanel.UserProfile'

DEFAULT_AVATAR_IMAGE = 'avatar.jpg'
AVATAR_URL_PREFIX = '/site_media/avatar/'
AVATAR_ROOT = MEDIA_ROOT + '/avatar/'

PHOTO_URL_PREFIX = '/site_media/photo/'
PHOTO_ROOT = MEDIA_ROOT + '/photo/'

MAX_PHOTO_SIZE = 500

LOGIN_URL = OLD_PHOTO_ROOT + '/userpanel/login/'
