from requests import Session
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:333btybfRA@127.0.0.1:5433/Assignment4'
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
db = SQLAlchemy(app)

class UserTable(db.Model):
    __tablename__ = 'crypto'
    id = db.Column('id', db.Unicode, primary_key = True)
    coin_name = db.Column('coin_name', db.Unicode)
    short_name = db.Column('short_name', db.Unicode)

    def __init__(self, id, coin_name, short_name):
        self.id = id
        self.coin_name = coin_name
        self.short_name = short_name

soup = BeautifulSoup('main.html', 'html.parser')

def findCoinId(cryptoName):
    return db.session.query(UserTable.id).filter_by(coin_name=cryptoName).first()

html = """<div class=my_class><form action="{{ url_for('news') }}"><input type=text name=coinInput></input> <input type=submit value="Send Request"></input></form> <p>news text</p></div>"""

def findNews(cryptoName):
    url = 'https://api.coinmarketcap.com/content/v3/news?coins=' + str(findCoinId(cryptoName))

    parameters = {
        'slug':cryptoName,
        'convert':'USD'
    }

    headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':'38334381-94e7-4f35-b5a7-7924dc4785c2'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    return response.text

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/news')
def news():
    coin = request.args.get('coinInput')

    with open("C:/Users/Gess/Desktop/pythonAssignments/Assignment4/src/templates/main.html", 'r') as f:
        html_file_as_string = f.read()

    soup = BeautifulSoup(html_file_as_string, "lxml")

    for div in soup.find_all('div', {'class': 'my_class'}):
        for p in div.find('p'):
            p.string.replace_with(str(findNews(coin)))

    with open('C:/Users/Gess/Desktop/pythonAssignments/Assignment4/src/templates/main.html', 'wb') as f:
        f.write(soup.renderContents())

    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)