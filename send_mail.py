#!/usr/bin/python
import time, os, glob, email, math
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# username = "anhminh3105@gmail.com"
# password = "minhNguyen.0449691348"
# recipients = ['anhminh3105@gmail.com', 'minhdo039@gmail.com', 'pham.chinh1197@gmail.com']
# recipients = ['anhminh3105@gmail.com']        
# path_to_dir = '/home/pi/'
def send_mail(username="pi3.centre@gmail.com", password="rasPb3rryP1", recipients=['anhminh3105@gmail.com', 'minhdo039@gmail.com', 'pham.chinh1197@gmail.com'], path_to_dir='/home/pi/GUI/database/'):
    device_list = 'device_list.csv'
    content = 'Here is the latest update of your house data.\n\n'
    for file_path in glob.glob(path_to_dir + '*.csv'):
        if os.path.getsize(file_path) > 0:
            data_type = file_path.split('/')[-1].replace('.csv', '')
            if data_type != 'device_list':
                with open(file_path, 'r') as f:
                    line = f.readlines()[-1]
                    cols = line.split(',')
                    hour = math.floor(float(cols[3]))
                    hour_float = float(cols[3]) - hour
                    minute = math.floor(hour_float * 60)
                    second = math.floor(((hour_float * 60) - minute) * 60)
                    content += 'On ' + cols[0] + '-' + cols[1] + '-' + cols[2] + ' at ' + str(hour) + ':' + str(minute) + ':' + str(second) + ' ' + data_type + ': ' + cols[4]     

    content += '\nCurrent Device Status:\n'
    device_list_filepath = path_to_dir + device_list
    if os.path.getsize(device_list_filepath) > 0:
        with open(device_list_filepath) as f:
            for line in f.readlines():
                cols = line.split(',')
                content += 'Name: ' + cols[0] + ' -- Code: ' + cols[1] + ' -- Location: ' + cols[2] + ' -- Status: ' + ('Enabled' if int(cols[3]) == 1 else 'Disabled')
                # print(line)
    try:
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = ','.join(recipients)
        msg['Subject'] = "Property Monitor Data Report on " + datetime.now().strftime("%Y:%m:%d:%H:%M:%S") 
        msg.attach(MIMEText(content))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(username, password)
        s.sendmail(username, recipients, msg.as_string())
        s.close()
        print('email has been sent successfully.\nEmail Preview:\n')
        print(content)
        return True
    except Exception as e:
        print('failed to send email with error')
        print(e)
    return False

def main():
    send_mail()

if __name__ == "__main__":
    main()