from flask import request, render_template
from datetime import datetime

def init_routes(app, request_data_manager):
    @app.route("/")
    def index():
        client_ip = request.remote_addr
        client_port = request.environ.get("REMOTE_PORT")
        user_agent = request.user_agent.string
        access_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # データの追加
        request_data_manager.add_request(client_ip, client_port, user_agent, access_time)

        # テンプレートをレンダリング
        return render_template(
            "index.html",
            request_count=request_data_manager.request_count,
            request_records=request_data_manager.request_records,
        )
