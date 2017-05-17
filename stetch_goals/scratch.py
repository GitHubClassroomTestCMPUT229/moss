#------------------------------------------------------------------------------
# Opens ./teachingTeam.json and returns the contacts list for the teaching team
# contacts["contacts"] is a list of email addresses: ["<address1>", "<address2>", ... ]
#------------------------------------------------------------------------------
def get_contacts():
    f = open("./class/teachingTeam.txt", "r")
    contacts = f.readlines()
    return contacts

#------------------------------------------------------------------------------
# Sends an email notifying about similarities to all members of the teaching team.
# https://docs.python.org/2/library/email-examples.html
# TODO: Serve the html as html within the email.
# TODO: Permit sending from server on eg: Heroku
# https://medium.freecodecamp.com/send-emails-using-code-4fcea9df63f
# https://www.ualberta.ca/computing-science/links-and-resources/technical-support/email/authenticated-smtp
#------------------------------------------------------------------------------
def notify(lab):
    fp = open("./results/{}.html".format(lab), 'rb')
    msg = MIMEText(fp.read())
    fp.close()

    sender = "hoye@cs.ualberta.ca"
    contacts = get_contacts()
    for contact in contacts:
        msg['Subject'] = "CMPUT 229 {} Results".format(lab)
        msg['From'] = sender
        msg['To'] = contact

        s = smtplib.SMTP('localhost')
        # Rough-in of authentication.  Invalid auth error. USERNAME & PASSWORD omitted for now.
        # s = smtplib.SMTP('smtp-auth.cs.ualberta.ca', 587)
        # s.starttls()
        # s.login(USERNAME, PASSWORD)   # KEPT BLANK FOR NOW, BUT TESTED WITH ACTUAL CREDENTIALS
        s.sendmail(sender, contact, msg.as_string())
        s.quit()
