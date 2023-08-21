
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import EarlyOnTable
app = Flask(__name__)

def main():
    return EarlyOnTable.getHtmlTable()

@app.route('/')
def hello_world():
    return main()

