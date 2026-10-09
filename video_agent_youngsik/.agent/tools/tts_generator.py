import os
import sys
import asyncio
from dotenv import load_dotenv

# Windows console UTF-8 patch for emojis and Korean characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

try:
    import edge_tts
except ImportError:
    print("❌ 패키지 없음: 'pip install edge-tts' 실행 요망")
    sys.exit(1)

load_dotenv()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output_assets")

async def _synthesize(text: str, voice: str, output_path: str, rate: str = "+0%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

def generate_voiceover(text: str, voice: str = "en-US-ChristopherNeural", output_filename: str = "voiceover.mp3", rate: str = "+5%"):
    """
    고품질 Edge-TTS 음성 생성
    - 추천 보이스:
      - en-US-ChristopherNeural (신뢰감 있고 박진감 넘치는 미국 남성)
      - en-US-GuyNeural (대중적인 미국 남성 캐주얼)
      - en-US-JennyNeural (밝고 세련된 미국 여성)
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target_path = os.path.join(OUTPUT_DIR, output_filename)

    print(f"🎙️ [TTS 음성 생성 중] 보이스: {voice} | 속도: {rate}")
    print(f"📝 대본: \"{text}\"")

    asyncio.run(_synthesize(text, voice, target_path, rate))

    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        print(f"✅ 음성 파일 생성 완료: {target_path} ({os.path.getsize(target_path)} bytes)")
        return target_path
    else:
        print("❌ 음성 파일 생성 실패!")
        return None

if __name__ == "__main__":
    sample_text = "Did this gadget just break the laws of physics?! This anti-gravity humidifier makes water flow upwards using pure optical illusion. Link in comments!"
    generate_voiceover(sample_text)
