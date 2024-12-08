## 概要
GCPの動画解析AIサービスを使用し、動画の中のテキストを抽出し、
テキストファイル（.sbv）で出力する

## 目的
動画＋音楽＋字幕を主体とした動画で活動しているYoutuber向けに
海外の視聴者獲得のため、Youtubeに取り込むための翻訳ファイル作成を支援する。
※Youtube標準の翻訳機能では精度が低いため、より翻訳のニュアンスなどを向上することができる。

翻訳ファイルは再生時間と字幕をテキストファイルで整理する必要があるが、作業負荷が高いため、
動画からテキストファイルを生成することで作業負荷を軽減できる。

## アーキテクチャ
### 言語
- front (firebase auth -> python flask)
- backend-api (python flask)

### 外部API連携
- GCP VideoInteligence api

### CICD
-  Build
    - Docker Image Build
    - GCP Build　⇒　Artifact Registry
-  Deploy
    - GCP Deoploy　⇒　CloudRun

### 環境変数
- BUCKET_NAME
    - GCP Cloud StorageのBucket名を設定する
