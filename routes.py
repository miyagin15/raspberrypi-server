from flask import request, render_template, jsonify
from datetime import datetime
from metric_collector import load_data_from_file
import os 
import json

ERROR_LOG_FILE = "error_log.json"

def init_routes(app, request_data_manager):
    # ヘッダーを追加する関数
    @app.after_request
    def add_ngrok_header(response):
        response.headers["ngrok-skip-browser-warning"] = "true"
        return response

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/error-log")
    def error_log():
        # エラーログを読み込む
        if os.path.exists(ERROR_LOG_FILE):
            with open(ERROR_LOG_FILE, "r") as f:
                try:
                    error_log = json.load(f)
                except json.JSONDecodeError:
                    error_log = []
        else:
            error_log = []

        return jsonify(error_log)
    
    # リクエスト履歴ページ
    @app.route("/request-history")
    def request_page():
        client_ip = request.remote_addr
        client_port = request.environ.get("REMOTE_PORT")
        user_agent = request.user_agent.string
        access_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # データの追加
        request_data_manager.add_request(client_ip, client_port, user_agent, access_time)

        # テンプレートをレンダリング
        return render_template(
            "request-history.html",
            request_count=request_data_manager.request_count,
            request_records=request_data_manager.request_records,
        )

    # ライブデータAPI
    @app.route("/api/live-data")
    def live_data_api():
        # ファイルからデータを読み取る
        live_data = load_data_from_file()
        return jsonify(live_data)
