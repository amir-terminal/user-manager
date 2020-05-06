from argparse import ArgumentParser
from data_class import UserManager
from utils.templates import render_context


parser = ArgumentParser(prog="usermanager")
parser.add_argument("-id","--user_id",type=int)
parser.add_argument("-e","--user_email",type=str)
parser.add_argument('-f',"--first",type = str)
parser.add_argument('-l',"--last",type = str)
parser.add_argument('-a',"--amount",type = float)
parser.add_argument("type",type = str,choices=["view","message","add","delete","update"])
args = parser.parse_args()


if args.type == "view":
    if args.user_id == None:
        print(UserManager().get_user_data(user_email = args.user_email,user_id=args.user_id))
    else:
        print(UserManager().get_user_data(user_email = args.user_email,user_id=args.user_id))
elif args.type == "message":
    UserManager().message_user(user_id=args.user_id,user_email = args.user_email)
elif args.type == "add":
    UserManager().add_user(first = args.first,last=args.last,email = args.user_email,amount=args.amount)
elif args.type == "delete":
    UserManager().delete_user(user_id=args.user_id,user_email=args.user_email)
else:
    UserManager().update_file(user_email = args.user_email,user_id=args.user_id)

