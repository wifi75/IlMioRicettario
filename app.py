from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']='dev'

@app.route('/')
def index():
    return 'Il Mio Ricettario V1'

if __name__ == '__main__':
    app.run(debug=True)
