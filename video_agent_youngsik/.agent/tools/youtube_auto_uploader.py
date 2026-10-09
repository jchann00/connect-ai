import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Windows console UTF-8 patch for emojis and Korean characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ 패키지 없음: 'pip install google-api-python-client google-auth-oauthlib google-auth-httplib2' 실행 요망")
    sys.exit(1)

load_dotenv()

# OAuth 2.0 권한 스코프 (업로드 및 채널 관리)
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube"
]

TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "youtube_token.json")
MEM_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "upload_history.json")

def get_client_secret_file():
    """OAuth 클라이언트 시크릿 파일 경로 확인"""
    env_path = os.getenv("YOUTUBE_CLIENT_SECRET_FILE")
    if env_path and os.path.exists(env_path):
        return env_path
    
    # 기본 탐색 경로들
    candidates = [
        "client_secret.json",
        "client_secrets.json",
        os.path.join(os.path.dirname(__file__), "..", "..", "client_secret.json"),
        os.path.join(os.path.dirname(__file__), "..", "memory", "client_secret.json")
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def get_authenticated_service():
    """YouTube Data API 인증 및 서비스 객체 생성"""
    creds = None
    token_full_path = os.path.abspath(TOKEN_PATH)

    # 1. 기존 토큰 로드
    if os.path.exists(token_full_path):
        try:
            creds = Credentials.from_authorized_user_file(token_full_path, SCOPES)
        except Exception as e:
            print(f"⚠️ 기존 토큰 로드 실패: {e}. 재인증을 시도합니다.")
            creds = None

    # 2. 토큰 유효성 검사 및 갱신/신규 인증
    if creds and not creds.valid:
        if creds.expired and creds.refresh_token:
            print("🔄 만료된 인증 토큰 갱신 중...")
            try:
                creds.refresh(Request())
                with open(token_full_path, "w", encoding="utf-8") as token_file:
                    token_file.write(creds.to_json())
                print("✅ 갱신된 토큰 저장 완료")
            except Exception as e:
                print(f"⚠️ 토큰 갱신 실패: {e}. 재인증을 시도합니다.")
                creds = None

    if not creds or not creds.valid:
        secret_file = get_client_secret_file()
        if not secret_file:
            print("\n❌ [인증 실패] 'client_secret.json' 파일을 찾을 수 없습니다!")
            print("📌 설정 가이드:")
            print(" 1. Google Cloud Console (https://console.cloud.google.com/) 접속")
            print(" 2. 'YouTube Data API v3' 라이브러리 사용 설정")
            print(" 3. [사용자 인증 정보] -> [OAuth 클라이언트 ID 만들기] (유형: 데스크톱 앱/Desktop App)")
            print(" 4. 다운로드한 JSON 파일을 프로젝트 루트 디렉터리에 'client_secret.json'으로 저장해주세요.")
            return None

        print(f"🌐 브라우저를 통한 Google 계정 인증을 시작합니다 (시크릿 파일: {secret_file})...")
        flow = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
        creds = flow.run_local_server(port=0)

        # 토큰 파일 저장
        os.makedirs(os.path.dirname(token_full_path), exist_ok=True)
        with open(token_full_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
        print(f"✅ 인증 토큰이 성공적으로 저장되었습니다: {token_full_path}")

    return build("youtube", "v3", credentials=creds)

def check_channel_connection():
    """현재 연동된 유튜브 채널의 기본 정보 및 상태 확인"""
    youtube = get_authenticated_service()
    if not youtube:
        return None

    try:
        response = youtube.channels().list(
            part="snippet,statistics,contentDetails",
            mine=True
        ).execute()

        items = response.get("items", [])
        if not items:
            print("⚠️ 연동된 유튜브 채널 정보를 찾을 수 없습니다.")
            return None

        channel = items[0]
        title = channel["snippet"]["title"]
        channel_id = channel["id"]
        custom_url = channel["snippet"].get("customUrl", "없음")
        subscribers = channel["statistics"].get("subscriberCount", "0")
        view_count = channel["statistics"].get("viewCount", "0")
        video_count = channel["statistics"].get("videoCount", "0")

        print("=" * 60)
        print("🎯 [YouTube 채널 연동 확인 성공]")
        print(f"📺 채널명: {title}")
        print(f"🆔 채널 ID: {channel_id}")
        print(f"🔗 채널 핸들/URL: @{custom_url} (https://www.youtube.com/channel/{channel_id})")
        print(f"👥 구독자 수: {int(subscribers):,}명 | 총 조회수: {int(view_count):,}회 | 등록 영상: {video_count}개")
        print("=" * 60)

        return {
            "channel_id": channel_id,
            "title": title,
            "subscribers": subscribers,
            "view_count": view_count,
            "video_count": video_count
        }
    except HttpError as e:
        print(f"❌ YouTube API 호출 에러: {e}")
        return None

def upload_video(file_path, title, description, tags=None, category_id="22", privacy_status="private", publish_at=None):
    """
    비디오 파일을 유튜브에 업로드하고 식별 정보를 반환합니다.
    - category_id: 22 (People & Blogs), 24 (Entertainment), 15 (Pets & Animals), 28 (Science & Technology)
    - privacy_status: 'private', 'unlisted', 'public'
    - publish_at: ISO 8601 UTC 문자열 (예: '2026-10-10T00:00:00Z'). 설정 시 자동으로 private로 업로드 후 해당 시각에 public 공개.
    """
    if not os.path.exists(file_path):
        print(f"❌ 업로드할 파일이 존재하지 않습니다: {file_path}")
        return None

    youtube = get_authenticated_service()
    if not youtube:
        return None

    if tags is None:
        tags = []

    status_obj = {
        "privacyStatus": "private" if publish_at else privacy_status,
        "selfDeclaredMadeForKids": False
    }
    if publish_at:
        status_obj["publishAt"] = publish_at

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": status_obj
    }

    if publish_at:
        print(f"\n🚀 [영상 예약 업로드 시작] '{title}' (예약 공개 일시: {publish_at})")
    else:
        print(f"\n🚀 [영상 업로드 시작] '{title}' (상태: {privacy_status})")
    media = MediaFileUpload(
        file_path,
        mimetype="video/*",
        chunksize=1024 * 1024 * 4,  # 4MB chunks
        resumable=True
    )

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"⏳ 업로드 진행률: {progress}%", end="\r")

    video_id = response.get("id")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n🎉 [업로드 성공!] 영상 URL: {video_url}")

    # 히스토리 기록
    record_history(video_id, title, description, tags, privacy_status, file_path)
    return response

def record_history(video_id, title, description, tags, privacy_status, file_path):
    """업로드 내역을 memory/upload_history.json에 누적 기록"""
    history = []
    mem_full_path = os.path.abspath(MEM_FILE)
    if os.path.exists(mem_full_path):
        try:
            with open(mem_full_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    history.append({
        "video_id": video_id,
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
        "uploaded_at": datetime.now().isoformat(),
        "status": "published" if privacy_status == "public" else "private",
        "file_path": file_path,
        "metadata": {
            "youtube_title": title,
            "description": description,
            "tags": tags
        }
    })

    os.makedirs(os.path.dirname(mem_full_path), exist_ok=True)
    with open(mem_full_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    print("📝 [기록 완료] upload_history.json에 성공적으로 추가되었습니다.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        check_channel_connection()
    else:
        print("YouTube Auto Uploader 유틸리티")
        print("명령어 예시:")
        print("  python youtube_auto_uploader.py --check   # 채널 연동 확인")
