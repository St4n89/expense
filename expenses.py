#!/usr/bin/env python
import csv
import re

groceries = {}
transport = {}
entertainment = {}
others = {}
cars = {}

def dictionarize(file,dictionary):
    dictfile = open(file)
    with dictfile as input:
        for line in input:
            key,value = line.split(":")
            dictionary[key] = value.strip()

def parsing(dictionary):
    with open('output.csv') as input:
        read = csv.reader(input, delimiter=';')
        with open('expenses.csv','a') as output:
            write = csv.writer(output, delimiter=';')
            for row in read:
                sms = row[1]
                for word in dictionary:
                    found = sms.count(word)
                    if found:
                        store = dictionary.get(word)
                        realdate = ((re.search('[0-9][\s][0-9][0-9].[0-9][0-9].[0-9][0-9]', sms)).group(0))
                        date = str((re.search('[0-9][0-9].[0-9][0-9].[0-9][0-9]',realdate).group(0)).replace('.','/'))
                        cost = int(round(float(row[2].replace(',','.'))))
                        write.writerow((store+" "+date, str(cost)))
                    else:
                        exit
            write.writerow(" ")

def formatcsv(filename):
    with open(filename) as input:
        read = csv.reader(input, delimiter=';')
        with open('output.csv','w') as output:
            next(read)
            write = csv.writer(output, delimiter=';')
            for row in reversed(list(read)):
                if row[7]!="0":
                    write.writerow((row[3], row[5], row[7]))

dictionarize('groceries.dic',groceries)
dictionarize('transport.dic',transport)
dictionarize('entertainment.dic',entertainment)
dictionarize('others.dic',others)
dictionarize('cars.dic',cars)
formatcsv('movementList.csv')
parsing(groceries)
parsing(transport)
parsing(entertainment)
parsing(others)
parsing(cars)
