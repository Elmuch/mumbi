
import nfc
import json
from flask import Flask,send_file,request,jsonify
import binascii
#from flask.ext.cors import CORS 
import pdb
from werkzeug import secure_filename
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir,'log.txt'),encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
  return '.' in filename and \
      filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

#CORS(app, resources=r'/api/*', allow_headers='Content-Type')

clf = nfc.ContactlessFrontend('usb')


def write_to_file(content,file_name): # Text records
  fo = open("uploads/"+file_name+".jpg","wb")
  fo.write(content)
  return("uploads/"+file_name+".jpg")

@app.route('/card-api/read')
def read():
  try:
    tag = clf.connect(rdwr={'on-connect': None})
  
    card_data = []
    ndef_record = {}

    for record in tag.ndef.message:
      if record.name == 'photo':
        img_url = write_to_file(record.data,"test_photo")
        ndef_record['data'] = img_url # Get the url and leave content in the card
        ndef_record["type"] = record.type
        ndef_record["name"] = record.name
        card_data.append(ndef_record.copy())
        continue

      ndef_record["data"] = record.data
      ndef_record["type"] = record.type
      ndef_record["name"] = record.name

      card_data.append(ndef_record.copy())
    
    return json.dumps(card_data)
  except Exception, e:
    return "Unable to read Tag"+str(e),500

def read_photo(url):
  f = open(url, 'rb')
  return f.read()

@app.route("/card-api/write", methods=['POST'])
def write():
  try:
    # tag = clf.connect(rdwr={'on-connect': None})
    data = request.json
    files = request.files['file']
    if files and allowed_file(files.filename):
      filename = secure_filename(files.filename)
      app.logger.info('FileName: ' + filename)
      updir = os.path.join(basedir, 'uploads/')
      files.save(os.path.join(updir, filename))
      file_size = os.path.getsize(os.path.join(updir, filename))
      return jsonify(name=filename, size=file_size)

    # ndef_records = []
    
    # for key in data:
    #   ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", key, str(data[key])))

    # # ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", "photo",read_photo('photo.jpg')))
    # tag.ndef.message = nfc.ndef.Message(ndef_records)

    # return "Tag was written successfully",200

  except Exception, e:
    return "Unable to write Tag -> "+str(e), 500

@app.route('/')
def index():
  return str(clf)

@app.route('/photo')
def photo():
  return(send_file(filename))


if __name__ == "__main__":
  app.run( 
    host="0.0.0.0",
    port=int("5000")
  )
# write()
# read()
