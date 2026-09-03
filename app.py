from flask import Flask, render_template, request
import resend
from resend.exceptions import ResendError
import os

app = Flask(__name__)

resend.api_key = os.environ["RESEND_API_KEY"]



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

