import string

from azure.storage.blob import BlockBlobService
from flask import Flask, render_template, request
import pyodbc
import os
import redis
import time
import random
import redis
import plotly.plotly as py
import plotly.graph_objs as go
from math import sin, cos, sqrt, atan2, radians
from plotly.figure_factory import np

application = app = Flask(__name__)

# port = int(os.getenv("VCAP_APP_PORT", '5000'))
# port = os.getenv("VCAP_APP_PORT")



server = 'mysqlserver6429.database.windows.net'
database = 'MyDB'
username = 'shreya6429'
password = 'Myaccount@123'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


block_blob_service = BlockBlobService(account_name = 'sqlvakgqkpxaark5yc', account_key = 'Qn2gu7TMRNXNLnodJakn4xaGrJoUD84FLxVCHcHaB+EyYamhbNhUyEedCA72J+gLrjDHziD7n2Joaw5HqTheKQ==')

container_name = 'quickstartblobs'
block_blob_service.create_container(container_name)

@app.route('/')
def home():
    return render_template('layout9.html')

@app.route('/q6', methods=['POST', 'GET'])
def q6():
    lat1 = float(request.form['lat1'])
    lat2 = float(request.form['lat2'])
    lon1 = float(request.form['long1'])
    lon2 = float(request.form['long2'])
    rows = []
    get = []
    c = []
    points = []
    points.append(['Lat Long Range','Count'])
    cur = cnxn.cursor()
    i = lat1
    j = lon1
    while(i < lat2 or j < lon2):
        cur.execute("select count(*) from all_month WHERE latitude between ? and ? and longitude between ? and ?",(i,i+1,j,j+1))
        get = cur.fetchone();
        key = str(i)+"-"+str(i + 1)+" & "+str(j)+"-"+str(j+1)
        points.append([key, get[0]])
        if(i < lat2):
            i =i+1
        if(j < lon2):
            j =j+1
    print(points)
    return render_template("pie_6.html", p=points)

@app.route('/q7', methods=['POST', 'GET'])
def q7():
    age1 = int(request.form['age1'])
    age2 = int(request.form['age2'])
    cab1 = int(request.form['cab1'])
    cab2 = int(request.form['cab2'])
    rows = []
    # get = []
    c = []
    points = []
    c.append(['age', 'Lat'])
    # val = round(random.uniform(2,5),1)
    cur = cnxn.cursor()
    cur.execute("select age,fare from minnow WHERE Age between ? and ? and Lat between ? and ?",
                (age1, age2, cab1 + '%', cab2 + '%'))
    get = cur.fetchall()
    for row in get:
        c.append([row[0]])
        print(c)
        # points.append([row[0], row[1]])
    return render_template("list1.html", rows=c)

@app.route('/q8', methods=['POST', 'GET'])
def q8():
    points = []
    points.append(['survived', 'notsurvived'])
    cur = cnxn.cursor()
    cur.execute("SELECT fare,COUNT(fare) FROM Assign4  GROUP BY fare ")
    a = cur.fetchall()
    cur.execute("SELECT fare,COUNT(fare) FROM Assign4 where Survived='0' GROUP BY fare")
    nonsur = cur.fetchall()
    f=[]
    ns=[]
    s=[]
    for row in a:
        f.append(row[0])
    for row in nonsur:
        ns.append(row[1])


    cur.execute("SELECT fare,COUNT(fare) FROM Assign4 where Survived='1' GROUP BY fare")
    b = cur.fetchall()
    for row in b:
        s.append(row[1])

    row = [f, ns, s]
    return render_template("q8horizontalbar.html", fare=f, ns=ns,s=s)

#---------------------------- scatter plot -----------------------------------------------------------------

@app.route('/options', methods=['POST', 'GET'])
def options():
    num = int(request.form['num'])
    rows = []
    c = []
    points = []
    style = {'role': 'style'}
    annotation = {'role': 'annotation'}
    points.append(['Mag', 'Query Count', style, annotation])
    for i in range(num):
        val = round(random.uniform(2, 5), 1)
        cur = cnxn.cursor()
        cur.execute("select count(*) from all_months WHERE mag = ?", (val,))
        get = cur.fetchone();
        rows.append(get)
        count = rows[i][0]
        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        points.append([val, count, color[0], count])

    return render_template("chart_scatter1.html", rows=[c], p=points)

#---------------------------- historical -----------------------------------------------------------------

@app.route('/historical', methods=['POST', 'GET'])
def historical():
    num = int(request.form['num'])
    rows = []
    c = []
    points = []
    style = {'role': 'style'}
    annotation = {'role': 'annotation'}
    points.append(['Mag', 'Query Count', style, annotation])
    for i in range(num):
        val = round(random.uniform(2, 5), 1)
        cur = cnxn.cursor()
        cur.execute("select count(*) from all_months WHERE mag = ?", (val,))
        get = cur.fetchone();
        rows.append(get)
        count = rows[i][0]
        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        points.append([val, count, color[0], count])

    return render_template("historical.html", rows=[c], p=points)

#---------------------------- column -----------------------------------------------------------------

@app.route('/chart_column', methods=['POST', 'GET'])
def chart_column():
    num = int(request.form['num'])
    rows = []
    c = []
    points = []
    style = {'role': 'style'}
    annotation = {'role': 'annotation'}
    points.append(['Mag', 'Query Count', style, annotation])
    for i in range(num):
        val = round(random.uniform(2, 5), 1)
        cur = cnxn.cursor()
        cur.execute("select count(*) from all_months WHERE mag = ?", (val,))
        get = cur.fetchone()
        rows.append(get)
        count = rows[i][0]
        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        points.append([val, count, color[0], count])

    return render_template("chart_column.html", rows=[c], p=points)

if __name__ == '__main__':
    app.run(debug=True)

# app.run(host='0.0.0.0', port=port)
# app.run(host='127.0.0.1', port=port)
