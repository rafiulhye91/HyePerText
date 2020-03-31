from flask import Flask
from flask import request
import configparser
import os
import smtplib
import socket
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(dir_path+'/config.ini')
gmail_user = config.get('credentials', 'user')
gmail_password = config.get('credentials', 'passwd')
subscribers = config.get('subscription','subscribers')

app = Flask(__name__)

def send_sms_via_email(to, subject, body):
    
    sent_from = gmail_user
    #to = subscribers.split(',')
    
    email_text = """To: %s\nSubject: %s\n\n%s\n    	""" % (", ".join(to), subject, body)
    
    try:
        print(str(datetime.datetime.now())+" -"+'Sending text...')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        return str(datetime.datetime.now())+" -"+'Text sent: '+str(to)
    except:
        return str(datetime.datetime.now())+" -"+'Failed to send text'

@app.route("/test")
def home():
    to = subscribers.split(',')
    return send_sms_via_email(to, "test", "body")
    
@app.route("/send-text")
def send_text():
    number = request.args.get('number', default = "", type = str)
    to =number+'@tmomail.net'
    subject = request.args.get('subject', default = "", type = str)
    body = request.args.get('body', default = "", type = str)
    return send_sms_via_email(to, subject, body)
    
if __name__ == '__main__':
    app.run(debug=True)    