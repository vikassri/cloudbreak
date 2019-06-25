from cbconnect import *


# connecting the class 
client = cbconnect(cbhost="hw-cb-dev01.us-east4.us.walmart.net",cbuser="hw-cb-hadoop@wal-mart.com", cbpass="3DLC3DLP")

# listong the workspaces
client.ListWorkSpaces()

# getting the list of stack with workspace id
client.ListStackWithWid(wid="2")
