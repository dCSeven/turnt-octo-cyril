#!py -2

from array import array

from encryptionLib import *	# encryption stuff is in encryptionLib.py

encryption=vigenere_enc
decryption=vigenere_dec
#data=array('c',map(chr,range(49,126))).tostring()
data="this is sparta98"

#key=5
key="cxfk go95"



def main():
	global encryption,data,key
	#print 'Current data is\n'+data+' with key: '+str(key)
	print 'Key: '+str(key)
	print 'Text:'+data
	enc=encryption(data,key)#.lstrip()
	print 'Enc: '+enc
	print 'Dec: '+decryption(enc,key)
	
main()