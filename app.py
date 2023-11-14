from flask import Flask, render_template, request
from flask_basicauth import BasicAuth
import sqlite3

app = Flask(__name__)

# Configuration
DATABASE = 'starwars.db'

# Configure Flask-BasicAuth
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
basic_auth = BasicAuth(app)


@app.route('/')
@basic_auth.required
def index():
    # Fetch all starwars data
    starwars_data = fetch_starwars_data()
    manufacturers = fetch_manufacturers()
    print(manufacturers)
    return render_template('index.html', starwars_data=starwars_data, manufacturers=manufacturers)

@app.route('/filter', methods=['POST'])
@basic_auth.required
def filter_starwars():
    manufacturer = request.form.get('manufacturer')
    starwars_data = fetch_starwars_data(manufacturer)

    return render_template('filtered_starwars.html', starwars_data=starwars_data, selected_manufacturer=manufacturer)

def fetch_starwars_data(manufacturer=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if manufacturer:
        query = f"SELECT * FROM starwars WHERE manufacturer = '{manufacturer}'"
    else:
        query = "SELECT * FROM starwars"

    cursor.execute(query)
    starwars_data = cursor.fetchall()

    conn.close()

    return starwars_data

def fetch_manufacturers():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT manufacturer FROM starwars")
    manufacturers = [row[0] for row in cursor.fetchall()]

    conn.close()

    return manufacturers

if __name__ == '__main__':
    app.run(debug=True)
