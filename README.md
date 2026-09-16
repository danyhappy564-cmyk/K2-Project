# K2-Project

> **SPT 4.1.5 용 대우정밀 K2 계열 소총 모드**
> 제작: **C33** / **R_F**

한국군 제식소총 K2 와 그 파생형을 Escape from Tushonka (SPT) 에 이식하는 프로젝트입니다.
모델은 [GAMGO](https://sketchfab.com/gamgo_studio) 님의 CC-BY-4.0 에셋을 사용합니다.

---

## 원본 모델 · 라이선스 (필독)

세 모델 모두 **GAMGO** (Seoul, Republic of Korea / 3D Artist) 제작입니다.

| 모델 | Sketchfab |
|---|---|
| K2 | https://sketchfab.com/3d-models/daewoo-k2-258d30e1f3e04c13a60abd916425b0c2 |
| K2C3 | https://sketchfab.com/3d-models/k2c3-39bb1eeed4b949c7a620b16667262faf |
| K2C4 | https://sketchfab.com/3d-models/k2c4-f23ce806f7324a7088a84e7bd859eaf5 |

**라이선스: CC-BY-4.0** — 저작자 표시만 하면 **상업적 이용까지 허용**됩니다.
(K2C3 동봉 `license.txt` 에서 확인. `requirements: Author must be credited. Commercial use is allowed.`)

라이선스가 요구하는 크레딧 문구입니다. **배포물·공유처 어디에나 아래를 그대로 포함해야 합니다.**

```
This work is based on "K2C3" (https://sketchfab.com/3d-models/k2c3-39bb1eeed4b949c7a620b16667262faf)
by GAMGO (https://sketchfab.com/gamgo_studio) licensed under CC-BY-4.0
(http://creativecommons.org/licenses/by/4.0/)

This work is based on "Daewoo K2" (https://sketchfab.com/3d-models/daewoo-k2-258d30e1f3e04c13a60abd916425b0c2)
by GAMGO (https://sketchfab.com/gamgo_studio) licensed under CC-BY-4.0
(http://creativecommons.org/licenses/by/4.0/)

This work is based on "K2C4" (https://sketchfab.com/3d-models/k2c4-f23ce806f7324a7088a84e7bd859eaf5)
by GAMGO (https://sketchfab.com/gamgo_studio) licensed under CC-BY-4.0
(http://creativecommons.org/licenses/by/4.0/)
```

제작자가 Sketchfab 댓글로도 *"제 모델중 다운로드 가능한 모든 3D 모델은 제한없이
이용가능하십니다"* 라고 직접 밝혔습니다. **해당 댓글은 스크린샷으로 보관해 두세요** —
계정이나 모델이 내려가면 근거가 사라집니다.

> ⚠️ **TODO**: `license.txt` 를 직접 확인한 것은 **K2C3 뿐**입니다. K2 · K2C4 의 동봉
> 라이선스 파일도 확인해서 동일한지 대조 필요.

---

## 만들려는 것

세 모델이 **총몸·권총손잡이·방아쇠울을 공유**하고 가구(핸드가드·개머리판·총열)만 다릅니다.
그래서 **별개 총 3정이 아니라 "총 1정 + 갈아끼우는 부품"** 으로 갑니다. 타르코프답고
파밍 재미도 생깁니다.

| 모델 | 실제 계보 | 특징 |
|---|---|---|
| **K2** | 원본 K2 | 플라스틱 리브 핸드가드, 고정 가늠쇠, 측면 접이식 고정 개머리판, 레일 없음, 465mm |
| **K2C3** | 사실상 **K2C1** | 쿼드레일 핸드가드, 상부 피카티니, AR식 신축+접이 개머리판, 465mm |
| **K2C4** | 사실상 **K2C** | 쿼드레일, 상부 레일, 신축 개머리판, **310mm 단축 총열** |

> `K2C3` / `K2C4` 는 공식 제식명이 아닙니다. 공식 계보는 K2 → K2C(단축) → K2C1(레일) 이고,
> 제작자 임의 명명으로 보입니다.

### 목표 슬롯 구성

| 슬롯 | 선택지 | 부품 출처 |
|---|---|---|
| `mod_barrel` | 465mm / **310mm 단축** | K2·K2C3 / K2C4 |
| `mod_handguard` | 플라스틱 리브 / **쿼드레일** | K2 / K2C3·K2C4 |
| `mod_stock` | K2 접이식 고정 / **AR 신축+접이** | K2 / K2C3·K2C4 |
| `mod_muzzle` | K2 소염기 / 표준 5.56 총구장치 | — |
| `mod_magazine` | **STANAG — 기존 M4 탄창 재사용** | 신규 에셋 불필요 |
| `mod_sight_front` / `_rear` | 고정 가늠쇠·가늠자 / 레일 BUIS | K2 / 공용 |
| `mod_mount` | **쿼드레일 핸드가드에만** (손전등·레이저·전방손잡이) | K2C3·K2C4 |
| `mod_scope` | **상부 레일에만** | K2C3·K2C4 |

1번(원본 K2) 구성으로 싸게 사서 → 레일 핸드가드 + 신축 개머리판 + 단축 총열을 물려 →
3번(K2C4) 으로 개조하는 흐름입니다.

---

## 현재 상태

| 단계 | 상태 |
|---|---|
| 모델 확보 (K2 / K2C3 / K2C4, FBX·glTF) | ✅ |
| 라이선스 확인 | ✅ CC-BY-4.0 (K2C3 기준) |
| **K2C3 모델 구조 분석** | ✅ 완료 |
| K2 · K2C4 모델 분석 | ⬜ 대기 |
| 블렌더 부품 분리·묶기 | ⬜ |
| Unity 프리팹·번들 | ⬜ |
| 서버 모드 (템플릿·슬롯·로케일·상인) | ⬜ |

---

## 모델 분석 결과 (K2C3 기준, 실측)

```
generator : Sketchfab-13.74.0 / glTF 2.0   (원본 FBX: K2C3_AR.FBX)
nodes 9 / meshes 2 / skins 없음 / animations 없음 / materials 2 / textures 8
```

| 항목 | 값 | 평가 |
|---|---|---|
| 삼각형 | **12,749** | 모드 무기로 충분. 바닐라보단 단순 |
| 메시 | 2개 (`Object001` 8,657 / `Body` 4,092) | 기능별이 아니라 앞/뒤 + 머티리얼 분할 |
| **loose part** | **212개** (194 + 18) | ⭐ **부품 셸이 살아있음** |
| 본(뼈대) | 없음 | 새로 만들어야 함 |
| 애니메이션 | 없음 | EFT 는 자체 애니를 쓰므로 무관 |
| 정점 속성 | `POSITION` `NORMAL` `TANGENT` `TEXCOORD_0` | 노멀맵 재굽기 불필요 |
| 텍스처 | 2048² PBR ×2 세트 | 그대로 활용 가능 |

**212 loose part 가 이 프로젝트의 성패를 갈랐습니다.** 통짜로 구워진 메시였다면 3D 툴로
잘라내고 구멍 막고 UV 수리까지 해야 했는데, 하드서피스 모델이라 셸이 그대로 살아있습니다.
→ 블렌더에서 `P` → `By Loose Parts` **한 번으로 212개 오브젝트**가 됩니다.
남는 일은 **자르기가 아니라 고르고 묶기**입니다.

### 부품 위치 지도 (0% = 총구, 100% = 개머리판 끝)

| 구간 | 삼각형 | 추정 정체 |
|---|---|---|
| 0 ~ 50% | 676 | **총열** |
| 16 ~ 25% | 486+ | 가늠쇠 · 가스블록 |
| 26 ~ 70% | **2,048** | **쿼드레일 핸드가드** (최대 조각) |
| 30 ~ 50% | 작은 조각 **139개** | 피카티니 레일 이빨 |
| 50 ~ 74% | **1,091** | **총몸(리시버)** |
| 51 ~ 65% | 135 / 117 / 90 | **장전손잡이 · 노리쇠 후보** |
| 64 ~ 73% | 390 | 권총손잡이 |
| 72 ~ 93% | 422 | 버퍼튜브 |
| 85 ~ 100% | 560 | **개머리판** |

핸드가드·총열·총몸·개머리판이 **전부 독립 셸** → 위의 부품 교체 구조가 성립합니다.

자세한 근거와 방법론은 [`k2 project/K2-WEAPON-MOD-PROJECT.md`](k2%20project/K2-WEAPON-MOD-PROJECT.md) 참조.

---

## K2 실물 스펙 → EFT 매핑

| 항목 | 실물 | EFT |
|---|---|---|
| 탄약 | 5.56×45mm NATO | `Caliber556x45NATO` |
| 총열 | 465mm / 단축 310mm | 탄속 ↑, 인체공학 ↓ |
| 무게 | 3.26kg (K2) / 3.6kg (K2C1) | 조립 완성 기준 역산 |
| 연사속도 | 700~900 rpm | `bFirerate` 750 |
| 탄속 | 915 m/s (K100탄) | 총열 배율 |
| 작동방식 | 장스트로크 가스 피스톤 + 회전 노리쇠 | M4(직충식)보다 반동·총구상승 ↑ |
| 탄창 | **STANAG** | M4 탄창 재사용 |
| 개머리판 | 측면 접이식 / AR 신축+접이 | `Foldable: true` |

**클론 베이스: HK416A5 권장** — 5.56 + 가스 피스톤 + STANAG + 접이식 개머리판 + 풀오토로
슬롯 구조가 K2 에 거의 1:1 입니다. M4A1 은 직충식이라 반동 성격이 다르고 개머리판이
안 접힙니다.

---

## 작업 분담

| 단계 | 담당 | 난이도 | 비고 |
|---|---|---|---|
| ① 모델 평가 | 완료 | — | |
| ② 블렌더: loose part 분리 → 기능별 묶기 | — | 중 | **자르는 게 아니라 고르는 작업** |
| ③ Unity: EFT 프리팹 계층 + `mod_*` 트랜스폼 + 번들 빌드 | — | **높음 — 진짜 산** | Unity 버전 정확히 맞출 것 |
| ④ 서버 모드 전부 | — | 중 | **②③ 과 무관하게 선행 가능** |

### ③ 에서 필요한 것 (EFT 무기 프리팹 요구사항)

- `mod_*` 부착 지점 트랜스폼 — 없으면 부착물 자체가 불가능
- `fireport` (총구 화염), `shell_eject` (탄피 배출)
- 손 IK 타겟 — 안 맞으면 캐릭터가 총을 허공에 듦
- 노리쇠 · 장전손잡이 = **움직이는 부품**이므로 반드시 별개 오브젝트
- EFT 셰이더로 머티리얼 변환 (Sketchfab 은 PBR 표준)
- LOD + 콜라이더
- 정확한 Unity 버전으로 AssetBundle 빌드

### 권장 진행 순서 — "리스킨 먼저"

서버 쪽은 모델이 있든 없든 **동일**합니다. 그래서 이 순서가 낭비가 없습니다.

1. **먼저** 서버 모드를 완성하고 프리팹 경로를 HK416 으로 걸어둠
   → 바로 게임에 **K2 스탯**으로 나옵니다 (모양만 HK416)
2. **나중에** 번들이 나오면 **프리팹 경로 문자열 하나만 교체**

누군가 Unity 를 붙들고 있는 동안 나머지는 이미 돌아가는 상태가 됩니다.

---

## 저장소 구조

```
README.md                                  이 문서
k2 project/
  K2-WEAPON-MOD-PROJECT.md                 기획·인수인계 문서 (분석 전문)
  모델링크 및 정보.md                        원본 링크 / 제작진 / 진행도 기록
  로드맵.png  로드맵 1.png  로드맵 2.png      분석 결과 요약 이미지
  모델 사진/  K2.png  K2C3.png  K2C4.png     변형별 외형
```

### 원본 에셋 (Release)

FBX 원본은 **103MB** 라 git 에 커밋할 수 없어 Release 로 올립니다.

| 태그 | 파일 | 크기 |
|---|---|---|
| [`fbx`](https://github.com/danyhappy564-cmyk/K2-Project/releases/tag/fbx) | `k2_fbx.7z` | 103 MB |

**원본 3D 에셋은 git 에 커밋하지 마세요.** 한 번 커밋하면 히스토리에 영구히 박혀서,
나중에 지워도 모든 클론이 계속 내려받습니다. 큰 바이너리는 전부 Release 로 갑니다.

- git 본체 → 소스코드, 문서, `scene.gltf`, `license.txt` (텍스트라 가볍고 diff 가 됨)
- Release → FBX·텍스처 원본, 빌드된 AssetBundle
- Git LFS 는 쓰지 않습니다 (무료 한도가 3D 에셋엔 금방 참)

---

## 참여 방법

공동작업 프로젝트입니다. 작업하기 전에 아래만 지켜주세요.

1. **작업 진행은 `k2 project/모델링크 및 정보.md` 의 `<제작진행도>` 에 한 줄씩 기록**
   (날짜 / 작업자 / 무엇을 했는지)
2. **큰 바이너리는 커밋 금지** → Release 에 올리고 README 표에 추가
3. **문서는 한국어**로 작성
4. CC-BY 크레딧 문구는 **어떤 배포물에서도 빼지 않기**
5. 모델 분석을 새로 돌렸다면 결과를 `K2-WEAPON-MOD-PROJECT.md` 에 반영

### 다음 할 일

- [ ] K2 · K2C4 도 glTF 구조 분석 (부품 지도 완성용)
- [ ] K2 · K2C4 의 `license.txt` 확인
- [ ] Sketchfab 제작자 댓글 스크린샷 보관
- [ ] 서버 모드 뼈대 생성 (모델과 무관하게 선행 가능)
- [ ] SPT 4.1.5 DB 에서 HK416A5 실제 템플릿 ID 확인 (기억에 의존 금지)

---

## 환경 메모

- 대상: **SPT 4.1.5** / 서버 `net10.0` / 클라(BepInEx) `netstandard2.1`
- NuGet 패키지는 `SPTushonka.*` 인데 **어셈블리 이름은 여전히 `SPTarkov.*`**
- 아이템 등록은 반드시 `OnLoadOrder.Preload` — 그 이후 단계면 서버가
  `DatabaseModifiedAfterCutoffException` 으로 죽습니다
