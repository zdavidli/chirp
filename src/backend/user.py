userID = ""

'''call trainer to start training'''
def startTraining(userList):
	if userID != "":
		userID = len(userList)
		addUser(userID)
		return trainer(userID)

'''use default voice for the user'''
def skipTraining(userList):
	if userID != "":
		userID = len(userList)	
		addUser(userID)
		return trainer(userID, default = true)