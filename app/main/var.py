import json
from flask import request
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/search', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    return result