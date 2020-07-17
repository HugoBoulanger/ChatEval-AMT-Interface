import boto3
import sys
import xmldict
from aws_credentials import *


def bonus(WorkerId,AssignmentId,BonusAmount):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	mturk.send_bonus(
		WorkerId=WorkerId,
		AssignmentId=AssignmentId,
		BonusAmount=BonusAmount,
		Reason="Thank you for your time")
	
def create_qual(WorkerId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	#create a qulaification
	qualification = mturk.create_qualification_type(
		Name="Patient", 
		Keywords="waiting",
		Description="We wanted to compensate you for what you did and your time",
		QualificationTypeStatus="Active")
	#assign the qualification
	mturk.associate_qualification_with_worker(
		QualificationTypeId=qualification['QualificationType']['QualificationTypeId'],
		 WorkerId=WorkerId)
	#print out the qualification when you create it the first time
	print("Created Qualification: " 
		+ qualification['QualificationType']['QualificationTypeId'])

def give_qual(WorkerId, QualificationTypeId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	#assign the created qualification to workers
	mturk.associate_qualification_with_worker(
		QualificationTypeId=QualificationTypeId,
		WorkerId=WorkerId)
	print("Qualification given")


def remove_qual(WorkerId, QualificationTypeId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	mturk.disassociate_qualification_from_worker(
		QualificationTypeId=QualificationTypeId,
		WorkerId=WorkerId)
	print("Qualification removed")

def check_qual():
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	#get the list of workers that you assigned the qualification to 	
	list = mturk.list_workers_with_qualification_type(
		QualificationTypeId='3A9QRABHWAIOMHBW26M0ZG8AWWNI2Q',
		Status='Granted',
		MaxResults=10)
	print(list)

def dummy_hit():
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	task = open(
		file='/Users/damiomitaomu/Documents/Mturk/templates/dummy_hit.xml',
		mode='r').read()
	new_hit = mturk.create_hit(
	Title = 'Q&A',
	Description = 'Anser the question',
	Keywords = 'question, answer',
	Reward = '3.00',
	MaxAssignments = 9,
	LifetimeInSeconds = 604800,
	AssignmentDurationInSeconds = 1200,
	AutoApprovalDelayInSeconds = 60,
	QualificationRequirements = [{
	'QualificationTypeId':'3A9QRABHWAIOMHBW26M0ZG8AWWNI2Q',
	'Comparator':'Exists',
	'RequiredToPreview':True}],
	Question = task)
	print("https://worker.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
	print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
	with open(id_file_name,'w') as f:
		f.write("%s\n" % new_hit['HIT']['HITId'])
	with open(link_file_name,'w') as f:
		f.write("%s\n" % new_hit['HIT']['HITGroupId'])


def get_results():
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	if worker_results['NumResults'] > 0:
		for assignment in worker_results['Assignments']:
			xml_doc = xmltodict.parse(assignment['Answer'])
			print("WorkerID: " + assignment['WorkerId'] + "\nAssignmentId: " 
				+ assignment['AssignmentId'])
			if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
				# Multiple fields in HIT layout
				for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
					print("For input field: " + answer_field['QuestionIdentifier'])
					print("Submitted answer: " + answer_field['FreeText'])
			else:
				# One field found in HIT layout
				print("For input field: " 
					+ xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
	else:
		print("No results ready yet")

def balance():
	region_name = 'us-east-1'
	endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

	mturk = boto3.client(
	    'mturk',
	    endpoint_url=endpoint_url,
	    region_name=region_name,
	    aws_access_key_id = AWS_ACCESS_KEY,
	    aws_secret_access_key = AWS_SECRET_KEY,
	)

	# This will return the balance in the account
	print(mturk.get_account_balance()['AvailableBalance'])

def approve(AssignmentId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk', 
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	mturk.approve_assignment(AssignmentId=AssignmentId,OverrideRejection=False)
	print("Approved")


def reject(AssignmentId, RequesterFeedback):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk', 
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	mturk.reject_assignment(AssignmentId=AssignmentId,RequesterFeedback=RequesterFeedback)
	print("Rejected")


def delete(HITId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk', 
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	mturk.delete_hit(HITId=HITId)

def assignment(AssignmentId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk', 
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	mturk.get_assignment(AssignmentId=AssignmentId)

def hit_info(HITId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk', 
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	mturk.get_hit(HITId=HITId)

def results(HITId):
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk', 
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')
	print(mturk.list_assignments_for_hit(
		HITId=HITId,
		AssignmentStatuses=['Approved']))

def survey_hit():
	MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	mturk = boto3.client(
		'mturk',
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		region_name ='us-east-1')



if __name__=="__main__":
	#To send a bonus to a worker (workerId, assignmentID, bonus amount)
	#bonus(sys.argv[1],sys.argv[2],sys.argv[3])

	#create and assign a qualification to a worker (workerID)
	#create_qual(sys.argv[1])

	#assign an existing qualification to a worker (workerID, qualificationtype)
	#give_qual(sys.argv[1],sys.argv[2])

	#remove a qualification from a worker (workerID, qualificationtype)
	#remove_qual(sys.argv[1],sys.argv[2])

	#check what workers have a qualification
	#check_qual()

	#post a dummy hit
	#dummy_hit()

	#get the results from the HIT
	#get_results()

	#approve assignment
	# approve()

	#reject assignment
	# reject()

	#delete HIT
	#delete(sys.argv[1])

	#get assignment information
	# assignment(sys.argv[1])

	#get the HIT info
	# git_info(sys.argv[1])

	#get the results from a HIT
	results(sys.argv[1])

	#launch the survey hit
	# survey_hit()




