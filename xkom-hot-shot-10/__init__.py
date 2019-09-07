import azure.functions as func
from __app__.shared import send_sms


def main(mytimer: func.TimerRequest):
    send_sms.send_sms()
