# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List,Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, EventType
import mysql.connector
import os
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from pretty_html_table import build_table
class Deposit(Action):
     def name(self) -> Text:
         return "action_deposit"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         acc_no=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         query = """select Cust_Name,Inv_Equity_Amt,Broker_email from margin_shortfall where Port_Num = %s"""
         cursor.execute(query,(acc_no,))
         records = cursor.fetchall()


         for row in records:

                    x = row[0]#cust name
                    y = row[1]#Inv_Equity_Amt
                    z = row[2]#mail id


         print(records)
         recipients = [z]
         print(recipients)
         emaillist = [elem.strip().split(',') for elem in recipients]
         msg = MIMEMultipart()
         msg['Subject'] = "Margin Call - Deposit Shares"
         msg['From'] = 'trojanmargincall@gmail.com'
         html = """\
                        <html>

                            <body>
                                     Hello,<br>

                                     </br>Client has decided to deposit the share to pay for the Margin Shortfall. Please Deposit the shares in Margin account.

                            <p>
                             Customer's Margin Shortfall amount is {0}{1}<br></br>


                            </p>


                          </body>
                            </html>
                        """.format("Rs.",y)
         #http://localhost:5002/guest/conversations/production/ad2191c19acb466381e12304c586cf71
         message = MIMEText(html, 'html')
         msg.attach(message)
         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
         #s.login(user = 'trojanmargincall@gmail.com',password = 'fwtlhalveomgebwx')
         server.login(user ='trojanmargincall@gmail.com',password = 'kwbwqtvivhmfbzgr')
         server.sendmail(msg['From'], emaillist , msg.as_string())
         server.quit()
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(acc_no,))
         connection.commit()
         #print("Table Updated")
         return []


class Greet(Action):
     def name(self) -> Text:
         return "action_greet"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         acc_no=tracker.get_slot('Port_Num')
         array= re.findall(r'[0-9]+',acc_no)
         p = (len(array[0]))
         if p == 6:
             connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
             cursor = connection.cursor()
             sql_select_query = """select * from margin_shortfall where Port_Num = %s"""
             cursor.execute(sql_select_query,(acc_no,))
             records = cursor.fetchall()
             try:
              for row in records:
                    #x = row[0]
                    y = row[2]
                    z = row[10]
              dispatcher.utter_message("Welcome  "+y+" , Your Margin Shortfall amount is "+z+" ")
              #dispatcher.utter_message("Your Outstanding amount is  "+z+" ")
             except:
              dispatcher.utter_message("Oh! Looks like you entered a wrong Portfolio Number. Entered Portfolio Number does not exist in the system.\nPlease Enter a valid portfolio Number")
         else:
             dispatcher.utter_message("Please check the number of digits mentioned in the Portfolio Number. Portfolio number is of 6 Digits ")
         return []
class ActionHelloWorld(Action):
     def name(self) -> Text:
         return "action_hello_world"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """select * from margin_shortfall where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         records = cursor.fetchall()
         for row in records:
                y = row[2]
                z = row[11]
                if z == "Pending":
                   dispatcher.utter_message(template="utter_payoption" )
                else:
                   dispatcher.utter_message("Congratulations, your portfolio is strong. You do not have any Margin shortfall")
                   dispatcher.utter_message(template='utter_end')
         return []
class ActionSbi(Action):
     def name(self) -> Text:
         return "action_sbi"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\"https://retail.onlinesbi.com/retail/login.htm")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Payment Successful! Your margin shortfall is corrected.")
         #dispatcher.utter_message(" Happy Trading")
         #print("Table updated")
         return []
class ActionIcici(Action):
     def name(self) -> Text:
         return "action_icici"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\" https://www.icicibank.com/Personal-Banking/insta-banking/internet-banking/index.page")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Payment Successful! Your margin shortfall is corrected.")
         #dispatcher.utter_message(" Happy Trading")
         #print("Table updated")

         return []
class ActionCiti(Action):
     def name(self) -> Text:
         return "action_citi"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\" https://www.online.citibank.co.in/products-services/online-services/internet-banking.htm")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Payment Successful! Your margin shortfall is corrected.")
         #dispatcher.utter_message(" Happy Trading")
         #print("Table updated")
         return []
class ActionAngel(Action):
     def name(self) -> Text:
         return "action_angel"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\" https://trade.angelbroking.com/")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Shares sold successfully and will reflect in the account post settlement")
         #dispatcher.utter_message(" Happy Trading")
         return []
class ActionIciciDirect(Action):
     def name(self) -> Text:
         return "action_icici_direct"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\" https://secure.icicidirect.com/customer/login")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Shares sold successfully and will reflect in the account post settlement")
         #dispatcher.utter_message(" Happy Trading")
         print("Table updated")
         return []
class ActionZerodha(Action):
     def name(self) -> Text:
         return "action_zerodha"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\" https://kite.zerodha.com/")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Shares sold successfully and will reflect in the account post settlement")
         #dispatcher.utter_message(" Happy Trading")
         print("Table updated")
         return []
class ActionKotak(Action):
     def name(self) -> Text:
         return "action_kotak_sec"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\" https://www.kotaksecurities.com/login_ubi.html")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Shares sold successfully and will reflect in the account post settlement")
         #dispatcher.utter_message(" Happy Trading")
         print("Table updated")
         return []
class ActionUpstox(Action):
     def name(self) -> Text:
         return "action_upstox"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         os.system("start \"\" https://api.upstox.com/index/login")
         folio=tracker.get_slot('Port_Num')
         connection = mysql.connector.connect(host='localhost',database='margin',user='root',password='1234')
         cursor = connection.cursor()
         sql_select_query = """update margin_shortfall set Inv_Equity_Amt = '0', Stat_Marg_Call = 'Paid' where Port_Num = %s"""
         cursor.execute(sql_select_query,(folio,))
         connection.commit()
         dispatcher.utter_message("Thanks. Shares sold successfully and will reflect in the account post settlement")
         #dispatcher.utter_message(" Happy Trading")
         print("Table updated")
         return []