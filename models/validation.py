from ldap3 import Server, Connection, SUBTREE

host = 'imanager.processit.site'
user = 'cn=idmadmin,ou=sa,o=pitg'
password = '3PITG#2023!'
search_base = 'ou=users,o=pitg'
server = Server(host)
conn = Connection(server, user=user, password=password, auto_bind=True)

def checkUniqueEmail(searchFilter: str):
    search_filter = f'(&(objectClass=inetOrgPerson)(mail={searchFilter}))'
    
    entryList = conn.extend.standard.paged_search(search_base=search_base,
                                                  search_filter=search_filter,
                                                  search_scope=SUBTREE,
                                                  attributes=['mail'],
                                                  generator=False)

    for user in entryList:
        mail = str(user['attributes']['mail'][0])
        if searchFilter == mail:
            return True  # Email already exists
    return False  # Email doesn't exist

def checkUniquePhone(phone_number):
    search_filter = f'(&(objectClass=inetOrgPerson)(telephoneNumber={phone_number}))'
    
    entryList = conn.extend.standard.paged_search(search_base=search_base,
                                                  search_filter=search_filter,
                                                  search_scope=SUBTREE,
                                                  attributes=['telephoneNumber'],
                                                  generator=False)

    for user in entryList:
        found_phone_number = str(user['attributes']['telephoneNumber'][0])
        if phone_number == found_phone_number:
            return True  # Phone number already exists
    return False  # Phone number doesn't exist


def search_active_user(searchFilter: str):
    search_filter = f'(&(objectClass=inetOrgPerson)(cn={searchFilter})(loginDisabled=FALSE))'
    
    ldap_data = []
    entryList = conn.extend.standard.paged_search(search_base=search_base,
                                                  search_filter=search_filter,
                                                  search_scope=SUBTREE,
                                                  attributes=['cn', 'loginDisabled', 'fullname', 'mail'],
                                                  generator=False)

    for user in entryList:
        cn = str(user['attributes']['cn'][0])
        if searchFilter == cn:
            ldap_data.append({
            'LoginID': str(user['attributes']['cn'][0]),
            'mail': str(user['attributes']['mail'][0]),
            'fullname': str(user['attributes']['fullname'][0])
            
            # Add more attributes as needed
        })

            #print(ldap_data)
            return ldap_data
    return [] 



if __name__ == '__main__':
    f = search_active_user('skarma')
    print(f)
    
