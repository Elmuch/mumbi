clf = nfc.ContactlessFrontend('usb')
tag = clf.connect(rdwr={'on-connect':None})
sp = nfc.ndef.SmartPosterRecord('htttp://www.egachuhi.me')
sp.title = "His Awesomeness"
tag.ndef.message = nfc.ndef.Message(sp)
print nfc.ndef.SmartPosterRecord(tag.ndef.message[0].pretty())
