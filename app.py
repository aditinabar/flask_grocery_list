from flask import Flask, render_template, request
from flaskext.mysql import MySQL
# from config import Config

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = "localhost"
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = None
app.config['MYSQL_DATABASE_DB'] = "mystore"

mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()


@app.route("/add_inventory", methods=['POST'])
def addItem():
    try:
        item = request.form['item']
        cat = request.form['category']
        num = request.form['quantity']
        price = request.form['price']

        cursor.execute(f"INSERT INTO storeInventory (name, category, quantity, price)\
                         VALUES ('{item}', '{cat}', '{num}', '{price}')")
        connection.commit()

    except Exception as e:
        print(f"Could not write to database because of error: {e}")
        raise
    else:
        print("Data entered into database")

    return


@app.route("/see_list", methods=['GET'])
def getInventory():
    try:
        sql = "SELECT * FROM storeInventory"
        cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        print(f"Could not read inventory from database because of error: {e}")

    return render_template('inventory_list.html', results=data)


@app.route('/')
def main():
    return render_template('index.html', title='Home')


if __name__ == '__main__':
    app.run(debug=True)
