import csv
from flask import request
from ldap3 import SUBTREE
from models.validation import *


def get_unique_cn(conn, base_cn):
    new_cn = base_cn
    index = 1
    while True:
        search_filter = f'(cn={new_cn})'
        result = conn.search('ou=users,o=pitg', search_filter, SUBTREE)
        if not result:
            return new_cn
        index += 1
        new_cn = f'{base_cn}{index}'



def user_input_to_dict():
    user = {}
    user['givenName'] = request.form.get('fname')#input('Enter given name: ')
    user['sn'] = request.form.get('sn')#input('Enter last name: ')
    user['ou'] = request.form.get('departmentNumber')
    user['title'] = request.form.get('designation')#input('Enter title: ')
    user['mail'] = request.form.get('mail')#input('Enter email: ')
    user['fullname'] = user['givenName'] + ' ' + user['sn']
    user['loginDisabled'] = "False"
    mobile_number = request.form.get('telephoneNumber')
    user['telephoneNumber'] = mobile_number
    user['L'] = request.form.get('location')
    user['employeeType'] = request.form.get('emptype')
    user['manager'] = request.form.get('manager')
    first_initial_fname = user['givenName'][0]
    first_five_characters_sn = user['sn'][:5]
    base_cn = first_initial_fname.lower() + first_five_characters_sn.lower()
    unique_cn = get_unique_cn(conn, base_cn)
    user['cn'] = unique_cn
    # print(user)
    return user, unique_cn

