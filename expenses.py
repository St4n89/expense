#!/usr/bin/env python
import csv
import re
import sys


def checkinput():
    if len(sys.argv) > 1:
        run = 1
        return run
    else:
        print("Please specify input files!")
        run = 0
        return run


def dictionarize(file, dictionary):
    dictfile = open(file)
    with dictfile as input_file:
        for line in input_file:
            key, value = line.split(":")
            dictionary[key] = value.strip()


def parsing_alfa(dictionary):
    with open('output.csv') as input_file:
        read = csv.reader(input_file, delimiter=';')
        with open('expenses.csv','a') as output_file:
            write = csv.writer(output_file, delimiter=';')
            for row in read:
                sms = row[1]
                for word in dictionary:
                    found = sms.count(word)
                    if found:
                        store = dictionary.get(word)
                        realdate = ((re.search('[0-9][\s][0-9][0-9].[0-9][0-9].[0-9][0-9]', sms)).group(0))
                        date = str((re.search('[0-9][0-9].[0-9][0-9].[0-9][0-9]', realdate).group(0)).replace('.', '/'))
                        cost = int(round(float(row[2].replace(',', '.'))))
                        write.writerow((store + " " + date, str(cost)))
                    else:
                        exit
            write.writerow(' ')


def parsing_citi(dictionary):
    with open(sys.argv[1]) as input_file:
        read = csv.reader(input_file, delimiter=',')
        with open('expenses.csv', 'a') as output:
            write = csv.writer(output, delimiter=';')
            for row in reversed(list(read)):
                sms = row[1]
                for word in dictionary:
                    found = sms.count(word)
                    if found:
                        store = dictionary.get(word)
                        date = row[0]
                        cost = int(round(float(row[2].replace('-', ''))))
                        write.writerow((store + " " + date, str(cost)))
                    else:
                        exit
            write.writerow(' ')


def formatcsv(filename):
    with open(filename) as input_file:
        read = csv.reader(input_file, delimiter=';')
        with open('output.csv', 'w') as output:
            next(read)
            write = csv.writer(output, delimiter=';')
            for row in reversed(list(read)):
                if row[7] != "0":
                    write.writerow((row[3], row[5], row[7]))

def execute(run):
    if run == 1:
        bank = sys.argv[2]

        groceries = {}
        transport = {}
        entertainment = {}
        others = {}
        cars = {}
        living = {}
        clarifications = {}

        dictionarize('groceries.dic', groceries)
        dictionarize('transport.dic', transport)
        dictionarize('entertainment.dic', entertainment)
        dictionarize('others.dic', others)
        dictionarize('cars.dic', cars)
        dictionarize('living.dic', living)
        dictionarize('clarifications.dic', clarifications)

        if bank == 'citi':
            parsing_citi(groceries)
            parsing_citi(transport)
            parsing_citi(entertainment)
            parsing_citi(others)
            parsing_citi(cars)
            parsing_citi(living)
            parsing_citi(clarifications)
        else:
            if bank == 'alfa':
                formatcsv(sys.argv[1])
                parsing_alfa(transport)
                parsing_alfa(groceries)
                parsing_alfa(entertainment)
                parsing_alfa(others)
                parsing_alfa(cars)
                parsing_alfa(living)
                parsing_alfa(clarifications)
            else:
                print("Incorrect BANK parameter")
                exit
    else:
        exit


execute(checkinput())
