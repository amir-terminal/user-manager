import csv
import os
import datetime
from tempfile import NamedTemporaryFile

def get_data(user_id = None,user_email = None):
    filename = os.path.join(os.path.dirname(__file__),"document/data.csv")
    user = []
    with open(filename,"r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if user_id is not None:
                if int(row["id"]) == int(user_id):
                    user.append(row)
  
            elif user_email is not None:
                if str(row.get("email")) == str(user_email):
                    user.append(row)
        if user == []:
            if user_email is not None:
                return "Email : {user_email} does not exist in the base !".format(user_email=user_email)
            elif user_id is not None:
                return "Id : {user_id} does not exist in the base !".format(user_id=user_id)
        else:
            return user
            