# WhiteAbyss
脆弱性診断Webアプリ

## Abstract
ユーザのブラウザのプラグインやツールなどの脆弱性を調べる

## Setup
###　必要なモジュール
- python 3.5.1  
- django 1.10.5  

### exploit-db
Linuxの場合， 以下のURLのHow to Install SearchSploit - Gitの項目の手順から， exploit-databaseをインストールする  
https://www.exploit-db.com/searchsploit/#installgit  

## Start
manage.pyがあるディレクトリで，　  
```
$ python manage.py runserver 0.0.0.0:8000  
```

- （接続する場合） localhost:8000
- （外部から接続する場合） {IPアドレス}:8000

## Image
* トップ画面
![image01.jpeg](https://raw.githubusercontent.com/isl14B/WhiteAbyss/develop/screen_shot/image01.jpeg)

* 診断結果画面
![image02.jpeg](https://raw.githubusercontent.com/isl14B/WhiteAbyss/develop/screen_shot/image02.jpeg)
