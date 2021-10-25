from jinja2 import Template
from requests import post
from pyqrcode import create
from io import BytesIO
from pymongo import MongoClient
from uuid import uuid4
from json import dump

client = MongoClient()

db = client.freshersParty

ticketsCollection = db.tickets

ticketsCollection.delete_many({})

GOTENBERG = "http://localhost:3000/forms/chromium/convert/html"

tickets = [{'firstName': 'Noah', 'lastName': 'Reilly', 'amount': 300,"branch":"CSE"},
           {'firstName': 'Lori', 'lastName': 'Stone', 'amount': 500,"branch":"CSE"},
           {'firstName': 'Brian', 'lastName': 'Wilkerson', 'amount': 500,"branch":"CSE"},
           {'firstName': 'Jose', 'lastName': 'Jackson', 'amount': 500,"branch":"CSE"},
           {'firstName': 'Melanie', 'lastName': 'White', 'amount': 300,"branch":"CSE"},
           {'firstName': 'Mary', 'lastName': 'White', 'amount': 500,"branch":"CSE"},
           {'firstName': 'Angela', 'lastName': 'Cox', 'amount': 500,"branch":"CSE"},
           {'firstName': 'Scott', 'lastName': 'Scott', 'amount': 300,"branch":"CSE"},
           {'firstName': 'Kathryn', 'lastName': 'Romero', 'amount': 500,"branch":"CSE"},
           {'firstName': 'Richard', 'lastName': 'Benitez', 'amount': 500,"branch":"CSE"}
]

paperData = {
	'paperWidth': 3.8,
	'paperHeight': 6.19,
	"marginTop": 0.05,
	"marginBottom": 0.05,
	"marginLeft": 0.05,
	"marginRight": 0.05
}

with open("ticket.html","r") as file:
	htmlFile = file.read()

with open("oysterbay.jpeg","rb") as file:
	oysterBayImage = file.read()

with open("style.css","r") as file:
	cssStyles = file.read()

template = Template(htmlFile)

for ticket in tickets:
	ticket['_id'] = uuid4().hex
	ticket['isValid'] = True

with open("tickets.json",'w') as jsonFile:
	dump(tickets,jsonFile,indent=4)

for userData in tickets:

	qrData = f"{userData['firstName']} {userData['lastName']} {userData['amount']} : {userData['_id']} "

	qr = create(qrData,encoding='utf-8')

	qrCodePng = BytesIO()

	qr.png(qrCodePng)

	qrCodePng.seek(0)

	output = template.render(userData)
	outputFile = BytesIO(bytes(output,encoding='utf-8'))

	response = post(GOTENBERG, data = paperData, files=[('index.html',outputFile),
														('oysterbay.jpeg',oysterBayImage),
														('style.css',cssStyles),
														("qrCode.png",qrCodePng)])
	pdfFile = BytesIO(response.content)

	with open(f"{userData['firstName']}_{userData['lastName']}.pdf","wb") as file:
		file.write(pdfFile.getvalue())

ticketsCollection.insert_many(tickets)