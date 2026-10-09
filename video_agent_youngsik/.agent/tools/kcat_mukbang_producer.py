import os
import sys
import time
from dotenv import load_dotenv

# Windows console UTF-8 patch for emojis and Korean characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from wan_video_maker import generate_wan_t2v
from tts_generator import generate_voiceover
from video_composer import compose_short_video
from youtube_auto_uploader import upload_video

OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "output_assets")

def produce_kcat_mukbang_episode(
    kfood_name: str = "Buldak Carbonara Spicy Fire Ramen",
    episode_num: int = 1,
    privacy_status: str = "public"
):
    """
    K-Cat Mukbang 쇼츠 에피소드 완전 무인 원스톱 제작 및 유튜브 배포 파이프라인
    """
    print("=" * 65)
    print(f"🐱🍲 [K-Cat Mukbang Episode #{episode_num} 무인 제작 파이프라인 가동]")
    print(f"🔥 타깃 K-Food 메뉴: {kfood_name}")
    print("=" * 65)

    # 1. Wan 2.1 고품질 프롬프트 설계
    video_prompt = (
        "Vertical 9:16 cinematic close-up video of an adorable fluffy chubby kitten wearing a tiny chef apron and bib, "
        "happily slurping a steaming bowl of glossy Korean carbonara spicy fire ramen noodles with melted stretchy cheese. "
        "Macro details of bright orange spicy noodles, appetizing food steam rising, delicious food shine, "
        "ultra-cute kitten facial expressions, bright cozy lighting, 4k ultra-realistic 3D Pixar aesthetic, viral mukbang"
    )

    # 2. 고에너지 글로벌 영문 내레이션 대본 설계
    narration_script = (
        "Chef Meow takes on the legendary Korean Buldak Fire Noodles! "
        "Watch this tiny fluffy kitten slurp the extra cheesy spicy ramen! "
        "Can he handle the heat till the very end?! "
        "Drop your favorite Korean food in the comments, and subscribe for daily bites!"
    )

    # 3. 비디오 렌더링 (Wan 2.1)
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

    # 2. 영상 모션 및 환경과 100% 동기화된 연속 순환 먹방 ASMR 사운드 생성
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
        # 기존 저장된 고품질 asmr 파일 폴백
        backup_asmr = os.path.join(OUTPUT_DIR, "kcat_ep1_asmr.mp3")
        if os.path.exists(backup_asmr):
            audio_path = backup_asmr
        else:
            return None

    # 5. 비디오 + 오디오 루프 믹싱 (FFmpeg)
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

    # 6. 유튜브 글로벌 SEO 패키징 & 자동 업로드
    print("\n[Step 4/4] 유튜브 알고리즘 최적화 자동 업로드...")
    title = f"Can Cute Kitten Handle Korean Buldak Fire Noodles?! 🌶️🍜 [Daily K-Food Mukbang #{episode_num}]"
    description = (
        f"Chef Meow takes on the viral Korean Carbonara Buldak Fire Ramen! 🌶️🔥\n"
        f"Can this tiny fluffy kitten survive the ultimate Korean spicy noodle challenge?!\n\n"
        f"🐾 Follow daily for delicious Korean street food & mukbangs!\n"
        f"👉 Hit Subscribe to keep Chef Meow well-fed!\n\n"
        f"#shorts #catmukbang #koreanfood #buldak #spicyramen #asmr #cutecat #foodie #mukbang #kfood"
    )
    tags = [
        "shorts", "cat mukbang", "korean food", "buldak ramen", 
        "spicy ramen", "asmr", "cute cat", "cat eating", 
        "mukbang", "kfood", "cute kitten", "spicy noodles"
    ]

    # Category ID: 15 (Pets & Animals)
    upload_res = upload_video(
        file_path=final_video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="15",
        privacy_status=privacy_status
    )

    if upload_res:
        video_id = upload_res.get("id")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print("=" * 65)
        print("🎉 [K-Cat Mukbang 1호 에피소드 배포 성공!]")
        print(f"🔗 유튜브 영상 URL: {video_url}")
        print("=" * 65)
        return upload_res
    else:
        print("❌ 유튜브 업로드 실패.")
        return None

if __name__ == "__main__":
    produce_kcat_mukbang_episode(episode_num=1, privacy_status="public")
