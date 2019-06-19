import string

from flask import Flask, render_template, request
import pyodbc
import os
import redis
import time
import random
import redis
from math import sin, cos, sqrt, atan2, radians

application = app = Flask(__name__)

# port = int(os.getenv("VCAP_APP_PORT", '5000'))
# port = os.getenv("VCAP_APP_PORT")


myHostname = "freebird.redis.cache.windows.net"
myPassword = "Rz1ycTO3oebJcgLJRIdLUrJZAveKitHsJ0gJhat6QNs="

r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)

result = r.ping()
print("Ping returned : " + str(result))

server = 'mysqlserver6429.database.windows.net'
database = 'MyDB'
username = 'shreya6429'
password = 'Myaccount@123'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/options', methods=['POST', 'GET'])
def options():
    start_time = time.time()
    num = int(request.form['num'])
    rows = []
    get = []
    c = []
    points = []
    points.append(['Mag','Query Count'])
    for i in range(num):
        val = round(random.uniform(2,5),1)
        cur = cnxn.cursor()
        a = 'select * from all_months WHERE mag = '+str(val)
        v = str(val)
        if r.get(a):
            c.append('Cached')
            rows.append(r.get(a))
        else:
            print('Not Cached')
            c.append('Not Cached')
            cur.execute("select count(*) from all_months WHERE mag = ?" ,(val,))
            get = cur.fetchone();
            rows.append(get)
            r.set(a,str(get))
        count = rows[i][0]
        points.append([str(val), count])
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("chart_scatter1.html", rows=[c], etime=elapsed_time, p=points)


if __name__ == '__main__':
    app.run(debug=True)

# app.run(host='0.0.0.0', port=port)
# app.run(host='127.0.0.1', port=port)
