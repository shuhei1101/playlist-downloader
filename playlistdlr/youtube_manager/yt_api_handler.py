# import json
# import os
# from typing import List

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# import pickle

# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"
# YOUTUBE_API_KEY = config.API_KEY  # APIキーを設定

# class YtAPIHandler:
#     def __init__(self, credentials_file: str, token_file: str):
#         """
#         コンストラクタで認証情報を初期化
#         """
#         self.credentials_file = credentials_file
#         self.token_file = token_file
#         self.youtube = self.authenticate(credentials_file, token_file)

#     @staticmethod
#     def authenticate(credentials_file: str, token_file: str):
#         """
#         OAuth認証を行い、YouTube APIクライアントを返す
#         """
#         scopes = ["https://www.googleapis.com/auth/youtube"]
#         creds = None

#         # トークンファイルが存在する場合は読み込む
#         if os.path.exists(token_file):
#             with open(token_file, 'rb') as token:
#                 creds = pickle.load(token)

#         # 認証が必要な場合
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
#                 creds = flow.run_local_server(port=0)

#             # トークンを保存
#             with open(token_file, 'wb') as token:
#                 pickle.dump(creds, token)

#         return build("youtube", "v3", credentials=creds)

#     def create_playlist(self, title: str, description: str, privacy_status: str = "private") -> dict:
#         """
#         プレイリストを作成する
#         """
#         request_body = {
#             "snippet": {
#                 "title": title,
#                 "description": description
#             },
#             "status": {
#                 "privacyStatus": privacy_status
#             }
#         }
#         response = self.youtube.playlists().insert(
#             part="snippet,status",
#             body=request_body
#         ).execute()
#         return response

#     async def add_video_to_playlist(self, playlist_id: str, video_id: str) -> dict:
#         """
#         プレイリストに動画を追加する
#         """
#         request_body = {
#             "snippet": {
#                 "playlistId": playlist_id,
#                 "resourceId": {
#                     "kind": "youtube#video",
#                     "videoId": video_id
#                 }
#             }
#         }
#         response = self.youtube.playlistItems().insert(
#             part="snippet",
#             body=request_body
#         ).execute()
#         return response

#     def add_videos_to_playlist(self, playlist_id: str, video_ids: List[str]) -> List[dict]:
#         """
#         プレイリストに複数の動画を追加する
#         """
#         responses = []
#         for video_id in video_ids:
#             request_body = {
#                 "snippet": {
#                     "playlistId": playlist_id,
#                     "resourceId": {
#                         "kind": "youtube#video",
#                         "videoId": video_id
#                     }
#                 }
#             }
#             response = self.youtube.playlistItems().insert(
#                 part="snippet",
#                 body=request_body
#             ).execute()
#             responses.append(response)
#         return responses

#     def search_videos(self, query: str, max_results: int = 5) -> dict:
#         """
#         動画を検索する
#         """
#         response = self.youtube.search().list(
#             part="snippet",
#             q=query,
#             type="video",
#             maxResults=max_results
#         ).execute()
#         return response


# # 動作確認用
# if __name__ == "__main__":
#     # 認証情報ファイルとトークンファイルのパス
#     credentials_file = "credentials.json"  # Google Cloud Console からダウンロードしたファイル
#     token_file = "token.pickle"  # 認証後に生成されるトークンファイル

#     # YtAPIHandler のインスタンスを作成
#     yt_handler = YtAPIHandler(credentials_file, token_file)

#     # プレイリストを作成
#     playlist = yt_handler.create_playlist(
#         title="テストプレイリスト",
#         description="これはテスト用のプレイリストです",
#         privacy_status="private"
#     )
#     print("作成されたプレイリスト:", playlist)

#     # 動画を検索
#     search_results = yt_handler.search_videos(query="Python tutorial", max_results=3)
#     print("検索結果:", search_results)

#     # プレイリストに動画を追加
#     if search_results["items"]:
#         video_ids = [item["id"]["videoId"] for item in search_results["items"]]
#         responses = yt_handler.add_videos_to_playlist(playlist_id=playlist["id"], video_ids=video_ids)
#         print("プレイリストに追加された動画:", responses)
