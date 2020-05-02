# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:13:31 2019

@author: Ishaan Radia
"""
#Imports for email sending and reading command line arguments
import smtplib
import time
from string import Template
import pandas as pd
import sys
import io, pkgutil

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def read_args():
    """
    Method to read inputs for parameters to email and store them.
    
    If major is not provided, there will be no message with your personalized major sent.
    If your major is provided, there will be a short message with your area of interest and praising the college.
    """

    EMAIL_ADDRESS = input("Enter email address: ")
    PASSWORD = input("Enter password: ")
    NAME = input("Enter your name: ")
    HOME_ADDRESS = input("Enter your home address: ")
    T_SHIRT_SIZE = input("Enter your T-Shirt size: ")
    MAJOR = input("Enter your intended major (or N if you don't want to): ")
    conf = input("You are about to email 1718 colleges asking for a t-shirt. Please confirm that you wish to proceed with this (Y/N): ")
    
    if conf != "Y" or conf != "y":
        sys.exit(0)

    if MAJOR == "N" or MAJOR == "n":
        MAJOR_STR = ""
    else:
        MAJOR_STR = f"I'm very interested in {MAJOR}, which I know is well reputed at your college!"

    return (EMAIL_ADDRESS, PASSWORD, NAME, HOME_ADDRESS, T_SHIRT_SIZE, MAJOR_STR)

def put_in_txt():
    """
    Helper Method to read in the name of each college in the list and add it to a list.
    """

    data = pkgutil.get_data("freetshirts", "CollegeEmails.csv")
    email = pd.read_csv(io.BytesIO(data)).head()
    names = []
    emails = []
    for college in email['College']:
        names.append(college)
    for emai in email['Email']:
        emails.append(emai)
    return (names, emails)

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    data = pkgutil.get_data("freetshirts", filename)
    return Template(data)

def set_up_template(template, college_name, home_address, t_shirt_size, name, major_str):
    """
    Helper method that modifies message to contain proper substitutes with Template object as input.
    """

    # add in the command line parameters to the message template
    message = template.substitute(PERSON_NAME = college_name,
    MAJOR = major_str,
    ADDRESS = home_address,
    TSHIRT = t_shirt_size,
    FIRST_NAME = name)

    return message

def create_message(sender, receiving_addr, message, subject):
    """
    Helper method that creates email message object with the correct from and to email address.
    """

    #create message
    msg = MIMEMultipart() 

    #add necessary From and To fields
    msg['From'] = sender
    msg['To'] = receiving_addr
    msg['Subject'] = f"Merchandise Request for {subject}"

    #add message to email
    msg.attach(MIMEText(message, 'plain'))

    return msg


def send_email():
    """
    Method for the main execution of the program.
    Reads in the college file, iterates through each email, and sends the customized message to each college.
    """

    #setup the names, emails, and template
    names, emails = put_in_txt()
    message_template = read_template('message.txt')
    count = 0
    EMAIL_ADDRESS, PASSWORD, NAME, HOME_ADDRESS, T_SHIRT_SIZE, MAJOR_STR = read_args()
    
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(EMAIL_ADDRESS, PASSWORD)

    # Send the email to each college
    for college_name, college_email in zip(names, emails):

        #Create message with customized parameters for that college
        message = set_up_template(message_template, college_name, HOME_ADDRESS, T_SHIRT_SIZE, NAME, MAJOR_STR)
        print(message)

        #create message and save it
        msg = create_message(EMAIL_ADDRESS, college_email, message, college_name)

        #send email message and print out successful completion message
        s.send_message(msg)
        del msg
        count += 1
        print (f"Sending email to {college_name}. This is email #{count}.")
            
    # Terminate the SMTP session and close the connection
    s.quit()
    print ('Sent to ' + str(count) + ' colleges')
    
