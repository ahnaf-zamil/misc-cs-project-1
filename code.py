#Oliver Thompson CS Homework
import random
import datetime
import csv
#Constants
POINTS_PER_DAY_REDEEMED = 25000
MIN_DAYS_TO_BOOK = 1
MAX_DAYS_TO_BOOK = 14
POINTS_BY_TIER = {'Silver':2500,'Gold':3000,'Platinum':4000}

def open_file():
    #Opens file and reads data into list
    with open('SampleData2017.txt') as file:
        return [line.strip().split(',')for line in file]

def random_id():
    #Generates random 3 digit number for member id
    digit1 = str(random.randint(0,9))
    digit2 = str(random.randint(0,9))
    digit3 = str(random.randint(0,9))
    return digit1+digit2+digit3

def make_new_id(name,data):
    #Makes member id for the new member
    namebit = name[0:3] #Fail with name < 3 chars. Fix This
    now = datetime.datetime.now()
    yearbit = now.year % 100 #Last two digits
    while True:
        numbit = random_id()
        new_id = namebit+numbit+str(yearbit)
        if is_unique(new_id,data):
            return namebit+numbit+str(yearbit)

def is_unique(new_id,data):
    #Checks if the new member id already exists
    for row in data:
        if new_id == row[0]:
            return False
    return True

def exists(user_id,data):
    #Returns true if a user_id exists (i.e. is valid)
    return not is_unique(user_id,data)

def new_member(name,data):
    #Makes a new member and adds all necessary data to their record
    now = datetime.datetime.now()
    member = [make_new_id(name,data),name,str(now.year),'Silver','0','0']
    return member

def writer(data):
    #Writes updated data back to text file
    with open('SampleData2017.txt', 'w') as csvfile:
        textwriter = csv.writer(csvfile, delimiter=',')
        for row in data:
            textwriter.writerow(row)

def update_customer_nights(nights,customer_record):
    #print('update_customer_nights')
    customer_record[4] = int(customer_record[4]) + nights
    customer_record[5] = int(customer_record[5]) + POINTS_BY_TIER[customer_record[3]]*nights
    #Membership status check
    if int(customer_record[4]) >= 100:
        customer_record[3] = 'Platinum'
    elif int(customer_record[4]) >= 30:
        customer_record[3] = 'Gold'
    return customer_record

def find_customer_index(memid,data):
    #Extracts the data of the customer out of all the data
    for i in range(len(data)):
        if memid == data[i][0]:
            return i

def update_nights(memid,data,nights):
    #print('update_nights')
    customer_index = find_customer_index(memid,data)
    customer_record = data[customer_index]
    del data[customer_index]
    data.append(update_customer_nights(nights,customer_record))
    return data

def input_id(data):
    #Loops through each customer id in the text file and checks if the one you input matches one of them
    while True:
        memid = input('Please enter member id ')
        if exists(memid,data):
            return memid
        else:
            print('Member id is invalid')
    
def book_nights(data):
    #Function for a member to book nights
    #print('\nbook_nights')
    memid = input_id(data)
    while True:
        nights = int(input('Please input the number of nights booked '))
        if nights >= MIN_DAYS_TO_BOOK and nights <= MAX_DAYS_TO_BOOK:
            break
        else:
            print('Value invalid: enter a value between 1 and 14')
    return update_nights(memid,data,nights)

def redeem_points(data):
    #Redeeming points for nights
    #print('\nredeem_points')
    memid = input_id(data)
    nights_redeemed = int(input('Input the number of nights redeemed: '))
    point_cost = nights_redeemed*POINTS_PER_DAY_REDEEMED
    customer_index = find_customer_index(memid,data)
    customer_record = data[customer_index]
    current_points = int(customer_record[5])
    if current_points >= point_cost:
        #Increment nights booked & decrement point balance
        customer_record[4] = int(customer_record[4]) + nights_redeemed
        customer_record[5] = current_points - point_cost
        del data[customer_index]
        data.append(customer_record)
        print('Points redeemed')
    else:
        print('You do not have enough points to complete this action')
                                     
def main():
    #Main function - runs whole program
    data = open_file()
    end = 0
    while end == 0:
        now = datetime.datetime.now()
        #User interface
        choice = input('''\n{0}/{1}/{2} {3}:{4}
================================
System Menu:

1) Add New Member
2) Book Nights
3) Redeem Points
4) View Members

Q to Quit
================================
>>>'''.format(now.day,now.month,now.year,now.hour,now.minute))
        if choice == '1':
            name = input("Please enter the customer's surname: ")
            data.append(new_member(name,data))
            writer(data)
        elif choice == '2':        
            book_nights(data)
            writer(data)
        elif choice == '3':
            redeem_points(data)
            writer(data)
        elif choice == '4':
            print('\nFormat = Member ID, Surname, Year Joined, Membership status, Nights Booked, Point Balance\n')
            for thing in data:
                print(thing)
        elif choice.lower() == 'q':
            print('\nSystem shutting down')
            end = 1

main()
