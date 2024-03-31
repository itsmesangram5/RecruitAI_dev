import mysql.connector
import json

class user_model():
    def __init__(self):
        try:
           self.con=mysql.connector.connect(host="localhost",user="root",password="tiger",database="flask_tutorial")
           self.cur=self.con.cursor(dictionary=True)
           print("Connected succesfully")
        except:
            print("Some Error")

    def user_get(self):
        self.cur.execute("SELECT * FROM users")
        result=self.cur.fetchall()
        #print(result)
        return json.dumps(result)
    
    def user_signup_model(self):
        return "This is user signUp model"
    
    def user_add(self,data):
        print(data['email'])
        return "request.form"