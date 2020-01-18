#!/usr/bin/env python
import csv
import re
import sys
import os
import datetime
import calendar

gettime = datetime.datetime.now()
month_now = calendar.month_abbr[gettime.month]
timestamp = str(str(gettime.day)+"-"+str(month_now)+"-"+str(gettime.year))
out_filename_alfa = str("Alfabank "+timestamp+".csv")
out_filename_citi = str("Citibank "+timestamp+".csv")

if os.path.isfile('output.csv'):
    os.remove('output.csv')


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
    expenses_lines = []
    removals = []

    with open('output.csv') as input_file:
        read = csv.reader(input_file, delimiter=';')
        fin_file = open(out_filename_alfa,'a')

        for row in read:
            expenses_rows = [row[0],row[1],row[2]]
            expenses_lines.append(expenses_rows)

        for str_num in range(len(expenses_lines)):
            sms = expenses_lines[str_num][1]
            for word in dictionary:
                found = sms.count(word)
                if found:
                    store = dictionary.get(word)
                    realdate = ((re.search('[0-9][\s][0-9][0-9].[0-9][0-9].[0-9][0-9]', sms)).group(0))
                    expdate = str((re.search('[0-9][0-9].[0-9][0-9].[0-9][0-9]', realdate).group(0)).replace('.', '/'))
                    cost = int(round(float(expenses_lines[str_num][2].replace(',', '.'))))
                    fin_file.write((store+" "+expdate+";"+str(cost)+"\n"))
                    removals.append(str_num)

    removals.sort(reverse=True)
    expenses_copy = list(expenses_lines)

    for rem_str_num in range(len(removals)):
        expenses_copy.pop(removals[rem_str_num])

    os.remove('output.csv')
    temp_file = open('output.csv','a')
    for fin_str_num in range(len(expenses_copy)):
        temp_file.write((expenses_copy[fin_str_num][0]+";"+expenses_copy[fin_str_num][1]+";"+expenses_copy[fin_str_num][2]+"\n"))

    fin_file.write("\n")


def parsing_citi(dictionary):
    expenses_lines = []
    removals = []

    with open('output.csv') as input_file:
        read = csv.reader(input_file, delimiter=';')
        fin_file = open(out_filename_citi,'a')

        for row in read:
            expenses_rows = [row[0],row[1],row[2]]
            expenses_lines.append(expenses_rows)

        for str_num in range(len(expenses_lines)):
            sms = expenses_lines[str_num][1]
            for word in dictionary:
                found = sms.count(word)
                if found:
                    store = dictionary.get(word)
                    expdate = expenses_lines[str_num][0]
                    cost = int(round(float(expenses_lines[str_num][2].replace('-', ''))))
                    fin_file.write((store+" "+expdate+";"+str(cost)+"\n"))
                    removals.append(str_num)

    removals.sort(reverse=True)
    expenses_copy = list(expenses_lines)

    for rem_str_num in range(len(removals)):
        expenses_copy.pop(removals[rem_str_num])

    os.remove('output.csv')
    temp_file = open('output.csv','a')
    for fin_str_num in range(len(expenses_copy)):
        temp_file.write((expenses_copy[fin_str_num][0]+";"+expenses_copy[fin_str_num][1]+";"+expenses_copy[fin_str_num][2]+"\n"))

    fin_file.write("\n")


def formatcsv_alfa(filename):
    with open(filename) as input_file:
        read = csv.reader(input_file, delimiter=';')
        with open('output.csv', 'w') as output:
            next(read)
            write = csv.writer(output, delimiter=';')
            for row in reversed(list(read)):
                hold_status = row[4]
                found_hold = hold_status.count("HOLD")
                if row[7] != "0":
                    if found_hold:
                        write.writerow((row[3], ("00 "+str(row[3])+" "+str(row[5])), row[7]))
                    else:
                        write.writerow((row[3], row[5], row[7]))


def formatcsv_citi(filename):
    with open(filename) as input_file:
        read = csv.reader(input_file, delimiter=',')
        with open('output.csv', 'w') as output:
            write = csv.writer(output, delimiter=';')
            for row in reversed(list(read)):
                if float(row[2]) <= "0":
                    write.writerow((row[0], row[1], row[2]))


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
        medicine = {}

        dictionarize('groceries.dic', groceries)
        dictionarize('transport.dic', transport)
        dictionarize('entertainment.dic', entertainment)
        dictionarize('others.dic', others)
        dictionarize('cars.dic', cars)
        dictionarize('living.dic', living)
        dictionarize('clarifications.dic', clarifications)
        dictionarize('medicine.dic', medicine)

        if bank == 'citi':
            if os.path.isfile(out_filename_citi):
                os.remove(out_filename_citi)
                
            formatcsv_citi(sys.argv[1])
            parsing_citi(groceries)
            parsing_citi(transport)
            parsing_citi(entertainment)
            parsing_citi(others)
            parsing_citi(cars)
            parsing_citi(living)
            parsing_citi(clarifications)
            parsing_citi(medicine)
        else:
            if bank == 'alfa':
                if os.path.isfile(out_filename_alfa):
                    os.remove(out_filename_alfa)

                formatcsv_alfa(sys.argv[1])
                parsing_alfa(groceries)
                parsing_alfa(transport)
                parsing_alfa(entertainment)
                parsing_alfa(others)
                parsing_alfa(cars)
                parsing_alfa(living)
                parsing_alfa(clarifications)
                parsing_alfa(medicine)
            else:
                print("Incorrect BANK parameter")
                exit
    else:
        exit


execute(checkinput())
