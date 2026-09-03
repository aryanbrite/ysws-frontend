from flask import Flask, render_template, request, redirect, session, url_for
import resend
from resend.exceptions import ResendError
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ["YUBIKEY"]

resend.api_key = os.environ["RESEND_API_KEY"]
HACKCLUB_CLIENT_ID = os.environ["HACKCLUB_CLIENT_ID"]
HACKCLUB_CLIENT_SECRET = os.environ["HACKCLUB_CLIENT_SECRET"]
REDIRECT_URL = os.environ["REDIRECT_URL"]



@app.route("/", methods = ["POST", "GET"])
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        session["mail"] = request.form.get("email")
        url = (f"https://auth.hackclub.com/oauth/authorize?client_id={HACKCLUB_CLIENT_ID}&redirect_uri={REDIRECT_URL}&response_type=code&scope=openid%20email%20name%20profile%20verification_status%20slack_id")
        return redirect(url)
        
        
        
    return render_template("index.html")

@app.route("/email")
def email():
    return render_template("email.html", name = session.get("user")["first_name"] )

@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    resp = requests.post("https://auth.hackclub.com/oauth/token", data = {
        "code":code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URL,
        "client_id": HACKCLUB_CLIENT_ID,
        "client_secret": HACKCLUB_CLIENT_SECRET
    } )
    access_token = resp.json()["access_token"]

    headers = {
            "Authorization": f"Bearer {access_token}"
        }

    dataauth = requests.get("https://auth.hackclub.com/api/v1/me", headers=headers)

    session["user"] = dataauth.json()["identity"]
    emailhtml = render_template("email.html", name = session.get("user")["first_name"] )
    params: resend.Emails.SendParams = {
        "from": "Pranjal <pranjal.hackclub@aryan.my>",
        "to": [session.get("mail")],
        "subject": "this is subject",
        "html": emailhtml,
    }
    
    try:
        email = resend.Emails.send(params) ## error tacking yaha se hogi ispe koi error tracker lagana hai 
        return redirect(url_for("dashboard"))
    except ResendError as error:
        return error

@app.route("/dashboard", methods = ["POST","GET"])
def dashboard():
    if "user" in session:
        if request.method == "POST":
                return redirect(url_for("logout"))
        return render_template("dashboard.html")
    else:
        return redirect(url_for("home"))



@app.route("/logout", methods=["POST"] )
def logout():
    session.clear()
    return redirect(url_for("home"))


