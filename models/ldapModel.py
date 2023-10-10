from ldap3 import Server, Connection, SUBTREE

from services.service import get_unique_cn

class LDAPModel:
    def __init__(self):
        self.host = 'imanager.processit.site'
        self.user = 'cn=idmadmin,ou=sa,o=pitg'
        self.password = '3PITG#2023!'
        self.search_base = 'ou=users,o=pitg'
        self.search_filter = '(objectClass=inetOrgPerson)'
        
        
        
    def verifyLogin(self, cn, pw):
        server = Server(self.host)
        with Connection(server, user = self.user, password=self.password, auto_bind=True) as conn:
            entryList = conn.extend.standard.paged_search(search_base= self.search_base,
                                            search_filter= self.search_filter,
                                            search_scope= SUBTREE,
                                            attributes= ['cn', 'nspmDistributionPassword'],
                                            generator = False)
            for user in conn.entries:
                if cn == user['cn']:
                    if pw == user['nspmDistributionPassword']:
                        return True
        raise Exception('Unauthorized user')   
        

    def create_user(self, user):
        server = Server(self.host)
        with Connection(server, user=self.user, password=self.password, auto_bind=True) as conn:
            dn = 'cn=' + user['cn'] + ',' + 'ou=users,o=pitg'
            entry = {}
            entry['objectClass'] = ['person', 'inetOrgPerson', 'OrganizationalPerson', 'top']
            entry.update(user)
            unique_cn = get_unique_cn(conn, user['cn'])
            conn.add(dn, attributes=entry)

                                          
                                           
                                           