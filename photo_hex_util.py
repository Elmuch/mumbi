import binascii
filename = 'photo.jpg'
with open(filename, 'rb') as f:
    content = f.read()
print(binascii.hexlify(content))