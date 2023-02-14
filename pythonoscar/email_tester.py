#!/usr/bin/env python3

import smtplib
from courses import Course

import time

def send_email(recipients, subject="Lorem ipsum dolor sit amet", body="consectetur adipiscing elit"):
    print("Sending email about: " + subject)
    gmail_user = 'saerik2001@gmail.com'
    gmail_password = 'Rikoitza2001'

    sent_from = gmail_user
    to = recipients

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

crns = ["32618", "27177", "27663"]
courses = [ Course(crn) for crn in crns ]
spots_open = [ 0 for x in crns ]

REFRESH_INTERVAL = 20

while True:
    for i in range(len(courses)):
        course = courses[i]
        #print(course.name)
        num_spots = course.get_registration_info("202202")['vacant']

        if spots_open[i] == 0 and num_spots > 0:
            print("Spot open in " + course.name)
            spots_open[i] = num_spots

            send_email("saerik2001@gmail.com", "Class", "Spot open in " + course.name)
        if spots_open[i] > 0 and num_spots == 0:
            print("Spot closed in " + course.name)
            spots_open[i] = num_spots

            send_email("saerik2001@gmail.com", "Class", "Spot closed in " + course.name)
    
    time.sleep(REFRESH_INTERVAL)
