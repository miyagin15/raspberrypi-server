from flask import Flask
import threading
from request_manager import RequestDataManager
from routes import init_routes
from metric_collector import start_data_collection

# 最大保存件数とデータファイルの設定
MAX_RECORDS = 30
DATA_FILE = "request_data.json"

def create_app():
    app = Flask(__name__)

    app.jinja_env.globals.update(enumerate=enumerate)
    # リクエストデータ管理インスタンスを作成
    request_data_manager = RequestDataManager(DATA_FILE, MAX_RECORDS)

    # ルートを初期化
    init_routes(app, request_data_manager)

    return app

if __name__ == "__main__":
    # Flaskアプリケーションを作成
    app = create_app()

    # データ収集スレッドを開始
    threading.Thread(target=start_data_collection, daemon=True).start()

    # アプリケーションを起動
    app.run(debug=True, host='0.0.0.0', port=8080)
