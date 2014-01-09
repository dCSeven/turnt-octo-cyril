#!py -2

from array import array

from encryptionLib import *	# encryption stuff is in encryptionLib.py

encryption=vigenere_enc_book
decryption=vigenere_dec_book
data=array('c',map(chr,range(49,126))).tostring()

key="abcde" # means shift the alphabet 5 to the right


	
def main():
	global encryption,data,key
	print 'Current data is\n'+data+' with key: '+str(key)
	print 'Text:'+data
	enc=encryption(data,key).lstrip()
	print 'Enc: '+enc
	print 'Dec: '+decryption(enc,key)
	
main()