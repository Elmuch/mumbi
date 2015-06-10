
import nfc
import json
from flask import Flask,send_file,request,jsonify
import binascii
from flask.ext.cors import CORS 
import pdb

app = Flask(__name__)

CORS(app, resources=r'/api/*', allow_headers='Content-Type')

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
		tag = clf.connect(rdwr={'on-connect': None})
		data = request.json
		ndef_records = []
		
		for key in data:
			ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", key, str(data[key])))

		ndef_records.append(nfc.ndef.Record("urn:nfc:wkt:T", "photo",read_photo('photo.jpg')))
		tag.ndef.message = nfc.ndef.Message(ndef_records)

		return "Tag was written successfully",200

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