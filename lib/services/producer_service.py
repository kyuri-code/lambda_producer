from sqlalchemy.orm import Session

import uuid
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.models.log_model import Log, LogModel
from lib.db_client.db_client import DBClient
from lib.client.sqs_client import SQSClient

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
            start_log = Log(uuid=start_uuid, log_message='Producer process started', processid=process_id)
            session.add(start_log)
            session.commit()

            # SQSにメッセージを送信
            self.sqs_client.send_message('This is a test message', process_id)
            
            # 終了ログをDBに追加
            end_log = Log(uuid=end_uuid, log_message='Producer process ended', processid=process_id)
            session.add(end_log)
            session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Error in producer process: {e}")

        finally:
            session.close()
            self.db_client.disconnect()