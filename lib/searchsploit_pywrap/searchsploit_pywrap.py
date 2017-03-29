import subprocess
import json

SEARCHSPLOIT_PATH = "/usr/local/bin/searchsploit"

def search(search_word: str) -> dict: 
    cmd = "{} -j {}".format(SEARCHSPLOIT_PATH ,search_word) # -jオプションでJSON形式でデータを出力
    
    p = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    result = json.loads(p.stdout.decode('utf-8')) # 検索結果をJSON形式からdict型に変換
    return result
