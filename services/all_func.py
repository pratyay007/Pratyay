from datetime import datetime
from ldap3 import Server, Connection, SUBTREE
import config


def current_time():
    # ct stores current time
    ct = datetime.now()
    print("current time:-", str(ct))

    return str(ct)

#approver for access to resources by manager approval
def getManagerCN(search_by_user):

    host = config.host
    user = config.user
    password = config.password
    search_base = config.search_base
    search_filter = '(cn='+search_by_user+')'

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
            attributes=['cn', 'manager'],
            generator=False
        )

        user_data = []


        # Iterate over the LDAP entries and extract the desired data
        for user in c.entries:
            dn_user = "cn=" + str(user['cn']) + ",ou=users,o=pitg"
            user_manager = str(user['manager'])
            # user_mail = str(user['mail'])
            user_data.append({'user_manager': user_manager, 'cn': str(user['cn'])})
            print(user_data)
            user_manager_cn=user_manager.split(',')
            user_manager_cn[0].split('=')
        # print(user_manager_cn[0].split('=')[1])    

        return (user_manager_cn[0].split('=')[1])   # Return the user_data list containing dn_user and cn

    except Exception as err:
        # Handle any exceptions or errors here
        print("LDAP Error:", err)
        return str(err)
    
# manager = getManagerCN('skarma')

def getemailbycn(search_by_user):

    host = config.host
    user = config.user
    password = config.password
    search_base = config.search_base
    search_filter = '(cn='+search_by_user+')'

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
            attributes=['cn', 'mail'],
            generator=False
        )

        

        # Iterate over the LDAP entries and extract the desired data
        for user in c.entries:
            dn_user = "cn=" + str(user['cn']) + ",ou=users,o=pitg"
            # user_mail = str(user['mail'])
        # print(str(user['mail']))
        return (str(user['mail']))  # Return the user_data list containing dn_user and cn

    except Exception as err:
        # Handle any exceptions or errors here
        print("LDAP Error:", err)
        return str(err)
    
# manager = getManagerCN('skarma')

#get approval from CTO for deactivation or deletion of employee
def getManagementUser():
    # ldap_config = LDAP_CONFIG

    host = config.host
    user = config.user
    password = config.password
    search_base = config.search_base
    search_filter = '(title=CTO)'

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
            attributes=['cn', 'loginDisabled'],
            generator=False
        )

        # Iterate over the LDAP entries and extract the desired data
        for user in c.entries:
            print(str(user['cn']))    

        return str(user['cn'])  # Return the user_data list containing dn_user and cn

    except Exception as err:
        # Handle any exceptions or errors here
        print("LDAP Error:", err)
        return str(err)
    
    



# Example usage:
# if __name__ == '__main__':
    # user_data = search_by_user('skarma')

    # Print the user data
    # for user in user_data:
    #     print(user['dn_user'])
    #     print(user['cn'])

