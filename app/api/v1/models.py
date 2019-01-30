
import datetime

USER_DB = []


class User():

    def __init__(self):
        self.db = USER_DB
        self.save(
            first_name="Eric",
            last_name="Muchogo",
            other_names="Ndungu",
            phonenumber="0725530122",
            email="erimucho@gmail.com",
            username="Muchogo",
            password="1000",
            isAdmin=True
        )

    def save(self, first_name, last_name, other_names, phonenumber,
             email, username, password, isAdmin=False):

        data = {
            "userid": len(self.db) + 1,
            "first_name": first_name,
            "last_name": last_name,
            "other_names": other_names,
            "phonenumber": phonenumber,
            "username": username,
            "email": email,
            "password": password,
            "isAdmin": isAdmin,
            "registeredOn": datetime.datetime.now(),
        }
        self.db.append(data)
        return data

    def check_username(self, username):
        return next(filter(lambda x: x['username'] == username, self.db), None)

    def check_email(self, email):
        return next(filter(lambda x: x['email'] == email, self.db), None)

    def confirm_login(self, username, pwd):
        return next(filter(lambda x: x['username'] == username and x['password'] == pwd, self.db), None)

    def search_user(self, id):
        return next(filter(lambda u: u['userid'] == id, self.db), None)


MEETUPS = [
    {
        "meetupsId": 1,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "location": "1.323,-2.32",
        "status": "draft",
        "comment": "Discussion of Flask",
        "images": ['https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?cs=srgb&dl=beach-exotic-holiday-248797.jpg&fm=jpg']
    },
    {
        "meetupsId": 2,
        "createdOn": datetime.datetime.now(),
        "createdBy": 2,
        "location": "1.323,-2.32",
        "status": "Cancelled",
        "comment": "Fellowship of Django",
        "images": []
    },
    {
        "meetupsId": 3,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "location": "-1.28333, 36.81667",
        "status": "postponed",
        "comment": "Discussion on Agile",
        "images": []
    }
]

class MeetupsModel():
    def __init__(self):
        self.db = MEETUPS

    def save(self, comment, location, createdBy, images, videos, status="draft"):
        uid = len(self.db) + 1
        data = {
            "meetupsId": uid,
            "createdOn": datetime.datetime.now(),
            "createdBy": createdBy,
            "location": location,
            "status": status,
            "comment": comment,
            "images": images,
        }
        self.db.append(data)
        return data

    def search_meetups(self, id):
        return next(filter(lambda i: i["meetupsId"] == id, self.db), None)
    
