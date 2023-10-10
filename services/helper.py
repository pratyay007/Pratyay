from flask import session, redirect, url_for
from functools import wraps

# Add a decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index'))
      
        return f(*args, **kwargs)
    return decorated_function


def previledge_required():

        if 'username' in session:
            department = session['department']
            designation=session['designation']
            if (department=='HR' and designation=='Manager-HRM & Excellence') or (department=='Management'):
                
                return True
            else:
                return False
            
def hr_associate_previledge_required():
        if 'username' in session:
            department = session['department']
            designation=session['designation']
            if (department=='HR' and designation=='HR Associate'):
                
                return True
            else:
                return False            
      



