import string
from array import array

####Caeasar
def caesar_ascii(data,key):
	to=array('c',map(lambda x:chr(x%95+32),range(key,95+key))).tostring()
	table=array('c',map(chr,range(0,32))).tostring() + to + array('c',map(chr,range(127,256))).tostring()
	#print 'DBG: key='+str(key)+'\nto='+to
	
	return data.translate(table)

def caesar_commonLetter(data,key):
	frm=range(ord('A'),ord('Z')+1)+range(ord('a'),ord('z')+1)
	frm=array('c',map(chr,frm)).tostring()
	to=frm[key:]+frm[:key]
	
	#print 'DBG:'+frm+'\nDBG:'+to
	trans=string.maketrans(array('c',frm).tostring(),array('c',to).tostring())
	return data.translate(trans)
	
def caesar_splitLetter(data,key): # original caesar
	frm1=range(ord('A'),ord('Z')+1)
	frm1=array('c',map(chr,frm1)).tostring()
	frm2=range(ord('a'),ord('z')+1)
	frm2=array('c',map(chr,frm2)).tostring()
	frm=frm1+frm2
	to=frm1[key:]+frm1[:key]+frm2[key:]+frm2[:key]
	del frm1,frm2
	#print 'DBG:'+frm+'\nDBG:'+to
	trans=string.maketrans(frm,to)
	return data.translate(trans)

	
	
#to be tested
def caesar_withTransformTableKey(data,key): #XXX maybe make something like split mapping (e.g. only map Letters)
	if len(key)!=256:
		print "Key not long enough (needs to be 256 characters)"
		return 'invalid key'
	else:
		return data.transform(key)
		
		
####Vigenere
# based on caeasar

def vigenere_enc(data,key): #XXX maybe to solve with some kind of dict
	if isinstance(key,str):	
		key=map(lambda x:ord(x)-ord('A'),key.upper())
		cryptext=array('c',data) #XXX probably not the best idea to use plaintext to initialize cryptified text
		print key
		for i in xrange(len(data)):
			cryptext[i]=caesar_splitLetter(data[i],int(key[i%len(key)])) #XXX find out which caesar to use
		return cryptext.tostring()
	else: 
		print "Key must be string"
		return "invalid"

# everything that is no letter will be translated into ' ' and is *NOT* recoverable
def vigenere_enc_book(data,key):
	if isinstance(key,str) and isinstance(data,str):
	
		prepData=lambda x:ord(x)-ord('A') if x.isalpha() else 27
		repairCryptext=lambda x:chr(x+ord('A'))if x<26 else ' '
		
		key=map(prepData,key.upper())
		data=map(prepData,data.upper())
		cryptext=array('c')
		print key
		
		for i in xrange(len(data)):
			cryptext.append(repairCryptext(((data[i]+key[i%len(key)])%27)))
		return cryptext.tostring()
	else:
		print "Key and data must be string"
		return "invalid"
		
def vigenere_dec_book(data,key): #FIXME doesn't work how it should (could also be vigenere_enc_book)
	if isinstance(key,str) and isinstance(data,str):
		
		prepData=lambda x:ord(x)-ord('A')if x.isalpha() else 27
		prepKey=lambda x:chr((27-prepData(x)%27)+ord('A'))
		return vigenere_enc_book(array('c',map(lambda x:chr(prepData(x)+ord('A')),data)).tostring(),array('c',map(prepKey,key)).tostring())
	else:
		print "Key and data must be string"
		return "invalid"
def vigenere_dec(data,key): # FIXME
	if isinstance(key,str):
		key=map(lambda x:ord(x)-ord('A'),key.upper())
		print key
		print '\n'
		key=map(lambda x:chr((-x+26)%26+ord('A')),key) # only works with caesar_splitLetter
		print key
		key=array('c',key).tostring()
		print key
		return vigenere_enc(data,key)
	else: 
		print "Key must be string"
		return "invalid"
	
# returns a table of 256 fields for each possible value
def histogramm(data):
	if isinstance(data,str):
		charTable=string.maketrans('','')
		for i in data:
			charTable[ord(i)]+=1
		return charTable
	else:
		print "data must be string"
		return "invalid"
