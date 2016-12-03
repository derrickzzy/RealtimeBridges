__author__ = 'zzhao01'

# send email
def send(msg_condition):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.mime.application import MIMEApplication
    fromaddr = 'realtimebridge@gmail.com'
    toaddrs  = 'zhiyong.zhao@tufts.edu'
    msgtext = "\tThis is a notice for Powder Mill Bridge.\n" \
          "\tThe Bridge health condition has changed.\n\n" \
          "\tThe current health condition is "+msg_condition+"\nAuto-send by the Real-time Bridge Structural Health Monitoring System"

    msg = MIMEMultipart()
    msg['From'] = 'Real-time Bridge'
    msg['To'] = 'zhiyong.zhao@tufts.edu'
    msg['Subject'] = '[Alert] Bridge Condition Changed!!!'

    msg.attach(MIMEText(msgtext))

    #msg.attach(MIMEApplication(file("C:/Users/zzhao01/Documents/Webserver/website/report.pdf").read(),'pdf'))

    # Credentials (if needed)
    username = 'realtimebridge@gmail.com'
    password = 'tuftscee'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

if __name__ == '__main__':
    send(msg_condition)
