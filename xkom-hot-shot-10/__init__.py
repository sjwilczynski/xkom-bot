import azure.functions as func
from __app__.shared import data_processor


def main(mytimer: func.TimerRequest):
    data_processor.process_new_data_from_webpage()
