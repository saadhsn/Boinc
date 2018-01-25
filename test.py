#!/usr/bin/python

"""
Application - Intermediate code 

Simple python string to query database and retrieve data. Also handles some 
simple bash functions for Debian (8.9 Jessie) .

"""

__author__ = "Saad Hussain"
__email__ =  "saad.hussain@itu.edu.pk"
__status__ = 'Development'
__version__ = "0.0.1"

import MySQLdb
import csv
import subprocess
import os

#connection string for database @localhost
db = MySQLdb.connect("localhost",            # hostname    
                     "pitb",                 # username
                     "greentree",            # password
                     "agriculturedata")      # database name

#creates a cursor object to execute sql queries
cur = db.cursor() 
cur.execute("select * from sample_infoo")
data = cur.fetchall ()

# filePath to be deleted once shiped to boinc dir
filePath=None


def genSiganturesCsv(dbcursor) :
    for row in data :
        with open('signatures.csv', 'a') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(row)


def shellGetOutput(str) :
    process = subprocess.Popen(str,shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    output, err =process.communicate()

    if (len(err) > 0):
        raise NameError (str+"\n"+output+err)
    return output


def sendInputFiles(homeDir) :
    #home directory of a sample project on user os
    boincDir=homeDir+"/projects/cplan"
    inputDir=homeDir+"/Desktop"
    comString="cp"+" "+inputDir+"/signatures.csv"+ " " +boincDir
    shipFiles=shellGetOutput(comString)
    global filePath
    filePath=inputDir+"/signatures.csv"  # generated signatures.csv file to be deleted after shipped to boinc  
    

def deleteFile(path):
    os.remove(path)



#generates signatures.csv from database for boinc input
genSiganturesCsv(data)
#retrieve home diretory of user
homeDir=os.getenv("HOME")
#ships input files to boinc direcotry
sendInputFiles(homeDir)
deleteFile(filePath)








        