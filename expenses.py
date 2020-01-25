#!/usr/bin/env python
import csv
import re
import sys
import os
import datetime
import calendar

gettime = datetime.datetime.now() #getting times-dates for filenames
month_now = calendar.month_abbr[gettime.month]
timestamp = str(str(gettime.day)+"-"+str(month_now)+"-"+str(gettime.year))
out_filename_alfa = str("Alfabank "+timestamp+".csv")
out_filename_citi = str("Citibank "+timestamp+".csv")

if os.path.isfile('output.csv'):
    os.remove('output.csv')


def checkinput(): #checking if any paramenters were specified
    if len(sys.argv) > 1:
        run = 1
        return run
    else:
        print("Please specify input files!")
        run = 0
        return run


def dictionarize(file, dictionary): #this creates dictionaries out of files
    dictfile = open(file)
    with dictfile as input_file:
        for line in input_file:
            key, value = line.split(":")
            dictionary[key] = value.strip()


def parsing_alfa(dictionary,nameline):
    expenses_lines = [] #array for csv processing
    removals = [] #storage for the removed entries

    with open('output.csv') as input_file: #get input from formatted csv
        read = csv.reader(input_file, delimiter=';')
        fin_file = open(out_filename_alfa,'a')

        fin_file.write(nameline)
        fin_file.write("\n")

        for row in read: #creating 2D array of expenses
            expenses_rows = [row[0],row[1],row[2]]
            expenses_lines.append(expenses_rows)

        for str_num in range(len(expenses_lines)):
            sms = expenses_lines[str_num][1]
            for word in dictionary:
                found = sms.count(word)
                if found:
                    store = dictionary.get(word)
                    realdate = ((re.search('[0-9][\s][0-9][0-9].[0-9][0-9].[0-9][0-9]', sms)).group(0)) #read date from sms line
                    expdate = str((re.search('[0-9][0-9].[0-9][0-9].[0-9][0-9]', realdate).group(0)).replace('.', '/'))
                    cost = int(round(float(expenses_lines[str_num][2].replace(',', '.'))))
                    fin_file.write((expdate+";"+store+";"+str(cost)+"\n"))
                    removals.append(str_num)

    removals.sort(reverse=True) #reversing, as the dates are last to first by default
    expenses_copy = list(expenses_lines) #copying the list to tamper with the copy

    for rem_str_num in range(len(removals)): #this is needed to get the list of unprocessed entries
        expenses_copy.pop(removals[rem_str_num])

    os.remove('output.csv')
    temp_file = open('output.csv','a')
    for fin_str_num in range(len(expenses_copy)): #here will be the unprocessed entries
        temp_file.write((expenses_copy[fin_str_num][0]+";"+expenses_copy[fin_str_num][1]+";"+expenses_copy[fin_str_num][2]+"\n"))

    fin_file.write("\n")


def parsing_citi(dictionary,nameline):
    expenses_lines = []
    removals = []

    with open('output.csv') as input_file:
        read = csv.reader(input_file, delimiter=';')
        fin_file = open(out_filename_citi,'a')

        fin_file.write(nameline)
        fin_file.write("\n")

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
                    fin_file.write((expdate+";"+store+";"+str(cost)+"\n"))
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
                hold_status = row[4] #processing unfinished transactions in the log
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
        kazan = {}
        restaurants = {}

        dictionarize('groceries.dic', groceries)
        dictionarize('transport.dic', transport)
        dictionarize('entertainment.dic', entertainment)
        dictionarize('others.dic', others)
        dictionarize('cars.dic', cars)
        dictionarize('living.dic', living)
        dictionarize('clarifications.dic', clarifications)
        dictionarize('medicine.dic', medicine)
        dictionarize('kazan.dic', kazan)
        dictionarize('restaurants.dic', restaurants)

        if bank == 'citi':
            if os.path.isfile(out_filename_citi):
                os.remove(out_filename_citi)

            formatcsv_citi(sys.argv[1])
            parsing_citi(groceries,"Products")
            parsing_citi(transport,"Transport")
            parsing_citi(entertainment,"Entertainment")
            parsing_citi(others,"Others")
            parsing_citi(cars,"Cars")
            parsing_citi(living,"Living")
            parsing_citi(medicine,"Medicine")
            parsing_citi(kazan,"Kazan")
            parsing_citi(restaurants,"Restaurants")
            parsing_citi(clarifications,"For review")
        else:
            if bank == 'alfa':
                if os.path.isfile(out_filename_alfa):
                    os.remove(out_filename_alfa)

                formatcsv_alfa(sys.argv[1])
                parsing_alfa(groceries,"Products")
                parsing_alfa(transport,"Transport")
                parsing_alfa(entertainment,"Entertainment")
                parsing_alfa(others,"Others")
                parsing_alfa(cars,"Cars")
                parsing_alfa(living,"Living")
                parsing_alfa(medicine,"Medicine")
                parsing_alfa(kazan,"Kazan")
                parsing_alfa(restaurants,"Restaurants")
                parsing_alfa(clarifications,"For review")
            else:
                print("Incorrect BANK parameter")
                exit
    else:
        exit


execute(checkinput())
