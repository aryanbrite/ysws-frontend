from flask import Flask, Blueprint, render_template

error = Blueprint("error", __name__)

@error.app_errorhandler(404)
def notfounderror(error):
    return render_template("404_error.html")