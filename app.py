from utils import *
from urllib import response
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import requests
import json

app = Flask(__name__)

artworks_app = App(uri="bolt://54.92.211.62:7687", username = "neo4j", password="detonation-cases-loudspeaker")
driv = artworks_app.create_driver()

# print(driv.run("MATCH (n) RETURN n LIMIT 25"))

upload_folder = os.path.join('static', 'uploads')

app.config['UPLOAD'] = upload_folder

@app.route("/") 
def index():
    query = """
    MATCH (n:Artwork)
    RETURN n.image_url 
    LIMIT 1
    """
    image = driv.run(query).to_data_frame()
    return render_template('index.html', image=image['n.image_url'][0])

@app.route('/search')
def search():
    return None


@app.route('/style-transfer', methods=['GET', 'POST'])
def style_transfer():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('style-transfer.html', img=img)
    return render_template('style-transfer.html')

app.run(host="0.0.0.0", port=80, debug=True)
