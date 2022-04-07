#!/usr/bin/env python3
#Hanna Prince 225292 Lab5

import datetime
import hashlib
import json
import os

#Returns records dict: containing files (with full path) and their associated hashes and date/time observed.
def makeRecord():
    print("Walking through file system...")
    record = {}
    for root, dirs, files in os.walk("/"):
        for f in files:
            fullPath = os.path.join(root, f)
            time = str(datetime.datetime.now())
            if(checkSkip(fullPath)):
                 #print(fullPath, " skipped")
                 continue
            #print(fullPath)
            hash = hashFile(fullPath)
            record[fullPath] = (hash, time)
            #print("File: ", fullPath, "; hash: ", hash, "; at time: ", time)
    print("...walk complete.")
    return record

#Checks if the file or directory should be skipped.
def checkSkip(name):
    ignore =  ["/dev", "/proc", "/run", "/sys", "/tmp", "/var/lib", "/var/run", "/swapfile"]#, "etc/pulse/client.conf.d/01-enable-autospawn.conf", "/etc/network/if-post-down.d/avahi-daemon"] #"/dev/loop8", "/dev/vcsa6"]
    for i in ignore:
        if i in name:
            return True
    return False

#Compare two records and prints any differences.
def compareRecords(new, old):
    print("Comparing storage files for differences...")
    for n in new.keys():
        if n not in old.keys():
            print("File added: ", n, ".")
        elif new[n][0] != old[n][0]:
            print("File modified: ", n, ".")
    for o in old.keys():
        if o not in new.keys():
            print("File removed: ", o, ".")
    print("...comparison done.")

#Returns stored records dict read from file
#Resource: https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
def readRecord(storageFile):
    print("Reading in storage file...")
    f = open(storageFile)
    record = json.load(f)
    f.close()
    print("...storage file read.")
    return record

#Stores the record in the designated file, in json format.
#Resource: https://pythonspot.com/save-a-dictionary-to-a-file/
def writeRecord(record, storageFile):
    print("Writing storage file...")
    j = json.dumps(record)
    f = open(storageFile, "w")
    f.write(j)
    f.close()
    print("...storage file ", storageFile, " successfully updated at: ", datetime.datetime.now())

#Returns hashed contents of given file (hash digest).
#Resources: https://docs.python.org/3/library/hashlib.html?highlight=hashlib#module-hashlib
#           https://www.programiz.com/python-programming/exception-handling
#
def hashFile(path):
    contents = ""
    try:
        file = open(path, 'rb')
        contents = file.read()
        file.close()
    except:
        contents = b'Some sort of error, most likely file not found Errno2'

    h = hashlib.new('sha256')
    h.update(contents)
    return h.hexdigest()

if __name__=='__main__':
    newRecord = makeRecord()
    try:
        oldRecord = readRecord("lab5.log")
        compareRecords(newRecord, oldRecord)
    except:
        print("Old log does not exist.")
    writeRecord(newRecord, "lab5.log")
