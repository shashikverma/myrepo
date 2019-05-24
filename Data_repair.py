import sys
import os
import socket,time
import xml.etree.ElementTree as ET

HOST = '127.0.0.1'
PORT = 10011

read_msisdn = []

def ReadMSISDN():
    os.chdir('C:\\Ericsson\\Ericsson Docs\\Scripts\\Python')
#    read_msisdn = []
    with open('msisdn.txt', 'r') as f:
      print("Starting MSISDN Read")
      for line in f:
        line = line.strip()
        read_msisdn.append(line)
    f.close()
    print("Finished reading ")

def PrintMSISDN():
  print("Start printing MSISDN")
  for lines in read_msisdn:
    print(lines)
  print("Finished print")

def MessageHeader():
        print("Message creation")
        messageHeader='''POST /Air HTTP/1.1
Content-Length: 841
Content-Type: text/xml
Connection: keep-alive
Date: Fri, 01 Jun 2018 13:55:39 CLT
Host: ''' + HOST + ''':''' + str(PORT) + '''
User-Agent: UGw Server/5.0/1.0
Authorization: Basic ZmRzdXNlcjpmZHN1c2Vy''' + "\n"
        return messageHeader

def GetAccDetailCreateMessage():
        for msisdn in read_msisdn:
            message= '''
<?xml version="1.0" encoding="utf-8"?>
<methodCall>
<methodName>GetAccountDetails</methodName>
<params>
 <param>
  <value>
   <struct>
    <member>
     <name>originNodeType</name>
     <value>
      <string>EXT</string>
     </value>
    </member>
    <member>
     <name>originHostName</name>
     <value>
      <string>virtualUATcom</string>
     </value>
    </member>
    <member>
     <name>originTransactionID</name>
     <value>
      <string>2018060322065160</string>
     </value>
    </member>
    <member>
     <name>originTimeStamp</name>
     <value>
      <dateTime.iso8601>20180603T22:06:51+0200</dateTime.iso8601>
     </value>
    </member>
    <member>
     <name>subscriberNumber</name>
     <value>
      <string>''' + msisdn + '''</string>
     </value>
    </member>
   </struct>
  </value>
 </param>
</params>
</methodCall>
'''
            stream = MessageHeader() + message
            SendandReceiveMessage(stream)
            #cProfile.run(SendandReceiveMessage())
        #print("Finished message creation")

def SendandReceiveMessage(message):
    print("Message to be sent =>" + "\n" + message)
    print("\n" + "Length of message =>" + str(len(message)))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Failed to create socket")
        sys.exit()
    print("Socket Created")
    print("Connecting to host: " + HOST + " at port: " + str(PORT))
    try:
        s.connect((HOST,PORT))
    except socket.error:
        print("Failed to connect to server")
        sys.exit()
    print("Connected to server")
    try:
        s.send(message.encode('utf-8'))
    except socket.error:
        print("Send Failed")
        sys.exit()
    print("Sent message to server")
    print("Waiting for response from server")
    begintime = time.time()
    respData = ''
    i = 1
    while 1:
        rcvdata = s.recv(7168)
        print("Receive loop count " + str(i))
        if not rcvdata:
            break
        else:
            respData = respData + rcvdata.decode()
            i += 1
            
    endtime = time.time()
    responseTime = endtime - begintime
    print("Received message from server in =>" + str(responseTime) + " sec")
    print("Length of received data =>" + str(len(respData)))
    s.close()
    print("Received data " + respData)
    tree = ET.parse('response.xml')
    root = tree.getroot()
    found = 0
    for elem in root.iter():
        for subelem in elem.itertext():
            if subelem == 'responseCode':
                found = 1
            elif found == 1:
                print("\nresponseCode," + subelem + '\n')
                break
        break        


#Program starts here
__file__ == "main"

ReadMSISDN()
#PrintMSISDN()

print("Please provide request to be sent" + 
" \n 1. GetAccDetail" + 
" \n 2. UpdateBalanceandDate"
)
option = input()
if int(option) == 1:
  GetAccDetailCreateMessage()
elif int(option) == 2 :
  GetAccDetailCreateMessage()
  UpdateBalanceandDate()
