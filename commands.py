from flask import Flask, render_template, request
import subprocess
import sys
import numpy as np
import pandas as pd
from werkzeug.useragents import UserAgent

app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"

@app.route("/", methods=['GET', 'POST'])
def index():
    output=''
    command=''
    isWindows=False

    user_agent=UserAgent(request.headers.get('User-Agent'))
    if str(user_agent).find('Windows')!=-1:
        isWindows=True

    if request.method=='POST':
        #output=''
#        for key in request.form:
#            output+=key+': '
#            output+=request.form[key]+', '

        command=request.form['command']
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                output+=line.decode('utf-8', 'slashescape')
        except:
            output=sys.exc_info()[0]
        #retval = p.wait()

        command=': '+command

    try:
        return render_template('index.html', output=output, command=command, user_agent=user_agent, isWindows=isWindows)
    except:
        return render_template('error.html', errormessage=sys.exc_info())

if __name__ == '__main__':
    app.debug=True
    app.run()
