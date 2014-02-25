===========
extractemail
===========

This python script extracts email messages from text files and writes them into XML records with fielded metadata.

Usage
-----

	extractemail.py files

Arguments
---------

files: path to one or more text files containing email messages, optionally wildcarded

-h, --help: show usage, and exit

Assumptions
-----------

- Metadata is assumed to come first, one item per line, delimited with a colon
- Only addresses in the form user@host.com are extracted at this time
