import os
import sys
import time
import requests
from dotenv import load_dotenv

# Windows console UTF-8 patch for emojis and Korean characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

try:
    import fal_client
except ImportError:
    print("❌ 패키지 없음: 'pip install fal-client' 실행 요망")
    sys.exit(1)

load_dotenv()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output_assets")

def check_fal_key():
    fal_key = os.getenv("FAL_KEY")
    if not fal_key or fal_key.strip() == "":
        print("\n❌ [FAL_KEY 미등록] .env 파일에 FAL_KEY가 설정되어 있지 않습니다!")
        print("📌 발급 가이드:")
        print(" 1. https://fal.ai 접속 및 회원가입")
        print(" 2. Dashboard > Keys에서 API Key 생성")
        print(" 3. .env 파일의 FAL_KEY= 항목에 붙여넣기")
        return False
    return True

def generate_wan_t2v(
    prompt: str,
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    output_filename: str = None
):
    """
    Wan 2.1 Text-to-Video 생성
    - endpoint: fal-ai/wan-t2v
    - aspect_ratio: "16:9" (유튜브 일반 영상) or "9:16" (쇼츠)
    - resolution: "720p" or "480p"
    """
    if not check_fal_key():
        return None

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not output_filename:
        timestamp = int(time.time())
        output_filename = f"wan_t2v_{timestamp}.mp4"

    target_path = os.path.join(OUTPUT_DIR, output_filename)

    print("=" * 60)
    print("🎬 [Wan 2.1 Text-to-Video 렌더링 시작]")
    print(f"📝 프롬프트: {prompt}")
    print(f"📐 비율/해상도: {aspect_ratio} ({resolution})")
    print("=" * 60)

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(f"  [Wan 2.1 연산] {log.get('message', '')}")

    try:
        handler = fal_client.subscribe(
            "fal-ai/wan-t2v",
            arguments={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution
            },
            with_logs=True,
            on_enqueue=lambda req_id: print(f"⏳ 큐 대기 시작 (Request ID: {req_id})...")
        )

        result = handler
        video_url = result.get("video", {}).get("url")

        if not video_url:
            print(f"❌ 영상 생성 결과 URL 없음: {result}")
            return None

        print(f"\n🎉 렌더링 완료! 비디오 다운로드 중: {video_url}")
        res = requests.get(video_url, stream=True)
        res.raise_for_status()

        with open(target_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"💾 영상 파일 저장 성공: {target_path}")
        return target_path

    except Exception as e:
        print(f"❌ Wan 2.1 T2V 생성 실패: {e}")
        return None

def generate_wan_i2v(
    image_path: str,
    prompt: str,
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    output_filename: str = None
):
    """
    Wan 2.1 Image-to-Video 생성 (실물 제품 이미지 기반 영상화)
    - endpoint: fal-ai/wan-i2v
    """
    if not check_fal_key():
        return None

    if not os.path.exists(image_path):
        print(f"❌ 입력 이미지 파일을 찾을 수 없습니다: {image_path}")
        return None

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not output_filename:
        timestamp = int(time.time())
        output_filename = f"wan_i2v_{timestamp}.mp4"

    target_path = os.path.join(OUTPUT_DIR, output_filename)

    print("=" * 60)
    print("🎬 [Wan 2.1 Image-to-Video 렌더링 시작]")
    print(f"🖼️ 소스 이미지: {image_path}")
    print(f"📝 모션 프롬프트: {prompt}")
    print(f"📐 비율/해상도: {aspect_ratio} ({resolution})")
    print("=" * 60)

    try:
        print("📤 이미지 Fal.ai 스토리지 업로드 중...")
        image_url = fal_client.upload_file(image_path)
        print(f"✅ 이미지 업로드 완료: {image_url}")

        handler = fal_client.subscribe(
            "fal-ai/wan-i2v",
            arguments={
                "image_url": image_url,
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution
            },
            with_logs=True,
            on_enqueue=lambda req_id: print(f"⏳ 큐 대기 시작 (Request ID: {req_id})...")
        )

        result = handler
        video_url = result.get("video", {}).get("url")

        if not video_url:
            print(f"❌ 영상 생성 결과 URL 없음: {result}")
            return None

        print(f"\n🎉 렌더링 완료! 비디오 다운로드 중: {video_url}")
        res = requests.get(video_url, stream=True)
        res.raise_for_status()

        with open(target_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"💾 영상 파일 저장 성공: {target_path}")
        return target_path

    except Exception as e:
        print(f"❌ Wan 2.1 I2V 생성 실패: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        if check_fal_key():
            print("✅ FAL_KEY 환경 변수가 설정되어 있습니다.")
    else:
        print("Wan 2.1 비디오 생성 유틸리티")
        print("사용법:")
        print("  python wan_video_maker.py --check")
