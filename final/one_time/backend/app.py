from flask import Flask, jsonify
import pyodbc


server = "server-itt.database.windows.net"
database = "dwdm"
username = "wefeelfineadmin"
password = "wefeelfine@123"
connectionString = f"""DRIVER={{SQL Server}};
                      SERVER={server};
                      DATABASE={database};
                      UID={username};
                      PWD={password};"""


app = Flask(__name__)
# don't modify above here


@app.route("/sentences/<number>", methods=['GET'])
@app.route("/sentences/", methods=['GET'])
def send(number = 100):
    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()
    SQL = f"SELECT TOP {number} * FROM UTTERANCE ORDER BY newid();"
    cursor.execute(SQL)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    count = len(rows)
    results = []
    for row in rows:
        results.append(dict(zip(columns, row)))

    # don't modify this

    cursor.commit()
    cnxn.close()
    response = jsonify({"number": count, "results": results})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



# don't modify below here
if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True)
    app.run()
