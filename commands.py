from flask import Flask, render_template, request
import subprocess
import sys
import os
import numpy
import pandas
from werkzeug.useragents import UserAgent

app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"

@app.route("/powershell", methods=['GET', 'POST'])
def powershell():
    output=''
    command=''
    isWindows=False
    FileSystemRights=''
    AccessControlType=''
    IdentityReference=''
    IsInherited=''
    InheritanceFlags=''
    PropagationFlags=''
    myheader=[]
    mylist=[]

    user_agent=UserAgent(request.headers.get('User-Agent'))
    platform=sys.platform
    cwd=os.getcwd()

    if platform.startswith('win32'): # 'linux', 'darwin', 'win32'
        isWindows=True

    if request.method=='POST':
        output=''

        command=r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
        script=request.form['script']
        argument=request.form['argument']
        try:
            if len(script) <=0:
                p = subprocess.Popen([command, '-ExecutionPolicy', 'Unrestricted', script],
                                      shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.getcwd())
            else:
                # './website/static/script/readdir.ps1'
                # 'D:/Public'
                if len(argument) <=0:
                    p = subprocess.Popen([command, '-ExecutionPolicy', 'Unrestricted', script],
                                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.getcwd())
                else:
                    argument='"'+argument+'"'
                    p = subprocess.Popen([command, '-ExecutionPolicy', 'Unrestricted', script, argument],
                                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.getcwd())
            for line in p.stdout.readlines():
                text=line.decode('utf-8', 'slashescape')
                output+=text
                tuples=list();
                if text[:16]=='FileSystemRights':       #FileSystemRights  : ReadAndExecute, Synchronize
                    FileSystemRights=text[19:].strip()
                    AccessControlType=''
                    IdentityReference=''
                    IsInherited=''
                    InheritanceFlags=''
                    PropagationFlags=''
                elif text[:17]=='AccessControlType':    #AccessControlType : Allow
                    AccessControlType=text[20:].strip()
                elif text[:17]=='IdentityReference':    #IdentityReference : Everyone
                    IdentityReference=text[20:].strip()
                elif text[:11]=='IsInherited':          #IsInherited       : False
                    IsInherited=text[19:].strip()
                elif text[:16]=='InheritanceFlags':     #InheritanceFlags  : ContainerInherit, ObjectInherit
                    InheritanceFlags=text[19:].strip()
                elif text[:16]=='PropagationFlags':     #PropagationFlags  : None
                    PropagationFlags=text[19:].strip()
                    mylist.append([FileSystemRights,AccessControlType,IdentityReference,IsInherited,InheritanceFlags,PropagationFlags])
        except:
            output=sys.exc_info()[0]

        command=command + ' ' + script + ' ' + argument
        if len(mylist) > 0 :
            myheader=['FileSystemRights','AccessControlType','IdentityReference','IsInherited','InheritanceFlags','PropagationFlags']

    try:
        return render_template('powershell.html', output=output, command=command, user_agent=user_agent, platform=platform, isWindows=isWindows, cwd=cwd, mylist=mylist, myheader=myheader)
    except:
        return render_template('error.html', errormessage=sys.exc_info())

@app.route("/", methods=['GET', 'POST'])
def index():
    output=''
    command=''
    isWindows=False

    user_agent=UserAgent(request.headers.get('User-Agent'))
    platform=sys.platform
    cwd=os.getcwd()

    if platform.startswith('win32'): # 'linux', 'darwin', 'win32'
        isWindows=True

    if request.method=='POST':
        output=''

#        for key in request.form:
#            output+=key+': '
#            output+=request.form[key]+', '

#p = subprocess.Popen(['powershell.exe', script], stdout=sys.stdout)
#p.communicate()

#psxmlgen = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
#                             '-ExecutionPolicy',
#                             'Unrestricted',
#                             './helloworld.ps1',
#                             'Hello'],
#                             cwd=os.getcwd())
#result = psxmlgen.wait()

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
        return render_template('index.html', output=output, command=command, user_agent=user_agent, platform=platform, isWindows=isWindows, cwd=cwd)
    except:
        return render_template('error.html', errormessage=sys.exc_info())

if __name__ == '__main__':
    app.debug=True
    app.run()
