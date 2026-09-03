from flask import Flask, render_template, request, redirect, session
import resend
from resend.exceptions import ResendError
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ["YUBIKEY"]

resend.api_key = os.environ["RESEND_API_KEY"]
HACKCLUB_CLIENT_ID = os.environ["HACKCLUB_CLIENT_ID"]
HACKCLUB_CLIENT_SECRET = os.environ["HACKCLUB_CLIENT_SECRET"]



@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        mail = request.form.get("email")
        emailhtml = render_template("email.html")
        params: resend.Emails.SendParams = {
            "from": "Pranjal <pranjal.hackclub@aryan.my>",
            "to": [mail],
            "subject": "this is subject",
            "html": emailhtml,
        }

        try:
            email = resend.Emails.send(params)
            return email
        except ResendError as error:
            return error
        
    return render_template("index.html")

@app.route("/email")
def email():
    return render_template("email.html")

@app.route("/login")
def login():
    url = (f"https://auth.hackclub.com/oauth/authorize?client_id={HACKCLUB_CLIENT_ID}&redirect_uri=http://127.0.0.1:5000/oauth/callback&response_type=code&scope=openid%20email%20name%20profile%20verification_status%20slack_id")
    return redirect(url)

@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    resp = requests.post("https://auth.hackclub.com/oauth/token", data = {
        "code":code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://127.0.0.1:5000/oauth/callback",
        "client_id": HACKCLUB_CLIENT_ID,
        "client_secret": HACKCLUB_CLIENT_SECRET
    } )
    access_token = resp.json()["access_token"]

    headers = {
            "Authorization": f"Bearer {access_token}"
        }

    dataauth = requests.get("https://auth.hackclub.com/api/v1/me", headers=headers)

    session["user"] = dataauth.json()["identity"]
    return session["user"]
