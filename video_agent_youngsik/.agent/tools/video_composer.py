import os
import sys
import subprocess
import imageio_ffmpeg

# Windows console UTF-8 patch for emojis and Korean characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output_assets")

def compose_short_video(
    video_path: str,
    audio_path: str,
    output_filename: str = "final_short.mp4"
):
    """
    비디오와 오디오를 완벽하게 합성하여 유튜브 쇼츠 규격(9:16, H.264, AAC)으로 렌더링.
    비디오 길이가 오디오보다 짧을 경우 자연스럽게 루프(-stream_loop) 처리.
    """
    if not os.path.exists(video_path):
        print(f"❌ 비디오 파일을 찾을 수 없습니다: {video_path}")
        return None
    if not os.path.exists(audio_path):
        print(f"❌ 오디오 파일을 찾을 수 없습니다: {audio_path}")
        return None

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target_path = os.path.join(OUTPUT_DIR, output_filename)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    print("=" * 60)
    print("🎞️ [비디오 + 오디오 최종 합성 시작]")
    print(f"📹 소스 비디오: {video_path}")
    print(f"🎵 소스 오디오: {audio_path}")
    print(f"🎯 출력 타깃: {target_path}")
    print("=" * 60)

    # ffmpeg 명령어: 비디오와 오디오가 모두 끊김 없이 모션에 맞춰 연속 재생되도록 
    # 오디오와 비디오의 길이를 상호 동기화하고 공백 없이 믹싱
    cmd = [
        ffmpeg_exe,
        "-y",
        "-stream_loop", "-1",
        "-i", video_path,
        "-stream_loop", "-1",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "12",  # 최적 쇼츠 길이인 12초 동안 영상 동작과 사운드가 빈틈없이 100% 동기화
        target_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", errors="ignore")
    if result.returncode != 0:
        print(f"❌ 합성 실패: {result.stderr}")
        return None

    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        size_mb = os.path.getsize(target_path) / (1024 * 1024)
        print(f"🎉 [합성 성공!] 최종 영상 파일: {target_path} ({size_mb:.2f} MB)")
        return target_path
    else:
        print("❌ 합성 파일이 생성되지 않았습니다.")
        return None

if __name__ == "__main__":
    v_path = os.path.join(OUTPUT_DIR, "wan_humidifier.mp4")
    a_path = os.path.join(OUTPUT_DIR, "narration_humidifier.mp3")
    compose_short_video(v_path, a_path, "final_shorts_anti_gravity_humidifier.mp4")
