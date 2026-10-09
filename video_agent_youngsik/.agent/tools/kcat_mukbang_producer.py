import os
import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Windows console UTF-8 patch for emojis and Korean characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from wan_video_maker import generate_wan_t2v
from video_composer import compose_short_video
from youtube_auto_uploader import upload_video

OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "output_assets")

def get_optimal_publish_time():
    """
    글로벌(미국/유럽/아시아) 쇼츠 알고리즘 노출이 가장 극대화되는 황금 시간대 계산:
    - 타깃: 한국 시각 오전 9:00 (KST) = 미국 동부 저녁 8:00 (EDT) 프라임타임!
    - 새벽 4:00 (KST) 생성 후 오전 9:00 (KST) 공개 예약 시 유튜브 서버 인덱싱 시간 5시간 완벽 확보.
    - UTC 반환 형식: YYYY-MM-DDTHH:MM:SSZ
    """
    now_kst = datetime.now()
    target_today_kst = now_kst.replace(hour=9, minute=0, second=0, microsecond=0)
    if now_kst >= target_today_kst:
        target_kst = target_today_kst + timedelta(days=1)
    else:
        target_kst = target_today_kst

    target_utc = target_kst - timedelta(hours=9)
    return target_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

def produce_kcat_mukbang_episode(
    kfood_name: str = "Buldak Carbonara Spicy Fire Ramen",
    episode_num: int = 1,
    privacy_status: str = "public",
    schedule_publish: bool = True
):
    """
    K-Cat Mukbang 쇼츠 에피소드 완전 무인 원스톱 제작 및 유튜브 예약 배포 파이프라인
    """
    print("=" * 65)
    print(f"🐱🍲 [K-Cat Mukbang Episode #{episode_num} 무인 제작 파이프라인 가동]")
    print(f"🔥 타깃 K-Food 메뉴: {kfood_name}")
    print("=" * 65)

    # 1. Wan 2.1 고품질 프롬프트 설계
    video_prompt = (
        f"Vertical 9:16 cinematic close-up video of an adorable fluffy chubby kitten wearing a tiny chef apron and bib, "
        f"happily eating and slurping a steaming bowl of glossy Korean {kfood_name} with appetizing toppings. "
        f"Macro details of food texture, delicious steam rising, rich food shine, "
        f"ultra-cute kitten facial expressions, bright cozy lighting, 4k ultra-realistic 3D Pixar aesthetic, viral mukbang"
    )

    # 2. 비디오 렌더링 (Wan 2.1)
    print("\n[Step 1/4] Wan 2.1 비디오 렌더링 시작...")
    video_filename = f"kcat_ep{episode_num}_video.mp4"
    video_path = generate_wan_t2v(
        prompt=video_prompt,
        aspect_ratio="9:16",
        resolution="720p",
        output_filename=video_filename
    )
    if not video_path:
        print("❌ 비디오 렌더링 실패로 중단합니다.")
        return None

    # 3. 영상 모션 및 환경과 100% 동기화된 연속 순환 먹방 ASMR 사운드 생성
    print("\n[Step 2/4] 영상 동작 맞춤 연속 순환 먹방 ASMR 사운드 생성 중...")
    asmr_prompt = (
        f"Continuous rhythmic loud eating ASMR for {kfood_name}, constant slurping and mouth chewing sounds, "
        "wet delicious food chewing without pauses, ongoing slurps and crunchy chews, warm sizzling street food ambiance, "
        "no speaking, no human voice, 100% continuous action synchronized eating sounds"
    )

    audio_filename = f"kcat_ep{episode_num}_asmr.mp3"
    audio_path = os.path.join(OUTPUT_DIR, audio_filename)

    try:
        import fal_client
        import requests
        res = fal_client.subscribe(
            'fal-ai/mmaudio-v2/text-to-audio',
            arguments={'prompt': asmr_prompt, 'duration': 12},
            with_logs=True
        )
        audio_url = res['audio']['url']
        r = requests.get(audio_url)
        with open(audio_path, 'wb') as f:
            f.write(r.content)
        print(f"✅ 연속 동작 ASMR 생성 및 저장 완료: {audio_path}")
    except Exception as e:
        print(f"⚠️ AI ASMR 생성 실패 ({e}), 비상 ASMR 오디오로 폴백...")
        backup_asmr = os.path.join(OUTPUT_DIR, "kcat_ep1_asmr.mp3")
        if os.path.exists(backup_asmr):
            audio_path = backup_asmr
        else:
            return None

    # 4. 비디오 + 오디오 루프 믹싱 (FFmpeg)
    print("\n[Step 3/4] 비디오 & 오디오 싱크 최종 합성...")
    final_filename = f"kcat_ep{episode_num}_final_short.mp4"
    final_video_path = compose_short_video(
        video_path=video_path,
        audio_path=audio_path,
        output_filename=final_filename
    )
    if not final_video_path:
        print("❌ 최종 합성 실패로 중단합니다.")
        return None

    # 5. 유튜브 글로벌 SEO 패키징 & 자동 업로드
    print("\n[Step 4/4] 유튜브 알고리즘 최적화 자동 업로드...")
    title = f"[ASMR] Cute Kitten Eating Korean {kfood_name} 🍜🐾 [Daily K-Food Mukbang #{episode_num}]"
    description = (
        f"🎧 WEAR HEADPHONES FOR BEST ASMR EXPERIENCE! 🐾\n"
        f"Watch this cute fluffy kitten enjoying delicious Korean {kfood_name}!\n"
        f"Non-stop satisfying slurping & chewing ASMR sounds with no talking.\n\n"
        f"🍜 Menu: {kfood_name}\n"
        f"🐾 Chef: Chef Meow\n"
        f"🔔 Subscribe to MeowBite for daily satisfying K-Food ASMR mukbangs!\n\n"
        f"#shorts #catmukbang #koreanfood #asmr #asmreating #cutecat #eatingsounds #kfood"
    )
    tags = [
        "shorts", "cat mukbang", "korean food", "asmr", 
        "asmr eating", "eating sounds", "cute cat", "cat eating", 
        "mukbang", "kfood", "cute kitten"
    ]

    # Category ID: 15 (Pets & Animals)
    publish_at = get_optimal_publish_time() if schedule_publish else None

    upload_res = upload_video(
        file_path=final_video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="15",
        privacy_status=privacy_status,
        publish_at=publish_at
    )

    if upload_res:
        video_id = upload_res.get("id")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print("=" * 65)
        print(f"🎉 [K-Cat Mukbang 에피소드 #{episode_num} 배포 성공!]")
        if publish_at:
            print(f"⏰ [예약 발행 설정] 글로벌 골든타임 공개 예정: {publish_at} (KST 09:00 AM)")
        print(f"🔗 유튜브 영상 URL: {video_url}")
        print("=" * 65)
        return upload_res
    else:
        print("❌ 유튜브 업로드 실패.")
        return None

if __name__ == "__main__":
    produce_kcat_mukbang_episode(episode_num=2, schedule_publish=True)
