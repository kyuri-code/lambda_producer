from sqlalchemy.orm import Session
from models.log_model import Log, LogModel
from db_client.db_client import DBClient
from client.sqs_client import SQSClient
import uuid

class ProducerService:
    def __init__(self):
        self.db_client = DBClient()
        self.sqs_client = SQSClient()
        self.db_client.connect()
    
    def process(self):
        session: Session = self.db_client.Session()
        process_id = str(uuid.uuid4())
        start_uuid = str(uuid.uuid4())
        end_uuid = str(uuid.uuid4())

        try:
            # 開始ログをDBに追加
            start_log = Log(uuid=start_uuid, log_message='Process started', processid=process_id)
            session.add(start_log)
            session.commit()

            # SQSにメッセージを送信
            self.sqs_client.send_message('This is a test message', process_id)
            
            # 終了ログをDBに追加
            end_log = Log(uuid=end_uuid, log_message='Process ended', processid=process_id)
            session.add(end_log)
            session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Error in producer process: {e}")

        finally:
            session.close()
            self.db_client.disconnect()