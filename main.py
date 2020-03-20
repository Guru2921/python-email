import smtplib
# ENV file
from dotenv import load_dotenv
# env
from os import environ

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'guru.softwaremaster@mail.ru'
PASSWORD = 'MbD7j6eQXG4En@L'

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    names, emails = get_contacts('contacts.txt') # read contacts
    message_template = read_template('message.html')

    # set up the SMTP server
    smpt_host = environ.get('SMPT_HOST')
    smpt_port = environ.get('SMPT_PORT')
    s = smtplib.SMTP(host=smpt_host, port=smpt_port)
    s.starttls()
    s.login(environ.get('SMPT_USERNAME'), environ.get('SMPT_PASSWORD'))

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="This is TEST"
        
        # add in the message body
        msg.attach(MIMEText(message, 'html'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    load_dotenv('.env')
    main()