# 🍜 Knowledge 02: K-Cat Mukbang Production Playbook

## 1. 비주얼 프롬프트 엔지니어링 공식 (Wan 2.1)

아기 고양이의 귀여움과 음식의 먹음직스러움(Food Porn)을 극대화하는 **골든 프롬프트 템플릿**:

```text
Vertical 9:16 cinematic close-up video of an adorable fluffy chubby kitten wearing a tiny chef apron and bib,
happily slurping a steaming bowl of glossy Korean {K-FOOD_NAME} with {TOPPING_DETAILS}.
Macro details of {TEXTURE_DESCRIPTION}, appetizing food steam rising, delicious food shine,
ultra-cute kitten facial expressions, bright cozy lighting, 4k ultra-realistic 3D Pixar aesthetic, viral mukbang
```

### 프롬프트 파라미터 규칙
- **구도:** `Vertical 9:16 cinematic close-up` (쇼츠 화면 가득 차는 시각적 만족감)
- **캐릭터:** `adorable fluffy chubby kitten wearing a tiny chef apron and bib` (사랑스러움 극대화)
- **음식 디테일:** `glossy`, `steaming`, `food steam rising`, `delicious food shine` (식욕 자극)
- **스타일:** `4k ultra-realistic 3D Pixar aesthetic` (불쾌한 골짜기를 원천 차단하는 고급스러운 동화풍 실사)

---

## 2. 연속 순환 ASMR 오디오 믹싱 공식 (MMAudio)

### 🚨 불변 원칙: No Announcer, 100% Continuous ASMR
- 아나운서 및 인간 목소리는 100% 배제.
- 영상 전 구간(0초~12초) 동안 고양이의 먹는 모션과 맞물려 **`호로록 면치기 ➔ 오물오물 씹기 ➔ 꿀꺽 삼키기`** 소리가 1초의 침묵도 없이 무한 순환되어야 함.

### ASMR 프롬프트 공식
```text
Continuous rhythmic loud eating ASMR for {K-FOOD_NAME}, constant slurping and mouth chewing sounds,
wet delicious food chewing without pauses, ongoing slurps and crunchy chews, warm sizzling street food ambiance,
no speaking, no human voice, 100% continuous action synchronized eating sounds
```

### FFmpeg 동기화 명령어
```bash
ffmpeg -y -stream_loop -1 -i video.mp4 -stream_loop -1 -i asmr.mp3 -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -t 12 output.mp4
```

---

## 3. 글로벌 유튜브 알고리즘 SEO 공식

### 제목 (Title)
- **공식:** `[ASMR] Cute Kitten Slurping {Korean Food Name} 🍜🐾 | Mukbang Eating Sounds`
- **모바일 최적화:** 앞단 30자 이내에 `[ASMR]`, `Cute Kitten`, `음식명`을 명확히 노출하여 CTR 확보.

### 설명 (Description)
```text
🎧 WEAR HEADPHONES FOR BEST ASMR EXPERIENCE! 🐾
Watch this cute fluffy kitten slurping and eating {Korean Food Name}!
Delicious noodle slurping & chewing sounds with no talking.

🍜 Menu: {Korean Food Name} ({한국어 표기})
🐾 Chef: Chef Meow
🔔 Subscribe to MeowBite for daily satisfying K-Food ASMR mukbangs!

#shorts #catmukbang #asmr #asmreating #koreanfood #{food_tag} #cutecat #eatingsounds
```

### 태그 (Tags)
```json
["shorts", "cat mukbang", "asmr", "asmr eating", "korean food", "noodle slurp", "eating sounds", "cute cat", "cat asmr", "kfood"]
```
