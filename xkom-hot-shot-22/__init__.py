import azure.functions as func
from __app__.shared import process_new_data


def main(mytimer: func.TimerRequest):
    process_new_data.process_new_data_from_webpage()