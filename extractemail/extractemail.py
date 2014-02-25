#############################################
# extractemail

# extracts email messages from text files and writes them into XML records with fielded metadata.

# assumptions:
# input is a file or list of files which must be text format
# output is named for the original but .xml
# metadata comes first, at most one field per line, denoted :
# no attempt to handle xml entities etc which may be problematic for 'correct' xml

import sys
import os
import argparse
import glob

#############################################
# main

def main(argv):

    # parse any command-line arguments
    parser = argparse.ArgumentParser(description="Extracts email messages from text files and writes them into XML records with fielded metadata.")
    parser.add_argument('file', help="filename to extract email from, or wildcard to process multiple files")
    args = parser.parse_args()

    # check for an input sFile
    if args.file:
        sArgs = args.file
    else:
        # no sFile - exit - parser will take care of usage/error reporting
        sys.exit()

    print "extractemail: starting up"

    lstFiles = []
    
    # did we get a single sFile as an argument?
    if os.access(sArgs, os.R_OK):
        # yes
        lstFiles.append(sArgs)
    else:
        # get the list of files
        lstFiles = glob.glob(sArgs)        
   
    for sFile in lstFiles:
            
        print "extractemail: processing:", sFile, 
        
        try:
            fileInput = open(sFile, "r")
        except Exception, e:
            print "(Error: ", e, ")"
            sys.exit()
        
        if sFile.endswith('.txt'):
            sOutputFilename = sFile.replace('.txt', '') + ".xml"
        else:
            sOutputFilename = sFile + ".xml"
        
        print "->", sOutputFilename 
    
        try:
            fileOutput = open(sOutputFilename, "w")
        except Exception, e:
            print "(Error: ", e, ")"
            sys.exit()
            
        # starting tag
        tmpString = "<document>\n"
        fileOutput.write(tmpString)
    
        # initialize
        ln = ""
        sBody = ""
        sTmp = ""
        
        # tbd lame lame lame
        lstTags =  [ "from", "to", "cc", "subject", "date", "attachments" ]
                     
        while 1:
            ln = fileInput.readline()
            
            if not ln:
                break
    
            # tbd: improve this
            ln = ln.replace("&nbsp;", " ")
            ln = ln.replace(">", "")
            ln = ln.replace("<", "")
            ln = ln.replace("&", "&amp;")

            lstLn = ln.split()
            
            tagFound = ""
            sValue = ""
            sTmp = ""
            
            for term in lstLn:

                # for each term in the line...
                
                # do we have a tag?
                if tagFound != "":
                    # we have a tag, save next argument
                    if tagFound in ("to", "from", "cc"):
                        if term.find("@") > -1:
                            sValue = term
                    else:
                        # a crude approximation
                        sValue = sValue + term + " "
                # end if

                for tag in lstTags:
                    # does it match a tag?
                    if term.lower().find(tag.lower() + ":") > -1:
                        # tag found
                        tagFound = tag
                        break
                    # end if
                # end for
                if not tagFound:
                    # another crude approximation...
                    sBody = sBody + term + " "
            # end for
            
            # end of line, if we have a tag write it out
            if tagFound:
                # write it out
                sTmp = "<" + tagFound + ">" + sValue.strip() + "</" + tagFound + ">\n"
                fileOutput.write(sTmp)
                # delete it from the taglist - first found wins
                lstTags.remove(tagFound)
                tagFound = ""

        # end while

        sTmp = "<body>" + sBody.strip() + "</body>\n</document>\n"
        fileOutput.write(sTmp)

        fileOutput.close()
        fileInput.close()

        # end while (1)
                
    # end for (sFile)
    
    print "extractemail: processing complete!"

# end main

#############################################

if __name__ == "__main__":
    main(sys.argv)
    
# end extractemail module