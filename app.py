from flask import Flask
from request_manager import RequestDataManager
from routes import init_routes

# 最大保存件数とデータファイルの設定
MAX_RECORDS = 30
DATA_FILE = "request_data.json"

def create_app():
    app = Flask(__name__)

    # リクエストデータ管理インスタンスを作成
    request_data_manager = RequestDataManager(DATA_FILE, MAX_RECORDS)

    app.jinja_env.globals.update(enumerate=enumerate)

    # ルートを初期化
    init_routes(app, request_data_manager)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
