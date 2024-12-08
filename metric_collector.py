import datetime
import random
import time
import json
import os
import traceback

# JSONファイルのパス
DATA_FILE = "metric.json"

# データ取得間隔 (秒)
DATA_INTERVAL = 60

# 1分間に取得されるデータ数
DATA_PER_MINUTE = 60 // DATA_INTERVAL
# 1時間に取得されるデータ数
DATA_PER_HOUR = DATA_PER_MINUTE * 60
# 24時間に取得されるデータ数
DATA_PER_DAY = DATA_PER_HOUR * 24

ERROR_LOG_FILE = "error_log.json"


# データを保存する関数
def save_data_to_file(data):
    temp_file = DATA_FILE + ".tmp"
    try:
        with open(temp_file, "w") as f:
            json.dump(data, f)
        os.replace(temp_file, DATA_FILE)  # 安全に元のファイルを置き換える
    except (TypeError, ValueError) as e:
        error_message = "Error saving data to file: " + str(e)
        print(error_message)
        save_error_log(error_message)


def save_error_log(error_message):
    # エラー情報を作成
    error_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "error_message": error_message,
        "traceback": traceback.format_exc(),  # スタックトレースを記録
    }

    # エラーログを読み込む
    if os.path.exists(ERROR_LOG_FILE):
        with open(ERROR_LOG_FILE, "r") as f:
            try:
                error_log = json.load(f)
            except json.JSONDecodeError:
                error_log = []
    else:
        error_log = []

    # エラーログに追加し、直近10件に制限
    error_log.append(error_entry)
    error_log = error_log[-10:]  # 直近10件のみ保持

    # エラーログを保存
    with open(ERROR_LOG_FILE, "w") as f:
        json.dump(error_log, f, indent=4)


# データを読み込む関数
def load_data_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                content = f.read().strip()  # ファイルの内容を取得
                if content:  # ファイルが空でないか確認
                    return json.loads(content)  # JSONデータを読み込む
            except json.JSONDecodeError as e:
                # JSONフォーマットが壊れている場合は空のリストを返す
                error_message = (
                    "JSONDecodeError:" + str(e) + "Resetting data to empty list."
                )
                print(error_message)
                save_error_log(error_message)
                return []
    return []  # ファイルが存在しない場合も空のリストを返す


# ラズパイでデータを取得する関数
def get_raspberry_pi_data():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as t:
            temp = int(t.read()) / 1000  # 温度取得
        with open("/proc/stat") as r:
            stats = r.readlines()
            stat = [line.strip().split() for line in stats if "cpu" in line]
            total_time = sum(int(x) for x in stat[0][1:])
            idle_time = int(stat[0][4])
            busy_time = total_time - idle_time
            cpu_usage = round((busy_time / total_time) * 100, 2)  # CPU使用率計算
    except Exception as e:
        # テスト用データ（Raspberry Pi以外の場合のフォールバック）
        temp = round(random.uniform(40, 80), 2)
        cpu_usage = round(random.uniform(0, 100), 2)

    return {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "temperature": temp,
        "cpu_usage": cpu_usage,
    }


# データ収集を開始する関数
def start_data_collection():
    # 初期データの読み込み
    live_data = load_data_from_file()

    while True:
        data = get_raspberry_pi_data()
        live_data.append(data)

        # 古いデータを削除（スライスを使用）
        live_data = live_data[-DATA_PER_DAY:]  # 最新の DATA_PER_DAY 件のみ保持

        # データをファイルに保存
        save_data_to_file(live_data)

        # データ取得間隔
        time.sleep(DATA_INTERVAL)
