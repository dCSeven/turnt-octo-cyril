#!py -2
# FIXME -d requires argument, but shouldn't (ArgumentParser)
# TODO add more choices to the ArgumentParser encryptionMethod
# TODO parse arguments in readParams

from array import array

import argparse
import sys

from encryptionLib import *	# encryption stuff is in encryptionLib.py

encryption=vigenere_enc
decryption=vigenere_dec
#data=array('c',map(chr,range(49,126))).tostring()
data="this is sparta98"

#key=5
key="cxfk go9"

def readParams():
	parser=argparse.ArgumentParser(description='A simple En-/Decryption library')
	parser.add_argument(
		'--plainFile', '-p', nargs='?', default=sys.stdin, type=argparse.FileType('r'),
		help='the plaintextfile to be encoded')
	parser.add_argument(
		'--out', nargs='?', default=sys.stdout, type=argparse.FileType('w'),
		help='the file where the encoded stuff should be written')
	parser.add_argument(
		'encryptionMethod', nargs='?', 
		choices=['caesar_enc', 'caesar_dec', 'vigenere_enc', 'vigenere_dec', 'vernam', 'vernam_h_enc', 'vernam_h_dec'])
	parser.add_argument(
		'-d','--debug', help='Debug') # FIXME requires argument, but shouldn't
	args = parser.parse_args()
#	args.log.write('%s' % sum(args.integers))
#	args.log.close()


def main():
	global encryption,data,key
	readParams()
	#print 'Current data is\n'+data+' with key: '+str(key)
	print 'Key: '+str(key)
	print 'Text:'+data
	enc=encryption(data,key)#.lstrip()
	print 'Enc: '+enc
	print 'Dec: '+decryption(enc,key)
	
main()
raw_input()
