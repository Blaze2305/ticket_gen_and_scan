from pymongo import MongoClient

client = MongoClient()

db = client.freshersParty

ticketsCollection = db.tickets

def checkTicketValid(tid:str)->dict:
	try:
		userData = ticketsCollection.find_one({"_id":tid})
	except Exception as e:
		print(f"ERROR => {e}")
		return {"status":500,"message":"Unable to fetch user data"}

	if not userData:
		return {"status":200,"message":{"isValid":False,"message":"Ticket does not exist in database"}}

	if not userData['isValid']:
		return {"status":200,"message":{"isValid":False,"message":"Ticket has already been scanned before."}}

	try:
		ticketsCollection.update_one({"_id":tid},{"$set":{"isValid":False}})
	except Exception as e:
		print(f"ERROR => {e}")
		return {"status":500,"message":"Unable to fetch user data"}

	return {"status":200,"message":userData}