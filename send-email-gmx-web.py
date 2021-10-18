import smtplib
#import urllib2
import datetime
from email.mime.text import MIMEText

#def get_ip():
 #       ip = urllib2.urlopen("http://automation.whatismyip.com/n09230945.asp").read()
  #      return ip

def send_ip():
        
        sender = "maul_martin@gmx.de" # Email des Absenders eintragen
        receiver = "maul_martin@gmx.de" # Email des Empfaenfers eintragen
        s = smtplib.SMTP("mail.gmx.net")
        s.ehlo()
        s.starttls() # SMTP-Server deines Email-Anbieters eintragen
        s.login("maul_martin@gmx.de", "Mmartin96") # LogIn-Name und Passwort deines Email_Accounts eintragen

        # Aktuelles Datum holen
        Datum = datetime.date.today()
        # Text
       # my_ip = get_ip()
       # print ("IP: " + my_ip)
        msg = MIMEText("Test hier wird keine IP versendet nach")
        msg['Subject'] = 'Nachricht vom Raspberry Pi - %s' % Datum.strftime('%b %d %Y')
        msg['From'] = sender
        msg['To'] = receiver


        s.sendmail(sender, receiver, msg.as_string())

if __name__ == "__main__":
        send_ip()