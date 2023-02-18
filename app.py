from flask import Flask, g, render_template, request, abort

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sqlite3

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import base64

### stuff from last class
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit-basic.html')
    else:
        try:
            if request.form['name'] and request.form['message']:
                insert_message(request)
                return render_template('submit-basic.html', info=True, message = request.form['message'], 
                                        name = request.form['name'])
            else:
                return render_template('submit-basic.html', error=True)
        except:
            return render_template('submit-basic.html', error=True)

@app.route('/view/')
def view():
    return render_template('view.html', messages = random_messages(5))

def get_message_db():
  # write some helpful comments here
  try:
          print('testing connection...')
          return g.message_db
  except:
          g.message_db = sqlite3.connect("messages_db.sqlite")
          cmd = '''
          CREATE TABLE IF NOT EXISTS messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          handle VARCHAR(255),
          message VARCHAR(255)
          );
          '''
          cursor = g.message_db.cursor()
          cursor.execute(cmd)
          print('not connected, connected to a database')
          return g.message_db
  
def insert_message(request):
    db = get_message_db()
    print('connected, and ready to command')
    cmd = '''
    INSERT INTO messages (handle, message)
    VALUES (?,?)
    '''
    cursor = db.cursor()
    print('cursor created')
    cursor.execute(cmd,(request.form['name'],request.form['message']))
    print('I\'ve inserted ',(request.form['name'],request.form['message']))
    db.commit()
    db.close()

def random_messages(n):
    db = get_message_db()
    cmd = '''
    SELECT * FROM messages ORDER BY RANDOM() LIMIT (?);
    '''
    cursor=db.cursor()
    cursor.execute(cmd,(n,))
    messages=cursor.fetchall()
    db.commit()
    db.close()
    print(messages)
    return messages

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)