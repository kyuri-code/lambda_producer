from src.services.producer_service import ProducerService

def lambda_hander(event, context):
    producer_service = ProducerService()
    producer_service.process()

    return {
        'statusCode': 200,
        'body': 'Producer process completed successfully'
    }