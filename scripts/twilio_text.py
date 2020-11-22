from twilio.rest import Client
import fire
import yaml
from pathlib import Path
import os
#pip install twilio
# Get from number, account_sid and auth_token here : https://www.twilio.com/console/sms/getting-started/build
# To learn more about sending Whatsapp texts : https://www.twilio.com/console/sms/whatsapp/learn

with open(os.path.join(Path(__file__).resolve().parents[1],'creds.yml')) as creds_file:
    creds = yaml.load(creds_file.read(),Loader=yaml.FullLoader)

DEFAULT_FROM = creds['twilio']['from']
DEFAULT_WAPP_FROM = creds['twilio']['wapp_from']
DEFAULT_BODY = creds['twilio']['body']
DEFAULT_TO = creds['twilio']['to']
account_sid = creds['twilio']['account_sid']
auth_token = creds['twilio']['auth_token']
#SMS cost : 0.00175 USD
#Whatsapp cost : 0.0007 USD

def send_sms(from_num=DEFAULT_FROM, to_num=DEFAULT_TO, body=DEFAULT_BODY):
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_= from_num, body=body, to=to_num)
    print ("Credits left :$%s"%client.balance.fetch().balance)
    print ("Message ID : %s"%message.sid)

def send_whatsapp(from_num=DEFAULT_WAPP_FROM, to_num=DEFAULT_TO, body=DEFAULT_BODY):
    from_num = "whatsapp:"+from_num if not from_num.startswith('whatsapp:') else from_num
    to_num = "whatsapp:"+to_num if not to_num.startswith('whatsapp:') else to_num
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_=from_num, body=body, to=to_num)
    print ("Message ID : %s"%message.sid)
    print ("Credits left :$%s"%client.balance.fetch().balance)

if __name__ == "__main__":
    fire.Fire({"send_sms":send_sms, 'send_whatsapp':send_whatsapp})