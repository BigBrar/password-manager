import json


def read_file():
    with open("user_data.json",'r')as file:
        existing_data = json.load(file)
    return existing_data

def write_file(existing_data):
    with open("user_data.json",'w')as file:
        json.dump(existing_data,file)


def add_pass(user, username,email ,account, password, note):
    print("ENTERED FUNCTION")
    print("USER - ",user)
    new_data = {"username":username,"email":email,"account": account, "password": password, "note": note}
    #read file data..
    existing_data = read_file()
    index = -1
    for users in existing_data:
        index+=1
        if user == list(users.keys())[0]:
            print("user found!!!")
            print(users)
            existing_data[index][user]['passwords'].append(new_data)
            # write data to file...
            write_file(existing_data)


def verify_user(user):
    #read file...
    if not find_user(user):
        existing_data = read_file()
        json_string = {user:{"passwords":[]}}
        existing_data.append(json_string)
        # write data to file....
        write_file(existing_data)
        print("USER ADDED !!!")
    else:
        print('user already exists...')


def find_user(user):
    existing_data = read_file()
    for users in existing_data:
        if user == list(users.keys())[0]:
            return True
        else:
            continue
    return False

def get_pass(user):
    if not find_user(user):
        return "user not found..."
    existing_data = read_file()
    for users in existing_data:
        if user == list(users.keys())[0]:
            user_data = users[user]['passwords']
    return user_data


def edit_pass(index, user, account, username, email, note, password):
    existing_data = read_file()
    new_data = {'username': username, 'email': email, 'account': account, 'password': password, 'note': note}
    for users in existing_data:
        if user == list(users.keys())[0]:
            users[user]['passwords'][index-1] = new_data
            write_file(existing_data)

def delete_pass(user, index):
    existing_data = read_file()
    for users in existing_data:
        if user == list(users.keys())[0]:
            try:
                del users[user]['passwords'][index-1]
                write_file(existing_data)
                return True
            except:
                print("Something went wrong...")
                return False


# def check_if_empty(json_string):


# [{"username": "sardarioo", "email": "deepindersinghdeep03@gmail.com", "account": " ", "password": "madara", "note": "password for gmail"}, {"username": "sardarioo", "email": "deepindersinghdeep03@gmail.com", "account": "Google", "password": "madara", "note": "password for tmail"}]
