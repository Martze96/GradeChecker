from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions import mouse_button
from selenium.webdriver.common.action_chains import ActionChains
from getpass import getpass
import smtplib
import time
import datetime

RED = '\033[91m'
GREEN = '\033[92m'
MAGENTA = '\033[35m'
WHITE = '\033[37m'
YELLOW = '\033[93m'

# Parameter für Benutzername und Passwort des LSF
#login_benutzername = "Dein Benutzername"
#login_passwort     = "Dein Passwort"

print(RED+"Vorabhinweis: Daten und Passwörter werden weder gespeichert noch mit Dritten geteilt, sie verkehren hier nur mit sich selbst!")
time.sleep(5)
# E-Mail Benachrichtigungseinstellungen
print(WHITE+"E-Mail Benachrichtigungseinstellungen:")
print("***************************************")
print(YELLOW+"E-Mail Addresse für Benachrichtigung eingeben: (E-Mail Absender ist gleich E-Mail Empfänger!)"+WHITE)
email_addresse     =  input()  
email_addresse_rec = email_addresse
print(YELLOW+"E-Mail Konto Passwort eingeben um Benachrichtigungen senden zu können:"+WHITE)
email_passwort     =  getpass() 
print(YELLOW+"E-Mail SMTP-Server (Bsp.: smtp.gmail.com) eingeben"+WHITE)
server = smtplib.SMTP(input(),587) 
print(RED+"Achtung: Oftmals blockiert der E-Mail Anbieter E-Mails von Programmen wie diesen, bei gmail hilft es die 2-Faktor Authentifizierung auszuschalten und Zugriff durch weniger sichere Apps zu gestatten (danach 10 min. warten) ")
print(WHITE+"E-Mail login in 5 Sekunden")
time.sleep(5)
print("E-Mail Login...")
server.starttls()
server.ehlo()
server.login(email_addresse,email_passwort)
print(GREEN+"E-Mail Login erfoglreich!")


# optionale Parameter
print(YELLOW+"Bitte den Intervall der Prüfung in Sekunden angeben: (Tipp: Lassen sie dem Browser zeit und vermeiden sie unnütze Auslastung des Hochschulservers! Empfehlung: Min. 300 Sekunden = alle 5 Minuten)"+WHITE)
pruef_intervall_in_sekunden = int(input())   # Standardeinstellung: 5 Minuten (Achtung: Dem Browser muss zeit gegeben werden sich bei jeder Prüfung zu aktualisieren, deshalb mindestens 5 Sekunden angeben)

# Systemparameter (nicht ändern, werden selbst gesetzt)
print(YELLOW+"Chrome wird nun geöffnet, bitte bleiben sie bei der Konsole um restliche Daten einzugeben!")
time.sleep(5)
driver = webdriver.Chrome()                                                         # Öffne Chrome
driver.get('https://www.lsf.hs-weingarten.de/qisserver/rds?state=user&type=0')      # gehe auf Webseite des LSF
anzahl_der_noten_start = -1
aktuelle_anzahl_der_noten = -1
#testCounter = 0

def navigateToNotenspiegel():
  notenspiegel = driver.find_element_by_xpath('//*[@id="makronavigation"]/ul/li[4]/a')
  notenspiegel.click()
  time.sleep(5) 

print("Bitte loggen Sie sich in das LSF ein um auf die STARTSEITE zu gelangen, danach bitte hier bestätigen mit der Eingabe von true "+GREEN)
loggedIn = input()
if loggedIn:
    navigateToNotenspiegel()
    print(WHITE+"Bitte warten...")



# Info: Es gibt absolut nichts zu machen, der Bot geht selber ins Internet (Chrome!!), loggt sich ein und nimmt die aktuelle Anzahl der Noten auf. 
#       Dann prüft er in einem Zeitintervall von 5 Minuten die neue Anzahl der Noteneinträge, sollte sich die Anzahl verändern (also es kam eine neue Note hinzu),
#       Dann schickt er eine Benachrichtigungs E-Mail an die eingegebene E-Mail-Addresse.

