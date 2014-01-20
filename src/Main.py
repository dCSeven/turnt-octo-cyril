#!py -2

from array import array

from encryptionLib import *	# encryption stuff is in encryptionLib.py

encryption=vernam_enc
decryption=vernam_dec
#data=array('c',map(chr,range(49,126))).tostring()
data="this is sparta"

#key=5
key="cxfk go"



def main():
	global encryption,data,key
	print 'Current data is\n'+data+' with key: '+str(key)
	print 'Text:'+data
	enc=encryption(data,key)#.lstrip()
	print 'Enc: '+enc
	print 'Dec: '+decryption(enc,key)
	
main()