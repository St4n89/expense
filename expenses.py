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
out_filename = str("Spendings "+timestamp+".csv")

if os.path.isfile('unknown.csv'): #removing old files if exist
    os.remove('unknown.csv')

if os.path.isfile(out_filename): #removing old files if exist
    os.remove(out_filename)


def dictionarize(file, dictionary): #this creates dictionaries out of files
    dictfile = open(file)
    with dictfile as input_file:
        for line in input_file:
            key, value = line.split(":")
            dictionary[key] = value.strip()


def parsing_alfa(dictionary,nameline):
    expenses_lines = [] #array for csv processing
    removals = [] #storage for the removed entries

    with open('output_alfa.csv') as input_file: #get input from formatted csv
        read = csv.reader(input_file, delimiter=';')
        fin_file = open(out_filename,'a')

        fin_file.write(nameline) #writing category name to output file
        fin_file.write("\n")

        for row in read: #creating 2D array of expenses
            expenses_rows = [row[0],row[1],row[2]]
            expenses_lines.append(expenses_rows)

        for str_num in range(len(expenses_lines)):
            sms = expenses_lines[str_num][1]
            for word in dictionary:
                found = sms.count(word) #search for word from dictionary
                if found:
                    store = dictionary.get(word)
                    realdate = ((re.search('[0-9][\s][0-9][0-9].[0-9][0-9].[0-9][0-9]', sms)).group(0)) #read date from sms line
                    expdate = str((re.search('[0-9][0-9].[0-9][0-9].[0-9][0-9]', realdate).group(0)).replace('.', '/')) #getting actual date
                    cost = int(round(float(expenses_lines[str_num][2].replace(',', '.'))))
                    fin_file.write((expdate+"20"+";"+store+";"+str(cost)+"\n"))
                    removals.append(str_num) #adding the found entry to the list for removals

    removals.sort(reverse=True) #reversing, so that the last entries popped out first
    expenses_copy = list(expenses_lines) #copying the list to tamper with the copy

    for rem_str_num in range(len(removals)): #this is needed to get the list of unprocessed entries
        expenses_copy.pop(removals[rem_str_num]) #popping out found entries

    os.remove('output_alfa.csv')
    temp_file = open('output_alfa.csv','a')
    for fin_str_num in range(len(expenses_copy)): #here will be the unprocessed entries
        tempdate = str(expenses_copy[fin_str_num][0].replace('.', '/')) #correcting the date format
        temp_file.write((tempdate+";"+expenses_copy[fin_str_num][1]+";"+expenses_copy[fin_str_num][2]+"\n"))


def parsing_citi(dictionary):
    expenses_lines = []
    removals = []

    with open('output_citi.csv') as input_file:
        read = csv.reader(input_file, delimiter=';')
        fin_file = open(out_filename,'a')

        for row in read:
            expenses_rows = [row[0],row[1],row[2]]
            expenses_lines.append(expenses_rows) #building the 2D list of transactions

        for str_num in range(len(expenses_lines)):
            sms = expenses_lines[str_num][1]
            for word in dictionary:
                found = sms.count(word)
                if found:
                    store = dictionary.get(word)
                    expdate = expenses_lines[str_num][0]
                    cost = int(round(float(expenses_lines[str_num][2].replace('-', ''))))
                    fin_file.write((expdate+";"+store+";"+str(cost)+"\n"))
                    removals.append(str_num) #adding the found entry to the list for removals

    removals.sort(reverse=True) #reversing, so that the last entries popped out first
    expenses_copy = list(expenses_lines)

    for rem_str_num in range(len(removals)):
        expenses_copy.pop(removals[rem_str_num]) #popping out found entries

    os.remove('output_citi.csv')
    temp_file = open('output_citi.csv','a')
    for fin_str_num in range(len(expenses_copy)): #here will be the unprocessed entries
        temp_file.write((expenses_copy[fin_str_num][0]+";"+expenses_copy[fin_str_num][1]+";"+expenses_copy[fin_str_num][2]+"\n"))

    fin_file.write("\n")


def formatcsv_alfa(filename):
    with open(filename) as input_file:
        read = csv.reader(input_file, delimiter=';')
        with open('output_alfa.csv', 'w') as output:
            next(read)
            write = csv.writer(output, delimiter=';')
            for row in reversed(list(read)):
                hold_status = row[4] #processing unfinished transactions in the log
                found_hold = hold_status.count("HOLD")
                if found_hold: #if the transaction is in HOLD status
                    write.writerow((row[3]+"20", ("00 "+str(row[3])+" "+str(row[5])), row[7])) #add date to sms line
                else:
                    if row[7] != "0": #if the transaction is an expense
                        write.writerow((row[3]+"20", row[5], row[7])) #do not change the sms line
                    else: #if it is not an expense
                        write.writerow((row[3]+"20", ("00 "+str(row[3])+" "+str(row[5])), row[6])) #add date to sms line


def formatcsv_citi(filename): #formatting citibank csv files
    with open(filename) as input_file:
        read = csv.reader(input_file, delimiter=',')
        with open('output_citi.csv', 'w') as output:
            write = csv.writer(output, delimiter=';')
            for row in reversed(list(read)):
                if float(row[2]) <= "0":
                    write.writerow((row[0], row[1], row[2]))


def execute():
        groceries = {} #creating the dictionaries
        transport = {}
        entertainment = {}
        others = {}
        cars = {}
        living = {}
        clarifications = {}
        medicine = {}
        kazan = {}
        restaurants = {}

        dictionarize('groceries.dic', groceries) #dictionarizing them
        dictionarize('transport.dic', transport)
        dictionarize('entertainment.dic', entertainment)
        dictionarize('others.dic', others)
        dictionarize('cars.dic', cars)
        dictionarize('living.dic', living)
        dictionarize('clarifications.dic', clarifications)
        dictionarize('medicine.dic', medicine)
        dictionarize('kazan.dic', kazan)
        dictionarize('restaurants.dic', restaurants)

        formatcsv_alfa('alfa.csv') #formatting the input files
        formatcsv_citi('citi.csv')

        parsing_alfa(groceries,"Products") #parsing the temp-output files
        parsing_citi(groceries) #note that alfabank function is always the first
        parsing_alfa(transport,"Transport") #it is needed for correct processing
        parsing_citi(transport)
        parsing_alfa(entertainment,"Entertainment")
        parsing_citi(entertainment)
        parsing_alfa(others,"Others")
        parsing_citi(others)
        parsing_alfa(cars,"Cars")
        parsing_citi(cars)
        parsing_alfa(living,"Living")
        parsing_citi(living)
        parsing_alfa(medicine,"Medicine")
        parsing_citi(medicine)
        parsing_alfa(kazan,"Kazan")
        parsing_citi(kazan)
        parsing_alfa(restaurants,"Restaurants")
        parsing_citi(restaurants)
        parsing_alfa(clarifications,"For review")
        parsing_citi(clarifications)


def csvmerge(): #merging two temp-output files into one
    readalfa = open('output_alfa.csv') #so that it has unknown transactions
    readciti = open('output_citi.csv') #from both input files

    writecsv = open('unknown.csv','a')

    for line in readalfa:
        writecsv.write("ALFA;"+(line)) #ALFA to know if the line is from alfabank

    for line in readciti:
        writecsv.write("CITI;"+line) #CITI to know if the line is from citibank

    os.remove('output_citi.csv')
    os.remove('output_alfa.csv')


execute()
csvmerge()
