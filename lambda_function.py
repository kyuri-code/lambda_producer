import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.services.producer_service import ProducerService

def lambda_hander(event, context):
    producer_service = ProducerService()
    producer_service.process()

    return {
        'statusCode': 200,
        'body': 'Producer process completed successfully'
    }