from cbconnect import *


# connecting the class 
client = cbconnect(cbhost="hostname",cbuser="useremail", cbpass="userpass")

# listong the workspaces
client.ListWorkSpaces()

# getting the list of stack with workspace id
client.ListStackWithWid(wid="2")
