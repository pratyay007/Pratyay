# LDAP configuration
from ldap3 import Connection, Server, SUBTREE
import pandas as pd
from datetime import datetime
import pytz
from dateutil import tz
# import config


def istTime(dt_str):
    date_format = "%Y-%m-%d %H:%M:%S"
    dt_utc = datetime.strptime(dt_str, date_format)
    dt_utc = dt_utc.replace(tzinfo=pytz.UTC)
    local_zone = tz.tzlocal()
    dt_local = dt_utc.astimezone(local_zone)
    local_time_str = dt_local.strftime(date_format)
    return local_time_str


def fetch_data_from_ldap():
    host = 'imanager.processit.site'
    user = 'cn=idmadmin,ou=sa,o=pitg'
    password = '3PITG#2023!'

    #variable for search base
    search_base = 'ou=users,o=pitg'

    #variable for apply filter for active users
    search_filter='(objectClass=inetOrgPerson)'


    server = Server(host)
    c = Connection(server, user=user, password=password, auto_bind=True)

    ldap_data = []

    active_user_list = c.search(search_base=search_base,
                                search_filter=search_filter,
                                search_scope=SUBTREE,
                                attributes=[    'cn',
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
    'manager',] )

    for user in c.entries:
        passExpTime = str(user['passwordExpirationTime'])
        if len(passExpTime) <= 2:
            passExpTime = ''
        else:
            passExpTime = pd.to_datetime(passExpTime, utc=True)
            passExpTimeStr = (passExpTime.replace(tzinfo=None)).strftime("%Y-%m-%d %H:%M:%S")
            passExpTime = istTime(passExpTimeStr)

        createTimestamp = str(user['createTimestamp'])
        if len(createTimestamp) <= 2:
            createTimestamp = ''
        else:
            createTimestamp = pd.to_datetime(str(createTimestamp), utc=True)
            createTimestampStr = (createTimestamp.replace(tzinfo=None)).strftime("%Y-%m-%d %H:%M:%S")
            createTimestamp = istTime(createTimestampStr)

        pwdChangedTime = str(user['pwdChangedTime'])
        if len(pwdChangedTime) <= 2:
            pwdChangedTime = 'Never Changed'
        else:
            pwdChangedTime = pd.to_datetime(str(pwdChangedTime), utc=True)
            pwdChangedTimeStr = (pwdChangedTime.replace(tzinfo=None)).strftime("%Y-%m-%d %H:%M:%S")
            pwdChangedTime = istTime(pwdChangedTimeStr)

        LastLoginTime = str(user['LoginTime'])
        if LastLoginTime == "[]":
            LastLoginTime = 'Never Logged in'
        else:
            LastLoginTime = pd.to_datetime(str(LastLoginTime), utc=True)
            LastLoginTimeStr = (LastLoginTime.replace(tzinfo=None)).strftime("%Y-%m-%d %H:%M:%S")
            LastLoginTime = istTime(LastLoginTimeStr)

        CreateTime = str(user['createTimestamp'])
        if CreateTime == "[]":
            CreateTime = ''
        else:
            CreateTime = pd.to_datetime(str(CreateTime), utc=True)
            CreateTimeStr = (CreateTime.replace(tzinfo=None)).strftime("%Y-%m-%d %H:%M:%S")
            CreateTime = istTime(CreateTimeStr)

        disabled = str(user['LoginDisabled']).strip()

        userprincipalname = str(user['city'])
        if userprincipalname == "[]":
            upn = ''
        else:
            upn = userprincipalname

        Objclass = str(user['objectclass'])
        if Objclass == "[]":
            objectClass = ''
        else:
            objectClass = Objclass

        comp = str(user['company'])
        if comp == "[]":
            company = ''
        else:
            company = comp

        if disabled == "[]":
            loginDisabled = 'Active'
        else:
            if str(user['loginDisabled']) == "False":
                loginDisabled = "Active"
            else:
                loginDisabled = "Inactive"

        code = str(user['co'])
        if code == "[]":
            co = ''
        else:
            co = code

        fullname = str(user['fullName'])
        if fullname == "[]":
            displayname = ''
        else:
            displayname = fullname

        givenname = str(user['givenName'])
        if givenname == "[]":
            gname = ''
        else:
            gname = givenname

        surname = str(user['sn'])
        if surname == "[]":
            sname = ''
        else:
            sname = surname

        cn = str(user['CN'])
        if cn == "[]":
            cname = ''
        else:
            cname = cn

        mail = str(user['mail'])
        if mail == "[]":
            mailid = ''
        else:
            mailid = mail

        manager = str(user['manager'])
        cn_values = []

        if manager != "[]":
            manager_values = [entry.strip() for entry in manager.strip("[]").split(',') if entry.strip()]
            
            # Extract 'cn' values from the list of entries
            cn_values = [entry.split('=')[1] for entry in manager_values if entry.startswith('cn=')]
            
            # Join the 'cn' values into a single string
            manager = ', '.join(cn_values)
            # print(manager)
        else:
            manager = ''
        
        ldap_data.append({
            'LoginID': cname,
            'FirstName': gname,
            'LastName': sname,
            'UserStatus': loginDisabled,
            'PasswordExpiredTime': passExpTime,
            'LastLogonDate': LastLoginTime,
            'WhenCreated': CreateTime,
            'EmailID': mailid,
            'Manager': manager
            # Add more attributes as needed
        })

    c.unbind()
    print(ldap_data)
    return ldap_data


if __name__ == '__main__':
    ldap_data = fetch_data_from_ldap()