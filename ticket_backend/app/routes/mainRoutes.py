from app import app
from app.db import mainDB
from flask import  Response,render_template
from json import dumps

@app.route('/',methods=['GET'])
def index():
	return Response("Server Running : 200 OK",200)

@app.route("/qr",methods=['GET'])
def qrScanner():
	return render_template("qr.html")

@app.route("/ticket/<tid>",methods=['GET'])
def checkTicket(tid):
	ticketData = mainDB.checkTicketValid(tid)
	return Response(dumps(ticketData['message']),status=ticketData['status'])