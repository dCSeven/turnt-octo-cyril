import string
from array import array

####Caeasar
def caesar_enc(data,key): return caesar_splitLetter(data,key)
def caesar_dec(data,key): return caesar_splitLetter(data,-key)

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

def vigenere_enc(data,key):return str(array('c',_vigenere_enc(data,key)).tostring())
def _vigenere_enc(data,key): #XXX maybe to solve with some kind of dict
	if isinstance(key,str):
		key=map(lambda x:ord(x)-ord('A') if x.isalpha() else int(x) if x.isdigit()  else 0,key.upper())	
		for i in xrange(len(data)):
			yield caesar_splitLetter(data[i],int(key[i%len(key)])) #XXX find out which caesar it should use
	else: 
		raise TypeError("Key must be string") #XXX maybe extend to support more than only string

def vigenere_dec(data,key):return str(array('c',_vigenere_dec(data,key)).tostring())	
def _vigenere_dec(data,key): 
	if isinstance(key,str):
		key=map(lambda x:ord(x)-ord('A') if x.isalpha() else int(x) if x.isdigit()  else 0,key.upper()) # if there is a Space (or other thing) don't shift
		key=map(lambda x:chr((-x+26)%26+ord('A')),key) # only works with caesar_splitLetter
		key=array('c',key).tostring()
		return _vigenere_enc(data,key)
	else: 
		raise TypeError("Key must be string")
		
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


#### RC4
# key_len:1<=k<=256Byte typ:5<=k<=16
class rc4_pn_gen:
	li=map(int,range(0,256))
	i=j=0
	def __init__(self,key):
		self.perm(map(ord,key)) # don't store the key (security stuff)
	def __iter__(self):
		return self
	def perm(self,key):
		self.j=0
		for i in xrange(0,256):
			self.j=(self.j+self.li[i]+key[i%len(key)])%256
			self.li[i],self.li[self.j]=self.li[self.j],self.li[i]	# swap li[i] and li[j]
		self.i=self.j=0
	def next(self):
		self.i=(self.i+1)%256
		self.j=(self.j+self.li[self.i])%256
		try:return self.li[(self.li[self.i]+self.li[self.j])%256]
		finally:self.li[self.i],self.li[self.j]=self.li[self.j],self.li[self.i]
		
def rc4_enc(data,key):
	if len(key)<1 or len(key)>=256: raise ValueError("len(key) must be anywhere in between 1 and 256") 
	rc4_png=rc4_pn_gen(key)
	del key # security stuff
	li=list()
	if isinstance(data,str):data=map(ord,data)
	for i in data:
		li.append(i^rc4_png.next())
	return li

rc4_dec=rc4_enc

def rc4_enc_iter(data,key):
	rc4_png=rc4_pn_gen(key)
	del key
	for i in data:
		yield i^rc4_png.next()

rc4_dec_iter=rc4_enc_iter

#### A5/1

class a5_pn_gen:
	def __init__(self,key):raise NotImplementedError()
	def __iter__(self):
		return self
	def perm(self,key):pass
	def next(self):pass

def a5_enc(data,key):
	if len(key)<1 or len(key)>=256: raise ValueError("len(key) must be anywhere in between 1 and 256") 
	a5_png=a5_pn_gen(key)
	del key # security stuff
	li=list()
	for i in data:
		li.append(i^a5_png.next())
	return li

a5_dec=a5_enc

def a5_enc_iter(data,key):
	a5_png=a5_pn_gen(key)
	del key
	for i in data:
		yield i^a5_png.next()

a5_dec_iter=a5_enc_iter
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


#### Tools

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

# subtracts the srings (only the letters)
# if the strings don't have the same size the shorter will be padded with A (means Zero)
def subtractStrings(minuend,subtrahend):
	if isinstance(minuend,str) and isinstance(subtrahend,str):
		length=len(minuend)-len(subtrahend)
		if(length<0): #subtrahend longer
			minuend+=''.zfill(-length)
		elif(length>0):#minuend longer
			subtrahend+=''.zfill(-length)
		return map(lambda x,y:ord(x)-ord(y) if isinstance(x,str) and isinstance(y,str) else 0,minuend,subtrahend)
		# TODO  add check if it is a letter and maybe add 'A' and call chr
	else:
		print "both parameters must be strings"
		return "invalid"
