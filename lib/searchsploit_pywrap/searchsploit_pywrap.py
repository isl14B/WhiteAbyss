import subprocess
import json

SEARCHSPLOIT_PATH = "/usr/local/bin/searchsploit"

def search(search_word: str) -> dict:
    # -jオプションでJSON形式でデータを出力
    cmd = "{} -j {}".format(SEARCHSPLOIT_PATH, search_word)

    p = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    # 検索結果をJSON形式からdict型に変換
    result = json.loads(p.stdout.decode('utf-8'))
    return result