def logIntoLsf():
  time.sleep(3) 
  name_box = driver.find_element_by_id('asdf')
  print("LSF LOGIN")
  print("**********")
  print("LSF-Benutzername eingeben:  ")
  name_box.send_keys( input())       
  time.sleep(1)
  pass_box = driver.find_element_by_id('fdsa')
  print("LSF-Passwort eingeben:  ")
  pass_box.send_keys( input())      
  time.sleep(1)
  login = driver.find_element_by_id('loginForm:login')
  login.send_keys(Keys.RETURN)
  print("Bitte nichts klicken, der Notenspiegel wird automatisch geöffnet!")
  time.sleep(5)




def InitialCheckGradeEntries():
  global anzahl_der_noten_start
  global aktuelle_anzahl_der_noten
  notentabelle = driver.find_elements_by_xpath('//*[@id="wrapper"]/div[6]/div[2]/table[2]/tbody/tr')
  anzahl_der_noten_start = len(notentabelle)-1
  aktuelle_anzahl_der_noten = anzahl_der_noten_start
  print(WHITE+"Anzahl der Noteneinträge beim ersten Zähldurchgang: " + str(anzahl_der_noten_start))
  time.sleep(2)
  print(GREEN+"Ab jetzt können sie den Chrome Browser minimieren und ein Kaffee trinken gehen, sie werden mit einer E-Mail benachrichtigt sobald es eine Änderung in der Anzahl der Noten gibt. bis dann!"+WHITE)
  time.sleep(10)


def checkGradeEntries():
  global aktuelle_anzahl_der_noten
  global anzahl_der_noten_start
  driver.refresh()
  notentabelle = driver.find_elements_by_xpath('//*[@id="wrapper"]/div[6]/div[2]/table[2]/tbody/tr')
  aktuelle_anzahl_der_noten = len(notentabelle)-1
  print(GREEN+"Anzahl der Noteneinträge bei Start: " + str(anzahl_der_noten_start) + "\n" "Aktuelle Anzahl der Noteneinträge: " + str(aktuelle_anzahl_der_noten)+WHITE )
  time.sleep(5)
  

# ---- Nun immerwieder machen und refreshen
def checkLoop():
  global anzahl_der_noten_start
  global aktuelle_anzahl_der_noten
  global testCounter
  while anzahl_der_noten_start == aktuelle_anzahl_der_noten:
    
    print("***********************************")
    print(str(datetime.datetime.now()) + " *********")
    print("***********************************")
    print("Prüfungsdurchgang wird gestartet...")
    time.sleep(3)
    checkGradeEntries()
    print("Noten geprüft!")
    time.sleep(1)
    print("nächste Prüfung in " + str(pruef_intervall_in_sekunden) + " Sekunden...")
    time.sleep(pruef_intervall_in_sekunden)
    
    # Auskommentiert, das wäre ein Testcase, sodass bei jeder dritten Prüfung eine neue Note dazukommt
    #if testCounter == 3: 
    #  aktuelle_anzahl_der_noten += 1
    #  testCounter = 0
    
    if anzahl_der_noten_start != aktuelle_anzahl_der_noten:
      changedEntries()
      break
    #else: testCounter += 1
    
    
    
      

def changedEntries():
  global aktuelle_anzahl_der_noten
  global anzahl_der_noten_start
  global email_addresse
  global email_addresse_rec
  global server

  
  print(GREEN+"NOTE HAT SICH VERÄNDERT")
  print("NOTE HAT SICH VERÄNDERT")
  print("Notenanzahl hat sich von " + str(anzahl_der_noten_start) + " auf " + str(aktuelle_anzahl_der_noten) + " verändert!")
  server.sendmail(email_addresse, email_addresse_rec, "Hey! Die Anzahl der Noten beim Start waren " + str(anzahl_der_noten_start) + " und sind gerade jetzt " + str(aktuelle_anzahl_der_noten) + " geworden! Checke deine Noten!!!!!!!!")
  print(WHITE+"E-Mail an " + email_addresse_rec + " wurde gesendet!")
  anzahl_der_noten_start = aktuelle_anzahl_der_noten
  checkLoop()
    


# --- MAIN PROZESS  ---

 

#logIntoLsf()

InitialCheckGradeEntries()
checkLoop()
driver.quit()




