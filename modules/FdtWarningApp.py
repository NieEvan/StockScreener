import threading
import json
from datetime import datetime
from typing import Optional
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
import sqlite3

from websocket import WebSocketApp, WebSocket
from database.mongo_client import connect_to_mongodb
from database.models import SignalModel


def execute_sql(db_path: str, sql: str, params: tuple = ()) -> list:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(sql, params)
    fetchall = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return fetchall


def send_email(recipient_email: str, body: str, subject: str, pwd: str, sender_email: str) -> None:
    smtp_server = 'smtp.163.com'
    port = 465
    recipient_email = recipient_email

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender_email
    msg['To'] = recipient_email

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, pwd)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()


def to_email(recipient_emails: list, text: str, transfer_pwd: str, sender_email: str) -> None:
    if transfer_pwd:
        for recipient_email in recipient_emails:
            for _ in range(3):
                try:
                    send_email(recipient_email, text, text, transfer_pwd, sender_email)
                    break
                except Exception as e:
                    print(f"邮件发送失败：{e}")
                time.sleep(5)


class FdtWarningApp:
    def __init__(self, real: bool = True) -> None:
        self.messages = []
        self.app: Optional[WebSocketApp] = None
        self.real = real
        # Initialize MongoDB connection
        self.db, error = connect_to_mongodb()
        if error:
            print(f"MongoDB connection failed: {error}")
        if self.real:
            self.thread_start()

    @staticmethod
    def on_message(_ws: WebSocket, msg: str) -> None:
        print(f"on_message: {msg}")

    def on_error(self, _ws: WebSocket, msg: str) -> None:
        print(f"on_error: {msg}")
        self.app.close()
        time.sleep(5)
        self.thread_start()

    def thread_start(self) -> None:
        self.app = WebSocketApp(
            # url="ws://172.16.16.70:7031",
            url="ws://172.16.16.76:7031",
            on_message=self.on_message,
            on_error=self.on_error,
        )
        t = threading.Thread(target=self.app.run_forever)
        t.start()
        print("connect")

    def send_msg(self) -> None:
        for msg in self.messages:
            try:
                self.app.send(json.dumps(msg))
                self.messages.remove(msg)
                print(f"send: {msg}")
            except Exception as e:
                print(f"error: {e}")

    def insert_db(self, args: tuple) -> None:
        try:
            document = SignalModel.create_document(*args)
            self.db["Signals"].insert_one(document)
        except Exception as e:
            print(f"MongoDB insertion error: {e}")

    def send_warning(self, symbol: str, direction: str, conditions: str, market: str,
                     warn_id: int = None, user: str = "", event: str = "early_warning") -> None:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = {
            "data": {
                "market": market,
                "symbol": symbol,
                "time": now,
                "direction": direction,
                "conditions": conditions,
                "id": warn_id if warn_id else int((time.time() - 20 * 365 * 24 * 3600) * 1000),
            },
            "event": event,
            "update_time": now,
            "user": user,
        }
        self.messages.append(msg)
        if self.real:
            self.send_msg()

        self.insert_db((
            msg['data']['symbol'], msg['data']['market'], msg['data']['time'],
            msg['data']['direction'], msg['data']['conditions'], msg['data']['id'],
        ))

    def hide_warning(self, warn_id: int, user: str = "", event: str = "hide_warning") -> None:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = {
            "data": {
                "id": warn_id
            },
            "event": event,
            "update_time": now,
            "user": user,
        }
        self.messages.append(msg)
        if self.real:
            self.send_msg()
