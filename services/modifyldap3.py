from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD
import config
from services.all_func import current_time

# function to deactivate employee
def modify_ldap_entry_deactivation(effected_user):
    # Define the server
    s = Server(config.host, get_info=ALL) 

    # define the connection
    c = Connection(s, user=config.user, password=config.password)
    c.bind()
    currentTime = current_time()
    accountDeactivationreason='Account has been deactivated on :'+currentTime
    # perform the Modify operation
    c.modify('cn='+effected_user+','+config.search_base,
         {'description': [(MODIFY_ADD, [accountDeactivationreason])],
          'loginDisabled': [(MODIFY_REPLACE, ['True'])]})
    print(c.result)

    # close the connection
    c.unbind()
   
   
# function to activate employee    
def modify_ldap_entry_activation(effected_user):
    # Define the server
    s = Server(config.host, get_info=ALL) 

    # define the connection
    c = Connection(s, user=config.user, password=config.password)
    c.bind()
    currentTime = current_time()
    accountActivationreason='Account has been activated on :'+currentTime
    # perform the Modify operation
    c.modify('cn='+effected_user+','+config.search_base,
         {'description': [(MODIFY_ADD, [accountActivationreason])],
          'loginDisabled': [(MODIFY_REPLACE, ['True'])]})
    print(c.result)

    # close the connection
    c.unbind()    

# function to provide employee access to resource
def modify_ldap_group(effected_user,grpname, reason):
    # Define the server
    s = Server(config.host, get_info=ALL)

    # define the connection
    c = Connection(s, user=config.user, password=config.password)
    c.bind()
    currentTime = current_time()
    dnUser= 'cn='+effected_user+','+config.search_base
    accountDeactivationreason='Account has been deactivated on :'+currentTime
    fetch_reason = reason
    print(fetch_reason)
    # perform the Modify operation
    c.modify(grpname,
         {'equivalentToMe': [(MODIFY_ADD, [dnUser])],
          'member': [(MODIFY_ADD, [dnUser])]})
    print(c.result)

    # close the connection
    c.unbind()
    


# Function to update employee address or phone number
def update_address_or_phone(effected_user, new_address=None, new_phone_number=None):
    # Define the server
    s = Server(config.host, get_info=ALL) 

    # Define the connection
    c = Connection(s, user=config.user, password=config.password)
    c.bind()
    
    # Create a dictionary to hold the modifications
    modifications = {}
    
    # Add new phone number if provided
    if new_phone_number:
        modifications['telephoneNumber'] = [(MODIFY_REPLACE, [new_phone_number])]
    
    # Add new address if provided
    if new_address:
        modifications['l'] = [(MODIFY_REPLACE, [new_address])]
    
    # Perform the Modify operation
    c.modify('cn=' + effected_user + ',' + config.search_base, modifications)
    print(c.result)

    # Close the connection
    c.unbind()   

    

if __name__ == 'main':
    m = modify_ldap_group('user1','cn=pam-imanager-server-access,ou=groups,o=pitg')