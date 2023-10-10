from os import environ, path, getcwd
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


load_dotenv(path.join(getcwd(), '.env'))

db = SQLAlchemy()
SECRET_KEY = environ.get('SECRET_KEY')


#Configutation of ldap
host = 'imanager.processit.site'
user = 'cn=idmadmin,ou=sa,o=pitg'
password = '3PITG#2023!'

#variable for search base
search_base = 'ou=users,o=pitg'

#variable for apply filter for active users
search_filter='(objectClass=inetOrgPerson)'

# Fields to Fetch from LDAP
ldap_fields = [
    'cn',
    'givenName',
    'sn',
    'mail',
    'fullName',
    'title',
    'createTimestamp',
    'lastLoginTime',
    'pwdChangedTime',
    'loginDisabled',
    'company',
    'co',
    'passwordExpirationTime',
    'workforceID',
    'lastLoginTime',
    'ObjectClass',
    'city',
    'costCenter',
    'createTimestamp',
    'mail',
    'nrfmemberof',
    'LoginTime',
    'manager',
]