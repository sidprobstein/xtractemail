===========
extractemail
===========

This python script reads email messages from text files and writes them into XML records with fielded metadata. 

Usage
-----

python extractemail.py file
	

Arguments
---------

file: the full path to the input text file


Notes
-----

- Metadata is assumed to come first, one item per line, delimited with a colon
- Only addresses in the form user@host.com are extracted at this time
