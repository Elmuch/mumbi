
import nfc
from flask import Flask,send_file,request,jsonify
import binascii
from flask.ext.cors import CORS 
import pdb

app = Flask(__name__)

CORS(app, resources=r'/api/*', allow_headers='Content-Type')

clf = nfc.ContactlessFrontend('usb')

@app.route('/card-api/read')
def read():
	tag = clf.connect(rdwr={'on-connect': None})
	print tag.ndef.message.pretty()
	return str(tag.ndef.message)

filename = 'photo.jpg'
with open(filename, 'rb') as f:
    content = f.read()
	# 
	# record11 = nfc.ndef.Record("urn:nfc:wkt:T", "photo", binascii.hexlify(content))

@app.route("/card-api/write", methods=['POST'])
def write():
	tag = clf.connect(rdwr={'on-connect': None})
	data = request.json
	ndef_records = []
	for key in data:
		ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", key,str(data[key])))

	tag.ndef.message = nfc.ndef.Message(ndef_records)

	return jsonify(data)

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