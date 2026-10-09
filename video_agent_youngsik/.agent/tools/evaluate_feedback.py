import os
import sys
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Windows console UTF-8 patch for emojis and Korean characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEM_FILE = os.path.join(BASE_DIR, "..", "memory", "upload_history.json")
REWARD_DIR = os.path.join(BASE_DIR, "..", "memory", "reward")
PUNISH_DIR = os.path.join(BASE_DIR, "..", "memory", "punishment")

sys.path.insert(0, BASE_DIR)
try:
    from youtube_auto_uploader import get_authenticated_service
except ImportError:
    get_authenticated_service = None

def evaluate_video_metrics():
    """
    업로드된 비디오의 24시간 실시간 통계를 YouTube Data API로 조회하고
    성과에 따라 강화학습(RL) 보상(Reward) / 처벌(Punishment) 오답 노트를 자동 갱신합니다.
    """
    if not os.path.exists(MEM_FILE):
        print("ℹ️ 업로드 히스토리 파일이 없습니다.")
        return

    with open(MEM_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    if not history:
        print("ℹ️ 평가할 영상 레코드가 비어 있습니다.")
        return

    youtube = get_authenticated_service() if get_authenticated_service else None
    os.makedirs(REWARD_DIR, exist_ok=True)
    os.makedirs(PUNISH_DIR, exist_ok=True)

    updated_count = 0
    now = datetime.now()

    for record in history:
        video_id = record.get("video_id")
        upload_time_str = record.get("uploaded_at")
        status = record.get("status")

        # 이미 평가 완료된 레코드는 건너뜀
        if status == "evaluated" or not video_id:
            continue

        # 업로드 시간 확인 (최소 24시간 경과 또는 수동 점검)
        try:
            uploaded_at = datetime.fromisoformat(upload_time_str)
            hours_elapsed = (now - uploaded_at).total_seconds() / 3600
        except Exception:
            hours_elapsed = 25  # 파싱 실패 시 즉시 평가 허용

        print(f"\n📊 [성과 평가 검사] Video ID: {video_id} (경과 시간: {hours_elapsed:.1f}시간)")

        # YouTube Data API로 실시간 지표 수집
        views = 0
        likes = 0
        comments = 0

        if youtube:
            try:
                res = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
                items = res.get("items", [])
                if items:
                    stats = items[0].get("statistics", {})
                    views = int(stats.get("viewCount", 0))
                    likes = int(stats.get("likeCount", 0))
                    comments = int(stats.get("commentCount", 0))
                    print(f"📈 [실시간 지표] 조회수: {views:,}회 | 좋아요: {likes:,}개 | 댓글: {comments:,}개")
            except Exception as e:
                print(f"⚠️ 지표 수집 에러: {e}")

        meta = record.get("metadata", {})
        title = meta.get("youtube_title", "제목 없음")

        summary = {
            "video_id": video_id,
            "title": title,
            "views": views,
            "likes": likes,
            "comments": comments,
            "evaluated_at": now.isoformat(),
            "hours_elapsed": round(hours_elapsed, 1)
        }

        # 24시간 기준 성과 임계값 (Shorts 기준: 10,000뷰 이상 = 바이럴 성공, 미만 = 개선 필요)
        SUCCESS_THRESHOLD = 5000

        if views >= SUCCESS_THRESHOLD:
            summary["verdict"] = "REWARD (성공)"
            summary["feedback"] = "썸네일/후크 시각적 어그로 성공. 동일한 캐릭터 연출 및 유사 K-Food 메뉴를 시리즈로 연속 확장할 것."
            with open(os.path.join(REWARD_DIR, "success_log.txt"), "a", encoding="utf-8") as f:
                f.write(json.dumps(summary, ensure_ascii=False) + "\n")
            print(f"🏆 [REWARD 등록 완료] '{title}' 성과 우수!")
        else:
            summary["verdict"] = "PUNISHMENT (개선 필요)"
            summary["feedback"] = "초반 2초 스와이프 이탈 발생 가능성. 더 자극적인 색감의 K-Food(치즈 분출, 매운맛 리액션 등)와 강렬한 사운드 훅 보강 필요."
            with open(os.path.join(PUNISH_DIR, "fail_log.txt"), "a", encoding="utf-8") as f:
                f.write(json.dumps(summary, ensure_ascii=False) + "\n")
            print(f"📝 [PUNISHMENT 오답노트 등록] '{title}' 개선 포인트 기록 완료.")

        record["status"] = "evaluated"
        record["final_stats"] = {"views": views, "likes": likes, "comments": comments}
        updated_count += 1

    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    print(f"\n✅ 총 {updated_count}개 영상 평가 및 강화학습 DB 업데이트 완료.")

if __name__ == "__main__":
    evaluate_video_metrics()
