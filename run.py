#!env/bin/python
##!winenv/Scripts/python.exe

from app import app

app.run(debug=True, host="0.0.0.0", port=int("5000"))
