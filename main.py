from flask import Flask, render_template, url_for, request
# from flask_mysqldb import MySQL
#import pymysql
import EncryptionData
import createKet
import mysql.connector
import DecryptionData

#to hash pw
import hashlib

app = Flask(__name__)

#connect to db
conn = mysql.connector.connect(host = 'localhost', user = 'sugandi', password = 's1234', database = 'security')

#login page
@app.route('/', methods =['GET','POST'])
def login():

    #get data from user table
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']

        hashObject = hashlib.md5(pw.encode('utf-8'))
        digest = hashObject.hexdigest()

        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE email =%s AND password = %s", (email,digest))
        result = cur.fetchone()
        if result:
            role = result[2]
            return render_template('viewMessage.html',role1=role)
        
        else:
            msg ="Incorrect username or password"
            return render_template('login.html', msg = msg)

    return render_template('login.html')

#register page
@app.route('/register', methods =['GET','POST'])
def register():
    
    #insert data to user table
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        role = request.form['jobRole']

        hashObject = hashlib.md5(pw.encode('utf-8'))
        digest = hashObject.hexdigest()

        cur = conn.cursor()
        cur.execute("INSERT INTO user (email,password,role) VALUES (%s,%s,%s)",(email,digest,role))
        conn.commit()
        return render_template('register.html')
    

    return render_template('register.html')

#send message page
@app.route('/sendMessage',methods =['GET','POST'])
def sendMessage():
    
    if request.method == "POST":
    
        message = request.form['message']
        role = request.form['role']
        print(message,role)
        createKet.KeyGeneration()
        EncryptionData.Encryption(message)
        
    return render_template('sendMessage.html')

#view message page
@app.route('/viewMessage',methods =['GET','POST'])
def viewMessage():
    msg = (DecryptionData.Decryption())
    return render_template("viewMessage.html", decryptmsg=msg)


if __name__ == "__main__":
    app.run(debug=True)
