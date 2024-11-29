import os
import json

class RequestDataManager:
    def __init__(self, data_file, max_records):
        self.data_file = data_file
        self.max_records = max_records
        self.request_records = []
        self.request_count = 0
        self.load_data()

    def load_data(self):
        """JSONファイルからリクエスト情報を読み込む"""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.request_records = data.get("records", [])
                self.request_count = data.get("count", 0)

    def save_data(self):
        """リクエスト情報をJSONファイルに保存する"""
        with open(self.data_file, "w") as file:
            json.dump({"records": self.request_records, "count": self.request_count}, file, indent=4)

    def add_request(self, client_ip, client_port, user_agent, access_time):
        """リクエスト情報を追加"""
        self.request_count += 1
        self.request_records.insert(
            0,
            {
                "IP Address": client_ip,
                "Port": client_port,
                "User Agent": user_agent,
                "Access Time": access_time,
            },
        )
        # 古いデータを削除
        if len(self.request_records) > self.max_records:
            self.request_records = self.request_records[:self.max_records]
        self.save_data()
