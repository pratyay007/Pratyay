from ldap3 import Server, Connection, SUBTREE




def ldaploginauth(cn,pwd):
    LDAP_CONFIG = {
    'host': 'imanager.processit.site',
    'user': 'cn='+cn+',ou=users,o=pitg',
    'password': pwd,
    'search_base': 'ou=users,o=pitg',
    'search_filter': '(cn={})'.format(cn) 
}
    ldap_config = LDAP_CONFIG

    host = ldap_config['host']
    user = ldap_config['user']
    password = ldap_config['password']
    search_base = ldap_config['search_base']
    search_filter = ldap_config['search_filter']

    try:
        # Establish a connection to the LDAP server
        server = Server(host)
        c = Connection(server, user=user, password=password, auto_bind=True)

        #print(c)
        # Search for active users
        active_user_list = c.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE)

        # Perform paged search for attributes 'cn'
        entry_list = c.extend.standard.paged_search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=['cn','givenName','sn','mail','ou','title','employeeType', 'l', 'telephoneNumber'],
            generator=False
        )

        user_data = []


        # Iterate over the LDAP entries and extract the desired data
        for user in c.entries:
            dn_user = "cn=" + str(user['cn']) + ",ou=users,o=pitg"
            user_data.append(dn_user)
            user_data.append(str(user['cn']))
            user_data.append(str(user['givenName']))
            user_data.append(str(user['sn']))
            user_data.append(str(user['mail']))
            user_data.append(str(user['ou']))
            user_data.append(str(user['title']))
            user_data.append(str(user['employeeType']))
            user_data.append(str(user['l']))
            user_data.append(str(user['telephoneNumber']))
            
            #user_data.append({'dn_user': dn_user, 'cn': str(user['cn']),'givenName': str(user['givenName']),'sn': str(user['sn']),'mail': str(user['mail']),'department': str(user['ou']),'designation': str(user['title']),'employeeType': str(user['employeeType'])})
        # print(user_data)    

        return user_data  # Return the user_data list containing dn_user and cn

    except Exception as err:
        # Handle any exceptions or errors here
        #print("LDAP Error:", err)
        err_data = []
        err_data.append("error")
        err_data.append(err)
        
        return [err_data]
        
# Example usage:
if __name__ == '__main__':
    user_data = ldaploginauth('skarma', 'Process@1234')

    #print(user_data[0][0])
    if user_data[0][0]=='error':
        print(user_data[0][1])
    else:
        print("generate session data for user: " + user_data[1])
    # Print the user data
    # for user in user_data:
    #     print(user['dn_user'])
    #     print(user['cn'])
