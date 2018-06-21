from twilio.rest import Client
from consts import *

"""
This is a file containing a function that sends a text when called.

The file can be imported into any script/program so a function that
sends a text does not need to be defined each time.
"""

def sendText(text, sender, recipient):
	"""
	This is the function that sends a text to a cell number.

	Parameter text: A string containing the message that is going
		to be sent in the body of the text.

	Parameter sender: A string containing the phone number that the
		text will be sent from. ** MUST be a Twilio number **

	Parameter recipient: A string containing the phone number that
		the text will be sent to. ** MUST be a registered number 
		with Twilio **
	"""

	# Creates a Twilio Client to using account SID and the
	# authentication token
	tCli = Client(ACCOUNT_SID, AUTH_TOKEN)

	# Creates a message with a body of text to be sent from the
	# sender to the recipient
	message = tCli.messages.create(body=text,from_=sender,\
		to=recipient)