from flask import Flask, request, jsonify
import pickle
import random
import string

app = Flask(__name__)

class User:
    def __init__(self, firstname, surname,balance):
        self.firstname = firstname
        self.surname = surname
        self.pin = User.generate_pin()
        self.password = User.generate_password()
        self.account_type = type(self).account_type
        self.id = f"{self.account_type}{str(type(self).next_id_num).rjust(4, '0')}"
        self.id_number = type(self).next_id_num
        self.balance = balance
        type(self).next_id_num += 1

    def __str__(self):
        return f"""
Name: {self.firstname}
Id: {self.id}
"""

    def save(self, filename="data.pickle"):
        try:
            with open(filename, "rb") as rfile:
                data = pickle.load(rfile)
        except FileNotFoundError:
            data = {}

        data[self.id] = self

        with open(filename, "wb") as wfile:
            pickle.dump(data, wfile)

    @staticmethod
    def generate_password():
        password_chars = string.ascii_letters + string.digits + "£$%&@?"

        password = ""
        while not User.is_valid_password(password):
            password = "".join([random.choice(password_chars) for i in range(8)])
        return password

    @staticmethod
    def generate_pin():
        return str(random.randint(1, 9999)).rjust(4, "0")


    @staticmethod
    def is_valid_password(password):
        has_symbol = False
        for char in "£$%&@?":
            if char in password:
                has_symbol = True
        has_uppercase = False
        for char in string.ascii_uppercase:
            if char in password:
                has_uppercase = True
        has_lowercase = False
        for char in string.ascii_lowercase:
            if char in password:
                has_lowercase = True
        has_number = False
        for char in string.digits:
            if char in password:
                has_number = True
        return has_symbol and has_uppercase and has_lowercase and has_number and len(password) == 8

    @staticmethod
    def load(user_type, filename="data.pickle"):
        try:
            with open(filename, "rb") as file:
                data = pickle.load(file)
        except FileNotFoundError:
            data = {}

        highest_id = 0
        for i in data:
            if (data[i].id_number > highest_id) and (type(data[i]) == user_type):
                highest_id = data[i].id_number
        user_type.next_id_num = highest_id+1
        return {key:value for (key, value) in data.items() if type(value) == user_type}

class CurUser(User):
    account_type = "cur"
    next_id_num = 1

class DepUser(User):
    account_type = "dep"
    next_id_num = 1

User.load(CurUser)
User.load(DepUser)

@app.route('/')
def index():
    return "Basic Call Center App v1"


@app.route('/users', methods=['GET'])
def get_users():
    dep_users = User.load(DepUser)
    cur_users = User.load(CurUser)
    all_users = {**dep_users, **cur_users}
    return jsonify({user.id: user.__dict__ for user in all_users.values()})

@app.route('/new_user', methods=['POST'])
def new_user():
    data = request.json
    account_type = data.get('account_type')
    firstname = data.get('firstname')
    surname = data.get('surname')
    initial_balance = data.get('initial_balance')
    if initial_balance <= 0:
        return "Initial balance must be greater than 0", 400

    if account_type == "cur":
        user = CurUser(firstname, surname, initial_balance)
    else:
        user = DepUser(firstname, surname, initial_balance)
    user.save()

    return jsonify({
        "firstname": user.firstname,
        "surname": user.surname,
        "pin": user.pin,
        "password": user.password,
        "account_type": user.account_type,
        "id": user.id
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)