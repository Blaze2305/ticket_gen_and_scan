from jinja2 import Template
from requests import post
from pyqrcode import create
from io import BytesIO
from pymongo import MongoClient
from uuid import uuid4
from json import dump
from dotenv import load_dotenv
from os import environ
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib


load_dotenv()


EMAIL = environ['EMAIL']
PASSWORD = environ['PASSWORD']

client = MongoClient()

db = client.freshersParty

ticketsCollection = db.tickets

ticketsCollection.delete_many({})

GOTENBERG = "http://localhost:3000/forms/chromium/convert/html"

body_text='''
Rules and Regulations to be followed while attending the fresher's party: 

1. College ID Card is a must. 
2. Don't get alcohol/other substances from outside to the venue. 
3. Any kind of misbehaviour won't be tolerated.
4. You are responsible for your own valuables/belongings.  
5. Students staying in hostels who haven't made any arrangements, have to reach their hostels on time. 
6. If any damage to property is caused, students who caused the damage have to bear the costs. 
7. Tickets should be brought along as entry will not be allowed without tickets.

Students who violate any of the above rules, at any point of time, will be asked to leave the venue immediately.
'''

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(EMAIL, PASSWORD)


tickets = [
	{'name': 'Noah Reilly', 'type': "GOLD","branch":"CSE","email":"niefreshers2k21@gmail.com","semester":1,"section":"A"},
	{'name': 'Lori Stone', 'type': "PLATINUM","branch":"ISE","email":"niefreshers2k21@gmail.com","semester":5,"section":"B"},
	{'name': 'Brian Wilkerson', 'type': "PLATINUM","branch":"CSE","email":"niefreshers2k21@gmail.com","semester":1,"section":"B"},
	{'name': 'Jose Jackson', 'type': "PLATINUM","branch":"CSE","email":"niefreshers2k21@gmail.com","semester":5,"section":"B"},
	{'name': 'Melanie White', 'type': "GOLD","branch":"CSE","email":"niefreshers2k21@gmail.com","semester":5,"section":"A"},
	{'name': 'Mary White', 'type': "PLATINUM","branch":"CSE","email":"niefreshers2k21@gmail.com","semester":1,"section":"A"},
	{'name': 'Angela Cox', 'type': "PLATINUM","branch":"Mech","email":"niefreshers2k21@gmail.com","semester":5,"section":"B"},
	{'name': 'Scott Scott', 'type': "GOLD","branch":"CSE","EEE":"niefreshers2k21@gmail.com","semester":3,"section":"A"},
	{'name': 'Kathryn Romero', 'type': "PLATINUM","branch":"ISE","email":"niefreshers2k21@gmail.com","semester":5,"section":"B"},
	{'name': 'Richard Benitez', 'type': "PLATINUM","branch":"CSE","email":"niefreshers2k21@gmail.com","semester":7,"section":"B"}
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

	qrData = f"{userData['name']} {userData['type']} : {userData['_id']} "

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

	with open(f"{userData['name']}.pdf","wb") as file:
		file.write(pdfFile.getvalue())

	pdfFile.seek(0)


	# EMAIL SENDING

	msg = MIMEMultipart('mixed')
	msg['Subject'] = f"NIE Freshers Party 2021"
	msg['From'] = EMAIL
	msg['To'] = ','.join([userData['email']])

	msg_body = MIMEMultipart('alternative')

	htmlpart = MIMEText(body_text)

	msg_body.attach(htmlpart)

	ticketAttachment = MIMEApplication(pdfFile.getvalue())

	ticketAttachment.add_header("Content-Disposition",'attachment',filename="Ticket.pdf")

	msg.attach(ticketAttachment)

	msg.attach(msg_body)

	server.send_message(msg,EMAIL, [userData['email']])

ticketsCollection.insert_many(tickets)