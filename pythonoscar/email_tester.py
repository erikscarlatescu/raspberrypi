#!/usr/bin/env python3

import smtplib
from courses import Course

import time

def send_email(recipients, subject="Lorem ipsum dolor sit amet", body="consectetur adipiscing elit"):
    print("Sending email about: " + subject)
    gmail_user = 'saerik2001@gmail.com'
    gmail_password = 'ydtrjsxuecyevnxd'

    sent_from = 'saerik2001@gmail.com'
    to = recipients

    message = """From: Course Notifier <saerik2001@gmail.com>
To:  <%s>
Subject: %s

%s
    """ % ('', subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, message)
        smtp_server.close()
    except Exception as ex:
        print ("Something went wrong….",ex)

send_email(['saerik2001@gmail.com'], 'Starting up OSCAR server', 'The server is started.')

emails = ['saerik2001@gmail.com']

crns = ['85373', '94299', '88359', '92643']
addresses = [0, 0, 0, 0]
courses = [ Course(crn) for crn in crns ]
spots_open = [ 0 for x in crns ]

REFRESH_INTERVAL = 5

while True:
    for i in range(len(courses)):
        course = courses[i]
        #print(course.name)
        num_spots = course.get_registration_info("202308")['vacant']
        print(str(course.name) + ": " + str(course.get_registration_info("202308")))

        if spots_open[i] == 0 and num_spots > 0:
            print("Spot open in " + course.name)
            spots_open[i] = num_spots

            send_email(emails[addresses[i]], course.name + " is open.", "Spot open in " + course.name)
        if spots_open[i] > 0 and num_spots == 0:
            print("Spot closed in " + course.name)
            spots_open[i] = num_spots

            send_email(emails[addresses[i]], course.name + " is closed.", "Spot closed in " + course.name)
    
    time.sleep(REFRESH_INTERVAL)
