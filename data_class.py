from tempfile import NamedTemporaryFile
from utils.templates import get_template_path,get_template,render_context
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import smtplib
import csv
import os
import shutil



class UserManager:
    def __init__(self):
        self.host = "smtp.gmail.com"
        self.port = 587
        self.username = "hungrypy99@gmail.com"
        self.password = "8302D10C0C"
        self.to_list = []
        self.file_ = os.path.join(os.path.dirname(__file__),"document/data.csv") 
        self.fieldnames = ["id","first","last","email","amount","sent","date"]

    #Deleting user
    def delete_user(self,user_id = None,user_email = None):
        user = self.get_user_data(user_id = user_id,user_email=user_email)
        if user:
            tempfile = NamedTemporaryFile(delete = True)
            try:
                with open(self.file_,"rb") as csvfile ,tempfile:
                    reader = csv.DictReader(csvfile)
                    writer = csv.DictWriter(tempfile,self.fieldnames)
                    writer.writeheader()
                    for row in reader:
                        if user_id is not None and user_email is None :
                            if int(user_id) != int(row.get("id")):
                                writer.writerow(row)
                        elif user_email is not None and user_id is None :
                            if str(user_email) != str(row.get("email")):
                                writer.writerow(row)
                    shutil.move(tempfile.name,self.file_)
                    print("user {email} has been deleted ".format(email=user["email"]))
            except OSError:
                pass
        else:
            print("No such user")

            
            
                        
    #id increaser
    def id_passer(self):
        high_id = 0
        with open(self.file_,"r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) > int(high_id):
                    high_id= int(row["id"])
                
        return high_id + 1

    #adding users
    def add_user(self,first = "Geust",last = "User",email = None ,amount= None):
        with open(self.file_,"a") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=self.fieldnames)
            row = {
                "id": int(self.id_passer()),
                "first":first,
                "last":last,
                "email":email,
                "amount":amount,
                "sent":False,
                "date":datetime.datetime.now()
            }
            writer.writerow(row)
    
    def update_file(self,user_email = None,user_id = None):
        tempfile = NamedTemporaryFile(delete=True)
        user = self.get_user_data(user_email = user_email,user_id= user_id)
        if user:
            try:
                with open(self.file_,"rb") as filecsv, tempfile:
                    reader = csv.DictReader(filecsv)
                    writer = csv.DictWriter(tempfile,fieldnames=self.fieldnames)
                    writer.writeheader()
                    for row in reader:
                        if user_id is not None and user_email is None :
                            if int(user["id"]) == int(row.get("id")):
                                row["amount"] = float(input("enter the amount you would like to change : "))
                                row["date"] = datetime.datetime.now()
                                writer.writerow(row)
                            else:
                                writer.writerow(row)
                        elif user_email is not None and user_id is None :
                            if str(user["email"]) == str(row.get("email")):
                                row["amount"] = float(input("enter the amount you would like to change : "))
                                row["date"] = datetime.datetime.now()
                                writer.writerow(row)
                            else:
                                writer.writerow(row)
                        
                    shutil.move(tempfile.name,self.file_)
            except OSError:
                pass

    #Changing file "the sent to True or false"
    def edit_file(self):
        tempfile = NamedTemporaryFile(delete=True)
        with open(self.file_,"rb") as filecsv, tempfile:
            reader = csv.DictReader(filecsv)
            writer = csv.DictWriter(tempfile,fieldnames=self.fieldnames)
            writer.writeheader()
            for row in reader:
                if int(row["id"]) == int(self.user_data["id"]):
                    row["sent"] = True
                writer.writerow(row)
            shutil.move(tempfile.name,self.file_)
            
    def message_user(self, user_id=None, user_email=None, subject="Billing Update!"):
        user = self.get_user_data(user_id=user_id,user_email=user_email)
        if user:
            plain_, html_ = self.render_message(user_id = user_id,user_email=user_email)
            user_email = user.get("email", "hello@teamcfe.com")
            self.to_list.append(user_email)
            try:
                print('sending ....')
                email_conn = smtplib.SMTP(self.host, self.port)
                email_conn.set_debuglevel(1)
                email_conn.ehlo()
                email_conn.starttls()
                email_conn.login(self.username, self.password)
                the_msg = MIMEMultipart("alternative")
                the_msg['Subject'] = subject
                the_msg["From"] = "helpcenter@apple.com"
                the_msg["To"]  = user_email
                part_1 = MIMEText(plain_, 'plain')
                part_2 = MIMEText(html_, "html")
                the_msg.attach(part_1)
                the_msg.attach(part_2)
                email_conn.sendmail(self.username, self.to_list, the_msg.as_string())
                email_conn.quit()
                self.edit_file()
            except smtplib.SMTPException:
                print("error sending message")

        
    def render_message(self,user_id = None, user_email = None):
        self.user_data = self.get_user_data(user_id = user_id,user_email=user_email)
        if isinstance(self.user_data,dict):
            file_txt = "templates/email_txt.txt"
            file_html = "templates/email_html.html"
            template_txt = get_template(file_txt)
            template_html = get_template(file_html)
            context = self.user_data
            plain_= render_context(template_txt,context)
            html_ = render_context(template_html,context)
            return (plain_,html_)
        return None

    def get_user_data(self,user_id = None,user_email = None):
        filename = os.path.join(os.path.dirname(__file__),"document/data.csv")
        self.user = []
        with open(filename,"r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if user_id is not None:
                    if int(row["id"]) == int(user_id):
                        self.user.append(row)
                        self.user_data = row
                elif user_email is not None:
                    if str(row.get("email")) == str(user_email):
                        self.user.append(row)
                        self.user_data = row
            if self.user == []:
                if user_email is not None:
                    print("Email : {user_email} does not exist in the base !".format(user_email=user_email))

                elif user_id is not None:
                    print("Id : {user_id} does not exist in the base !".format(user_id=user_id))
                return None
            
            return self.user_data

                