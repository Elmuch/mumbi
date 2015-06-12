
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
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024

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
def startConnection():
  try:
   clf = nfc.ContactlessFrontend('usb')
   return clf
  except Exception, e:
   print e



def write_to_file(content,filename): # Text records
  updir = os.path.join(basedir, 'uploads/')
  fo = open(os.path.join(updir,filename),"wb")
  fo.write(content)
  return os.path.join(updir,filename)

@app.route('/')
def index():
  clf = startConnection()
  try:
    device_info = jsonify(name=clf.dev.product, vendor=clf.dev.vendor, capabilities=clf.dev.capabilities)
    clf.close()
    return device_info, 200
  except Exception, e:
    return "Unable to find Reader please make sure the Reader is connected", 400
  

@app.route('/card-api/read')
def read():
  clf = startConnection()
  try:
    tag = clf.connect(rdwr={'on-connect': None})
    card_data = []
    ndef_record = {}

    for record in tag.ndef.message:
      if record.name == 'photo':
        img_url = write_to_file(record.data,"test_photo")
        ndef_record['data'] = img_url 
        ndef_record["type"] = record.type
        ndef_record["name"] = record.name
        card_data.append(ndef_record.copy())
        continue

      ndef_record["data"] = record.data
      ndef_record["type"] = record.type
      ndef_record["name"] = record.name

      card_data.append(ndef_record.copy())

    clf.close()
    return json.dumps(card_data),200
  except Exception, e:
    return "Unable to read Tag"+str(e),500

def read_photo(url):
  f = open(url, 'rb')
  return f.read()

def process_img(request):
  files = request.files['file']
    
  if files and allowed_file(files.filename):
    filename = secure_filename(files.filename)
    app.logger.info('FileName: ' + filename)
    updir = os.path.join(basedir, 'uploads/')
    files.save(os.path.join(updir, filename))
    file_size = os.path.getsize(os.path.join(updir, filename))

    return jsonify(name=filename, size=file_size, file_path=os.path.join(updir,filename))

@app.route("/card-api/write", methods=['POST'])
def write():
  clf = startConnection()
  ndef_record = {}
  ndef_pretty = []

  try:
    tag = clf.connect(rdwr={'on-connect': None})
    ndef_records = []
    
    for key in request.form:
      ndef_record['name'] = key
      ndef_record['data'] = request.form[key]
      ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", key, str(request.form[key])))
      ndef_pretty.append(ndef_record.copy())
    
    if request.files:
      file_response = process_img(request)
      img_url = json.loads(file_response.data)['file_path']
      ndef_record['name'] = 'photo'
      ndef_record['data'] = img_url
      ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", "photo",read_photo(img_url)))
      ndef_pretty.append(ndef_record.copy())

    tag.ndef.message = nfc.ndef.Message(ndef_records)

    clf.close()
    return json.dumps(ndef_pretty),200

  except Exception, e:
    return "Unable to write Tag -> "+str(e), 500
