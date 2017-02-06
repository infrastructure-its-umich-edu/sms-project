"""
Django settings for sms project.

Generated by 'django-admin startproject' using Django 1.8.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: Path(BASE_DIR, ...)
import saml2
import ldap
import sys
from decouple import config
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from dj_database_url import parse as db_url
from unipath import Path

BASE_DIR = Path(__file__).parent

SAML2_URL_PATH = '/accounts/'
SAML2_URL_BASE = config('SAML2_URL_BASE', default='http://localhost:8000/accounts/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosaml2',
    'bootstrap3',
    'demo',
    'sendsms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sms.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=db_url
    )
}

AUTHENTICATION_BACKENDS = (
    'djangosaml2.backends.Saml2Backend',
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '%slogin/' % SAML2_URL_PATH
LOGIN_REDIRECT_URL = '/sms/send'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTH_LDAP_SERVER_URI = config('AUTH_LDAP_SERVER_URI', default='')
AUTH_LDAP_USER_DN_TEMPLATE = config('AUTH_LDAP_USER_DN_TEMPLATE', default='')
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(config('AUTH_LDAP_GROUP_BASE', default=''),
                                    ldap.SCOPE_SUBTREE,
                                    config('AUTH_LDAP_GROUP_FILTER',
                                           default='(objectClass=groupOfNames)')
                                    )
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
#AUTH_LDAP_REQUIRE_GROUP = config('AUTH_LDAP_REQUIRE_GROUP', default='')
AUTH_LDAP_FIND_GROUP_PERMS = config('AUTH_LDAP_FIND_GROUP_PERMS', default=True, cast=bool)
AUTH_LDAP_AUTHORIZE_ALL_USERS = config('AUTH_LDAP_AUTHORIZE_ALL_USERS', default=True, cast=bool)

ALLOW_GROUP = config('ALLOW_GROUP', default='allowed group')

SAML_CONFIG = {
    'xmlsec_binary': '/usr/bin/xmlsec1',
    'entityid': '%smetadata/' % SAML2_URL_BASE,
    # directory with attribute mapping
    #'attribute_map_dir': Path(BASE_DIR, 'attribute-maps'),
    'name': 'SMS Portal',
    # this block states what services we provide
    'service': {
        # we are just a lonely SP
        'sp': {
            'name': 'SMS Portal',
            'name_id_format': ('urn:oasis:names:tc:SAML:2.0:'
                               'nameid-format:transient'),
                         'authn_requests_signed': 'true',
                         'allow_unsolicited': True,
                         'endpoints': {# url and binding to the assetion consumer service view
                                       # do not change the binding or service name
                                       'assertion_consumer_service': [('%sacs/' % SAML2_URL_BASE,
                                                                       saml2.BINDING_HTTP_POST),
                                                                      ],
                                       # url and binding to the single logout service view+
                                       # do not change the binding or service name
                                       'single_logout_service': [('%sls/' % SAML2_URL_BASE,
                                                                  saml2.BINDING_HTTP_REDIRECT),
                                                                 ('%sls/post' % SAML2_URL_BASE,
                                                                  saml2.BINDING_HTTP_POST),
                                                                 ],
                                       },

                         # attributes that this project need to identify a user
                         'required_attributes': ['uid'],

                         # attributes that may be useful to have but not
                         # required
                         'optional_attributes': ['eduPersonAffiliation'],
                         },
                  },
    # where the remote metadata is stored
    'metadata': {'local': [Path(BASE_DIR, 'meta/remote-metadata.xml')], },
    # set to 1 to output debugging information
    'debug': 1,
    # certificate
    'key_file': Path(BASE_DIR, 'saml/key'),
    'cert_file': Path(BASE_DIR, 'saml/cert'),
}

SAML_CREATE_UNKNOWN_USER = True

SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username', ),
    'mail': ('email', ),
    'givenName': ('first_name', ),
    'sn': ('last_name', ),
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# value for SMS provider
SMS_USER = config('SMS_USER')
SMS_PASS = config('SMS_PASS')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
       'console': {
           'level': DEBUG,
           'class': 'logging.StreamHandler',
           'stream': sys.stdout,
       },
     },
     'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['console'],
            'level': config('DJANGO_AUTH_LDAP_LOG_LEVEL', default='DEBUG'),
            'propagate': True,
        },
        'sms': {
            'handlers': ['console'],
            'level': config('SMS_LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
     },
}
