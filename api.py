
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

try:
 clf = nfc.ContactlessFrontend('usb')
except Exception, e:
 print e



def write_to_file(content,file_name): # Text records
  fo = open("uploads/"+file_name+".jpg","wb")
  fo.write(content)
  return("uploads/"+file_name+".jpg")

@app.route('/')
def index():
  try:
    return jsonify(name=clf.dev.product, vendor=clf.dev.vendor, capabilities=clf.dev.capabilities), 200
  except Exception, e:
    return "Unable to find Reader please make sure the Reader is connected", 400
  

@app.route('/card-api/read')
def read():
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
    
    return json.dumps(card_data)
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
  try:
    tag = clf.connect(rdwr={'on-connect': None})
    ndef_records = []
    
    for key in request.form:
      ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", key, str(request.form[key])))
    
    if request.files:
      file_response = process_img(request)
      img_url = json.loads(file_response.data)['file_path']
      ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", "photo",read_photo(img_url)))

    tag.ndef.message = nfc.ndef.Message(ndef_records)

    return "Tag was written successfully",200

  except Exception, e:
    return "Unable to write Tag -> "+str(e), 500

if __name__ == "__main__":
  app.run( 
    host="0.0.0.0",
    port=int("5000")
  )
# write()
# read()
