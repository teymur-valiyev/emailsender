import csv
import os

def getRecipients():
	data = []
	try:
		with open(os.path.join('config', 'recipients.csv'), 'rt') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:					
				data.append(row)
	except Exception as e:
		raise
	
	return data

def getEmailBody():
	data = ''
	try:
		with open(os.path.join('config','email_body.txt'),) as emailBody:
			data = emailBody.read()					
	except Exception as e:
		raise

	return data

def getAttachments():
	attachments = [] 
	for attachment in os.listdir('attachments'):
		attachments.append(os.path.join('attachments', attachment))
		
	return attachments