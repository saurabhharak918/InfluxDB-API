# save this as app.py
from flask import Flask,render_template
from flask.globals import request

app = Flask(__name__)

@app.route('/')
def Get_time():
    return render_template('home.html',data=[{'name':'1m'}, {'name':'2m'}, {'name':'3m'},{'name':'10m'},{'name':'30m'},{'name':'45m'},{'name':'1h'},{'name':'2h'},{'name':'3h'},{'name':'6h'},{'name':'15h'},])

@app.route("/test" , methods=['GET', 'POST'])

def test():
    select = request.form.get('get_time')
    data = get_the_data(str(select))
    jsondata = data.to_json(orient='index')
    return(jsondata)


def get_the_data(time):
    import pandas as pd
    from influxdb_client import InfluxDBClient
    from influxdb_client.client.write_api import SYNCHRONOUS


    token = "CCnNI4aAzqWKUMMMFLTxE9jZLembWconNmgLNHxNpHLlR9VfvKcfexcLYWTCrvN6HGcvqMBKEXdLvfU-6l8KJA=="
    org = "autointelli"
    bucket = "autointelli"

    client = InfluxDBClient(url="http://172.16.1.4:8086", token=token,org = org)
    query_api = client.query_api()
    tm = str(time)
    query= '''
    from(bucket: "autointelli")
    |> range(start:'''+'-'+tm+''', stop: now())
    |> filter(fn: (r) => r._measurement == "cpu")
    |> filter(fn: (r) => r._field == "usage_user")
    |> filter(fn: (r) => r.cpu == "cpu-total")'''


    tables = query_api.query_data_frame(query)
    return tables



if __name__ == '__main__':
    app.run(debug=True)


