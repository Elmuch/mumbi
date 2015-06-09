
import nfc
from flask import Flask 
import binascii
from flask import send_file

app = Flask(__name__)

clf = nfc.ContactlessFrontend('usb')
print(clf)
print('Touch a tag')


@app.route('/card-api/read')
def read():
	tag = clf.connect(rdwr={'on-connect': None})
	return str(tag.ndef.message)


# uri = 'http://www.egachuhi.me' # These will be transimitted via a url-params 
# awesomeness= "His Dudeness"
tag = clf.connect(rdwr={'on-connect': None})

filename = 'photo.jpg'
with open(filename, 'rb') as f:
    content = f.read()

# @app.route("/card-api/write")
def write():
	record1 = nfc.ndef.Record("urn:nfc:wkt:T", "id", "\x02en123232!")
	record2 = nfc.ndef.Record("urn:nfc:wkt:T", "name", "\x02deElijah!")
	record3 = nfc.ndef.Record("urn:nfc:wkt:T", "dob", "\x02de21-2-1970")
	record4 = nfc.ndef.Record("urn:nfc:wkt:T", "lt", "\x02de10000")
	record5 = nfc.ndef.Record("urn:nfc:wkt:T", "ct", "\x02deHallo Welt!")
	record7 = nfc.ndef.Record("urn:nfc:wkt:T", "id7", "\x02deHallo Welt!")
	record8 = nfc.ndef.Record("urn:nfc:wkt:T", "id8", "\x02deHallo Welt!")
	record9 = nfc.ndef.Record("urn:nfc:wkt:T", "id9", "\x02deHallo Welt!")
	record10 = nfc.ndef.Record("urn:nfc:wkt:T", "id10", "\x02deHallo Welt!")
	record11 = nfc.ndef.Record("urn:nfc:wkt:T", "photo", binascii.hexlify(content))
	tag.ndef.message = nfc.ndef.Message([record1, record2,record3,record4,record11,record5,record7,record8,record10])

def connected(tag):
	print tag
	return tag

def connect():
	print str(tag.ndef.message.pretty())

@app.route('/')
def index():
	return str(clf)

@app.route('/photo')
def photo():
	return(send_file(filename))

write()
# connect()

if __name__ == "__main__":
  app.run()