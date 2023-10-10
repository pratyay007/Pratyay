from flask import Flask, jsonify, render_template, redirect, session, request
from models.ldapModel import LDAPModel
from models.records import *
from models.validation import *
from services.service import *
from flask_mail import Mail
from services.search_user import ldap_search
from services.login_ldap import ldaploginauth
from services.fetch_total_users import fetch_data_from_ldap
from flask_session import Session
from services.helper import *
from config import db
from datetime import datetime
from config import *
from os import environ, path, getcwd
from sqlalchemy.orm import Session
from services.modifyldap3 import *
from services.all_func import *
from services.mail_config import *

load_dotenv(path.join(getcwd(), '.env')) #loading .env file

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY #getting the secret key from .env
    app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based session storage
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SESSION_PERMANENT'] = True #session will last as long as session lifetime defined
    app.config['PERMANENT_SESSION_LIFETIME'] = 1200  # 30 minutes in seconds
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI') # getting the database URI from .env
    app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER') # getting the mail server from .env
    app.config['MAIL_PORT'] = environ.get('MAIL_PORT') # getting the mail port from .env
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME') # getting the mail usernmame from .env
    app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD') # getting the mail password from .env
    Session(app) # creating an instance of session
    mail = Mail(app) # creating an instance of mail
    db.init_app(app)


    with app.app_context(): #creating an app context
        @app.route('/', methods=['GET', 'POST']) 
        def index():
            if 'username' in session: # if user has activate session
                return redirect('/dashboard')  # Redirect to the user page
            return render_template('login.html') # else render login.html


        @app.route('/authvalidate', methods=['GET', 'POST'])
        def authvalidate():
            error = None #setting the initial error value to none
            try:
                if request.method == 'POST': # if the request is post
                    
                    cn = request.form.get('username') # get user cn from form input
                    pwd = request.form.get('password') # get user password from form input
                    print(cn, pwd)
                    auth_login = ldaploginauth(cn, pwd) # calling the ldaploginauth function and passing the cn and password as an argument
                    
                    #return auth_login[0][0]
                    if auth_login[0][0]=='error':
                        #return str(auth_login[0][1])
                        # error_txt = "str(auth_login[0][1])"
                        error_txt = "Invalid username or password"
                        return render_template('login.html', error_txt=error_txt) 
                    else:
                        # Store user information in the session
                        session['username'] = auth_login[1] 
                        session['givenname'] = auth_login[2]
                        session['sn'] = auth_login[3]
                        session['mail'] = auth_login[4]
                        session['department'] = auth_login[5]
                        session['designation'] = auth_login[6] 
                        session['emptype'] = auth_login[7]
                        session['l'] = auth_login[8]
                        session['telephoneNumber'] = auth_login[9]
                        # You can also set other user-related data in the session if needed
                        # session['user_id'] = auth_login[2]  
                        return redirect('dashboard')
                        #return "generate session data for user: "+auth_login[1] 
            except Exception as err:
                error = str(err)   
                return redirect('/')


        @app.route('/create_user', methods=['GET', 'POST'])
        @login_required
        #@previledge_required
        def create_user():
            error = None
            success_message = None
            generated_cn = None
            dropdown_options = []

            try:
                # Call the ldap_search function
                user_data = ldap_search()
                # Generate dropdown options from LDAP user data
                for user in user_data:
                    dn_user = user['dn_user']
                    cn_user = user['cn']
                    dropdown_options.append((dn_user,cn_user))
                
                if request.method == 'POST':
                    ldap_model = LDAPModel()
                    user, generated_cn = user_input_to_dict()

                    # Server-side validation for first name and last name
                    if not user['givenName'].isalpha() or not user['sn'].isalpha():
                        error = 'First name and last name should contain only letters.'
                        return render_template('create_user.html', error=error, dropdown_options=dropdown_options)
                    # Server-side validation for mobile number
                    if len(user['telephoneNumber']) != 10 or not user['telephoneNumber'].isdigit():
                        error = 'Mobile number should contain exactly 10 digits.'
                        return render_template('create_user.html', error=error, dropdown_options=dropdown_options)
                    
                    # Check if the phone number already exists in LDAP
                    
                    if checkUniqueEmail(user['mail']):    
                        error = 'Email address already exists. Please choose a different email address.'    
                        return render_template('create_user.html', error=error, dropdown_options=dropdown_options)
                    

                    # Check if the email address (mail field) already exists in LDAP
                    if not checkUniquePhone(user['telephoneNumber']):
                        ldap_model.create_user(user)
                        # creation_time = datetime.utcnow()
                        # created_by = (user['givenName'])

                    # Save the record to PostgreSQL using SQLAlchemy
                    # try:
                    #     user_creation = UserCreation(created_by=created_by)
                    #     print(user_creation)
                    #     db.session.add(user_creation)
                    #     db.session.commit()

                    # except Exception as e:
                    #     error = 'Error saving the record to PostgreSQL: {}'.format(str(e))
                    #     user['creation_time'] = creation_time
                    #     user['created_by'] = created_by
                        
                        
                        # Redirect to the success page after successful user creation
                        return render_template('success.html', generated_cn=generated_cn)
                    else:
                        error = 'Phone number already exists. Please choose a different phone number.'

            except Exception as err:
                error = 'Ldap server is not responding'
                error_log = f'An error has occurred: {str(err)}'
                print(error_log)
            # print(dropdown_options)
            
            checkPrivilege=previledge_required()
            if checkPrivilege==True:
                return render_template('create_user.html', success_message=success_message, generated_cn=generated_cn, error=error, dropdown_options=dropdown_options)
            else:
                return render_template('permissionDenied.html')
            
            

        @app.route('/dashboard', methods=['GET', 'POST'])
        @login_required
        def dashboard():
            if 'username' in session:
                username = session['username']
            else:
                return redirect('/')    
            return render_template('dashboard.html')


        @app.route('/view_total_users')
        @login_required
        def get_ldap_data():
            try:
                users = fetch_data_from_ldap()
                # print(users)
                checkPrivilege=previledge_required()
                hr_associate_privilege= hr_associate_previledge_required()
                if checkPrivilege==True:
                    return render_template('view_total_users.html', users=users)
                elif hr_associate_privilege==True:
                    return render_template('view_total_users.html', users=users)
                else:
                    return render_template('permissionDenied.html')
            except:
                return render_template('500_error.html')
             

        @app.route('/send_mail', methods=['POST'])
        def send_mail():
            # Parse JSON data from the request
            data = request.get_json()
            fname = data.get('fname')
            loginid = data.get('loginid')
            pwd = data.get('pwd')
            recipient_email = data.get('mail')
            image_url = 'https://processitglobal.com/wp-content/themes/pitg-child/assets-pitg/images/logo.png'


            # Create the email message with HTML formatting
            message_body = f"<p><img src='{image_url}' alt='Company Logo' width='100' height='75'></p>"
            message_body += f"<p>Hello {fname},</p>"
            message_body += f"<h3><strong>Welcome to ProcessIT Global Pvt Ltd.</strong></h3>"
            message_body += f"<p>We are happy to inform you that your account has been successfully onboarded.</p>"
            message_body += f"<p><strong>Please find the below information for login and access purposes:</strong></p>"
            message_body += f"Login ID : {loginid}<br>"
            message_body += f"Password : <span style='color:white;'>{pwd}</span>"
            message_body += f"<p>Access URL : <a href='https://sso.processit.site/nidp'>https://sso.processit.site/nidp</a></p>"
            message_body += f"<p><strong>Please ensure that following details are listed in your host file:</strong></p>"
            message_body += f"192.168.1.7  &nbsp;&nbsp;&nbsp;&nbsp; sso.processit.site<br>"
            message_body += f"192.168.1.7  &nbsp;&nbsp;&nbsp;&nbsp; uasso.processit.site<br>"
            message_body += f"192.168.1.7  &nbsp;&nbsp;&nbsp;&nbsp; pamsso.processit.site<br>"
            message_body += f"192.168.1.7  &nbsp;&nbsp;&nbsp;&nbsp; hrreporting.processit.site<br>"
            message_body += f"192.168.1.7  &nbsp;&nbsp;&nbsp;&nbsp; reporting.processit.site<br>"
            message_body += f"<p><strong>Thanks & Regards,</strong></p>"
            message_body += f"<p><strong>PITG Identity & Access Management Team.</strong></p>"
            message_body += f"<p>Note: In case of any support please call +91-9432881844 or raise request in user application portal.</p>"
            
            message = Message(subject="Your account has been onboarded into PITG environment",
                            sender=app.config["MAIL_USERNAME"],
                            recipients=[recipient_email],
                            html=message_body)

            # Send the email
            try:
                mail.send(message)
                return jsonify({"message": "Email sent successfully"}), 200
            except Exception as e:
                return jsonify({"message": f"Email could not be sent: {str(e)}"}), 500


        @app.route('/permissionDenied', methods=['GET', 'POST'])
        def permissionDenied():   
            return render_template('permissionDenied.html')
        
        @app.route('/deactivate_employee', methods=['GET', 'POST'])
        @login_required
        def deactivate_employee():      
            checkPrivilege=previledge_required()
            if checkPrivilege==True:                 
                return render_template('deactivate_employee.html')
            else:
                return render_template('permissionDenied.html')   
        
        @app.route('/activate_employee', methods=['GET', 'POST'])
        @login_required
        def activate_employee():      
            checkPrivilege=previledge_required()
            if checkPrivilege==True:                 
                return render_template('activate_employee.html')
            else:
                return render_template('permissionDenied.html')                


        #route for deactivation of employee
        @app.route('/disable_employee', methods=['GET', 'POST'])
        @login_required
        def disable_employee():
            error_message = None
            users = []


            if request.method == 'POST':
                search_filter = request.form.get('searchFilter')
                users = search_active_user(search_filter)
 
                if not users:
                    error_message = 'Employee Not Found!'
            
                if 'deactivate' in request.form:
                    approver_name = 'NA'
                    get_management = getManagementUser()
                    reason_for_deactivation = request.form.get('reason_for_deactivation')
                    requested_id=request.form.get('requested_id')


                    new_task = TrnApprovalTask(
                        tat_task_type='deactivation',
                        tat_task_state='pending',
                        tat_requested_id=requested_id,
                        tat_request_by=session.get('username'),
                        tat_approver=get_management,
                        tat_reason=reason_for_deactivation,
                        tat_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )

                    db.session.add(new_task)
                    db.session.commit()
                    
                    print('saved to the db')
                    deactivate_mail = deactivation_mail('pending',str(requested_id), str(session.get('username')), str(get_management))
                    # deactivate_mail = deactivation_mail('pending','skarma', 'Souvik', 'skarma')

                    return redirect('/view_all_requests')

            return render_template('deactivate_employee.html', users=users, error_message=error_message)


        @app.route('/approve', methods=['POST'])
        @login_required
        def approve():
            if request.method == "POST":
                data = request.get_json()
                tat_id = data.get('tatId')
                tat_effected_id=data.get('tat_effected_id')
                tat_resource_group=data.get('tat_resource_group')
                tat_task_type=data.get('tat_task_type')
                tat_reason= data.get('tat_reason')
                print(tat_reason)


                # Create a session and use Session.get() to retrieve the task
                session = db.session
                task = session.get(TrnApprovalTask, tat_id)

                if task:
                    # Check if the task is currently "pending"
                    if task.tat_task_state == 'pending':
                        # Update the task status to "approved"
                        task.tat_task_state = 'approved'
                        session.commit()
                        print("From route:::::::::"+tat_effected_id)
                        if tat_task_type=='deactivation':
                            isdiactivated=modify_ldap_entry_deactivation(str(tat_effected_id))
                            print(isdiactivated)
                        elif tat_task_type=='access_to_resource':
                            modifyLdapGroup = modify_ldap_group(str(tat_effected_id),str(tat_resource_group),str(tat_reason))   
                            print(modifyLdapGroup)
                        # elif tat_task_type=='activation':
                        #     isactivated = modify_ldap_entry_activation(str(tat_effected_id))   
                        #     print(modifyLdapGroup)    
                        
                        return jsonify(success=True)
                    else:
                        return jsonify(success=False, message='Task is already ' + task.tat_task_state)
                else:
                    return jsonify(success=False, message='Task not found.')

            return jsonify(success=False, message='Invalid request.')

        @app.route('/reject', methods=['POST'])
        @login_required
        def reject():
            if request.method == "POST":
                data = request.get_json()
                tat_id = data.get('tatId')
                tat_task_state = data.get('tat_task_state')

                # Check if the tat_id exists in the database
                session = db.session
                task = session.get(TrnApprovalTask, tat_id)
                if task:
                    # Check if the task is currently "pending"
                    if task.tat_task_state == 'pending':
                        # Update the task status to "rejected"
                        task.tat_task_state = 'rejected'
                        db.session.commit()
                        # reject_mail = atr_mail(tat_task_state, session['givenname'], session['username'], session['mail'])
                        # print(reject_mail)
                        return jsonify(success=True)
                    else:
                        return jsonify(success=False, message='Task is already ' + task.tat_task_state)
                else:
                    return jsonify(success=False, message='Task not found.')

            return jsonify(success=False, message='Invalid request.')


        @app.route('/access_to_resource', methods=['GET', 'POST'])
        @login_required
        def access_to_resource():
            users = []
            if request.method == 'POST':

                if 'access' in request.form:
                    reason_for_access = request.form.get('reason_for_access')
                    resource_group = request.form.get('resource_name')
                    requested_id=request.form.get('requested_id')
                    print(f"This is the session user: {session['username']}")
                    get_manager = getManagerCN(session['username'])
                    print(f"This is the manager: {get_manager}")
    
                    new_task = TrnApprovalTask(
                        tat_task_type='access_to_resource',
                        tat_task_state='pending',
                        tat_requested_id=session.get('username'),
                        tat_request_by=session.get('username'),
                        tat_approver=get_manager,
                        tat_reason=reason_for_access,
                        tat_resource_group= resource_group,
                        tat_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )

                    db.session.add(new_task)
                    db.session.commit()
                    print('saved to the db')
                    access_mail = atr_mail('pending', str(session.get('username')),  str(get_manager))

                    return redirect('/view_all_requests')

            return render_template('access_to_resource.html', users=users)

        @app.route('/deactivate_ac', methods=['GET', 'POST'])
        @login_required
        def deactivate_ac():
            return render_template('deactivate_ac.html')
        
        @app.route('/test', methods=['GET', 'POST'])
        # @login_required
        def test():
            # user_data = getManagerCN('rrosha')
            
            # maill = atr_mail('rejected','souvik', 'skarma', 'souvik.karmakar@processitglobal.com')
            # mailll = getemailbycn('skarma')
            deactivate_mail = deactivation_mail('pending','skarma', 'Souvik', 'skarma')

            # return (deactivate_mail)
            return (deactivate_mail)
        
        @app.route('/test2', methods=['GET', 'POST'])
        def test2():
            sendtoEmail = getemailbycn('skarma')
            print(sendtoEmail) 
            return (sendtoEmail)

        
        @app.route('/view_all_requests', methods=['GET', 'POST'])
        @login_required
        def view_all_requests():
            users = TrnApprovalTask.query.all()
            # print(users)
            return render_template('view_all_requests.html', users=users)
        
        @app.route('/update_info', methods=['GET', 'POST'])
        @login_required
        def update_info():
            if request.method == 'POST':
                new_address = request.form.get('new_address')
                new_phone_number = request.form.get('new_phone_number')
                
                # Call the update function with the new address and phone number
                result = update_address_or_phone(session['l'], new_address, new_phone_number)
                
                if result:
                    # Update successful
                    print('Information updated successfully', 'success')
                else:
                    # Update failed or user not found
                    print('Failed to update information', 'danger')
                    
                # Redirect to the dashboard page after the form is submitted
                return redirect(url_for('dashboard'))    

            # Retrieve the current address and phone number
            address = session['l']
            phone_number = session['telephoneNumber']
            
            return render_template('update_info.html', address=address, phone_number=phone_number)


        @app.route('/success', methods=['GET', 'POST'])
        @login_required
        def success():
            return render_template('success.html')
        

        @app.route('/logout')
        def logout():
            # Clear the session data
            session.clear()
            print(session)
            # Redirect the user to the specified URL
            return redirect('https://sso.processit.site/AGLogout')
        
        # db.drop_all()
        db.create_all()
        db.session.commit()
        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port='8001')
