import string
from array import array

####Caeasar
def caesar_ascii(data,key):
	if isinstance(key,str):
		try:
			key=int(str)
		except exceptions.ValueError:pass #TODO
			
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
		
####Rot13

def rot13(data): return caesar_splitLetter(data,13)
def rot12(data): return data.encode('rot13')
		
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
	
		prepData=lambda x:ord(x)-ord('A') if x.isalpha() else 26
		repairCryptext=lambda x:chr(x+ord('A'))if x<26 else ' '
		
		key=map(prepData,key.upper())
		data=map(prepData,data.upper())
		cryptext=array('c')
		
		print 'KEY: '+str(key)
		print 'DATA:'+str(data)
		
		for i in xrange(len(data)):
			cryptext.append(repairCryptext(((data[i]+key[i%len(key)])%27)))
		return cryptext.tostring()
	else:
		print "Key and data must be string"
		return "invalid"


def vigenere_dec_book(data,key): #FIXME doesn't work how it should (could also be vigenere_enc_book)
	if isinstance(key,str) and isinstance(data,str):
		
		prepData=lambda x:ord(x)-ord('A')if x.isalpha() else 26
		prepKey=lambda x:chr(((27-prepData(x))%27)+ord('A'))
		return vigenere_enc_book(array('c',map(lambda x:chr(prepData(x)+ord('A')),data.upper())).tostring(),array('c',map(prepKey,key.upper())).tostring())
	else:
		print "Key and data must be string"
		return "invalid"
		
		
# everything that is no letter will be trimmed
def vigenere_enc_book26(data,key):
	if isinstance(key,str) and isinstance(data,str):
	
		prepData=lambda x:ord(x)-ord('A') if x.isalpha() else 25
		repairCryptext=lambda x:chr(x+ord('A'))if x<26 else 'Z'
		
		key=map(prepData,key.upper())
		data=map(prepData,data.upper())
		cryptext=array('c')
		
		print 'KEY: '+str(key)
		print 'DATA:'+str(data)
		
		for i in xrange(len(data)):
			cryptext.append(repairCryptext(((data[i]+key[i%len(key)])%26)))
		return cryptext.tostring()
	else:
		print "Key and data must be string"
		return "invalid"


def vigenere_dec_book26(data,key): #FIXME doesn't work how it should (could also be vigenere_enc_book)
	if isinstance(key,str) and isinstance(data,str):
		prepData=lambda x:ord(x)-ord('A')if x.isalpha() else 25
		prepKey=lambda x:chr(((-prepData(x)+26)%26)+ord('A')) #XXX why 26 + 6????
		return vigenere_enc_book26(array('c',map(lambda x:chr(prepData(x)+ord('A')),data.upper())).tostring(),array('c',map(prepKey,key.upper())).tostring())
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
	

####Vernam
# clean vernam en-/decryption (without anything other)
def vernam(data,key):return array('c',_vernam(data,key)).tostring()
# vernam en-/decryption 
def _vernam(data,key):
	if type(data)!=type(key):
		print "Key must have the same type as data"
		return #"invalid"
	if isinstance(data,str):vern=lambda x,y: chr(ord(x)^ord(y))
	elif isinstance(data,int):vern=lambda x,y: x^y	#XXX totest
	else:
		print "vernam for {} not defined yet".format(type(data))
		return #"invalid"
	
	for i in xrange(len(data)):
		yield vern(data[i],key[i%len(key)])

# encrypts with vernam (and encodes with base64 to make it printable)
def vernam_enc(data,key):return vernam(data,key).encode('base64')

# encrypts with vernam (and decodes from base64)
def vernam_dec(data,key):return vernam(data.decode('base64'),key)
#XXX maybe compress before encryption to make more secure (*but* the header is identifiable (therefore must be cut))



####Random (selfmade)
import random

def rand_enc(data,key):
	if(isinstance(key,int)):  random.seed(key)
	elif(isinstance(key,chr)):random.seed(ord(chr))
	else:
		print "Key must be int"
		return "invalid"
	random.shuffle(data) # change to something more reproduceable
	return data
	
def rand_dec(data,key):
	return 'not_done_yet'