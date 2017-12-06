def getArticle():
	text = []
	idx = 1
	with open('article.txt','r') as f:
		data = f.readlines()
		for i in data:
			if i != '\n':
				s = "{ 'id':" + str(idx) + "," + "'text':" + i.rstrip() + " }"  
				text.append(s)
				idx+=1
	return text

a = getArticle()
print a
'''
create a list of 100 words article
use javascript to display those article when start is hit. 
change to the next article
'''


