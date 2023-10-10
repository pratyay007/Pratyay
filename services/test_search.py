from ldap3 import Server, Connection, SUBTREE


LDAP_CONFIG = {
    'host': 'imanager.processit.site',
    'user': 'cn=admin,ou=sa,o=system',
    'password': 't6D%pl37',
    'search_base': 'ou=users,o=pitg',
    'search_filter': '(objectClass=inetOrgPerson)'
}

def test_search():
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

        # Search for active users
        active_user_list = c.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE)

        # Perform paged search for attributes 'cn'
        entry_list = c.extend.standard.paged_search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=['cn', 'userPassword'],
            generator=False
        )

        user_data = []

        # Iterate over the LDAP entries and extract the desired data
        for user in c.entries:
            dn_user = "cn=" + str(user['cn']) + ",ou=users,o=pitg"
            user_pass = str(user['userPassword'])
            user_data.append({'pass': user_pass, 'cn': user['cn']})
        print(user_data)    

        return user_data  # Return the user_data list containing dn_user and cn

    except Exception as err:
        # Handle any exceptions or errors here
        print("LDAP Error:", err)
        return []

# Example usage:
if __name__ == '__main__':
    user_data = test_search()

    # Print the user data
    # for user in user_data:
    #     print(user['dn_user'])
    #     print(user['cn'])
