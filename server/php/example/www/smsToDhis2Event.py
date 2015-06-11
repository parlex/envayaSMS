import os, json, sys, urllib2, urllib, cookielib

message = sys.argv[1]
baseUrl = 'https://apps.dhis2.org/dev/api/'

#TODO: make this the phoneNumber that is sending the text

phoneNum = '94238318'

def processMessage(msg):
   nums = msg.strip().split(':')[0].split('of')
   appendMessage(message.split('of' + nums[1] + ":")[1], nums[0])

   if str(allFilesCreated()) ==  nums[1]:
       concatFiles(int(nums[1]))

def allFilesCreated():
    print len(os.listdir(phoneNum))
    return len(os.listdir(phoneNum))

def concatFiles(amount):
   with open(phoneNum + '/output.txt', 'w+') as outfile:
       for fname in range(1, amount+1):
           with open(phoneNum + '/' + str(fname)) as infile:
               outfile.write(infile.read())
   parseMessage(open(phoneNum + '/output.txt', 'r+').read())

def appendMessage(msg, num):
   if not os.path.exists(phoneNum):
       os.makedirs(phoneNum)
   storeMessage = open(phoneNum + '/' + num, 'a')
   storeMessage.write(msg)
   storeMessage.close()
   
def parseMessage(msg):
   smsDict = dict(item.split('=') for item in msg.strip().split(':')) 
   dataElms = dict(item.split('!') for item in smsDict['d'].strip().split(','))
   del smsDict['d']

   buildJson(smsDict, dataElms)

def getValueFromNumber(dataID, number):
   saveAs = 'temp.json'
   apiType = 'dataElements/'
   login = " -u admin:district -v >> "

   cmd =  "curl '" + baseUrl + apiType + dataID + ".json" + "'" + login + saveAs
   os.system(cmd)
   
   with open(saveAs) as data_file:
      data = json.load(data_file)

   os.remove(saveAs)
   
   if not data.get('optionSet'):
     return None
   else:
      cmd =  "curl '" + data['optionSet']['href']+ '.json' + "'" + login + saveAs
      os.system(cmd)
      
      with open(saveAs) as data_file:
         data = json.load(data_file)
         
      os.remove(saveAs)

   return data['options'][number]['name']


def buildJson(eventData, dataElements):
   data = {}
   tmp = {}
   dataVals = []

   data['orgUnit'] = eventData['o']
   data['eventDate'] = eventData['eD'] 
   data['status'] = 'COMPLETED' 
   data['storedBy'] = eventData['o'] 
   data['program'] = eventData['p'] 

   for key in dataElements:
      value = getValueFromNumber(key, number)
      if value is None:
         tmp['value'] = dataElements[key]
      else:
         tmp['value'] = value
      tmp['dataElement'] = key
      tmp['providedElsewhere'] = 'false'
      dataVals.append(tmp)
      tmp = {}
   
   data['dataValues'] = dataVals
   data['eventDate'] = eventData['eD']
   data['dueDate'] = eventData['dD']
   data['programStage'] = eventData['ps']

   storeValues = open('testPost.json', 'w+')
   storeValues.write(json.dumps(data))
   storeValues.close()
   
   os.system("curl -d @testPost.json 'https://apps.dhis2.org/dev/api/events' -H 'Content-Type:application/json' -u android:Android123 -v")

   os.remove('testPost.json')


processMessage(message)
