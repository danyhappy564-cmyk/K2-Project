# K2-Project

> **SPT 4.1.5 용 대우정밀 K2 계열 소총 모드**
> 제작: **C33** / **R_F**

한국군 제식소총 K2 와 그 파생형을 Escape from Tushonka (SPT) 에 이식하는 프로젝트입니다.
모델은 [GAMGO](https://sketchfab.com/gamgo_studio) 님의 CC 라이선스 에셋을 사용합니다
> (모델별로 CC-BY-4.0 / CC-BY-SA-4.0 로 다름 — 아래 라이선스 절 확인).

---

## 원본 모델 · 라이선스 (필독)

세 모델 모두 **GAMGO** (Seoul, Republic of Korea / 3D Artist) 제작입니다.

| 모델 | Sketchfab |
|---|---|
| K2 | https://sketchfab.com/3d-models/daewoo-k2-258d30e1f3e04c13a60abd916425b0c2 |
| K2C3 | https://sketchfab.com/3d-models/k2c3-39bb1eeed4b949c7a620b16667262faf |
| K2C4 | https://sketchfab.com/3d-models/k2c4-f23ce806f7324a7088a84e7bd859eaf5 |

### ⚠️ 세 모델의 라이선스가 전부 다릅니다 (2026-09-16 재확인)

세 `license.txt` 를 전부 대조했습니다. **CC 두 종류 + Sketchfab 고유 라이선스 하나,
셋이 전부 다릅니다.**

| 모델 | 라이선스 (동봉 `license.txt`) | 요구사항 |
|---|---|---|
| **K2** | **Sketchfab Standard** (CC 아님!) | 저작자 표시 불필요, 상업적 이용·파생물 제작 허용<br>**단, 원본을 "독립 파일로" 재배포·재판매 금지** |
| K2C3 | CC-BY-4.0 | 저작자 표시만 하면 상업적 이용까지 허용 |
| **K2C4** | CC-BY-SA-4.0 | 저작자 표시 **+ 파생물도 동일 라이선스로 공개 (ShareAlike)** |

#### K2C4 — ShareAlike (SA)

**계획(부품 갈아끼우기)상 SA 조항은 반드시 트리거됩니다.** CC-BY-SA 의 "각색물(adapted
material)"은 리깅·절단·재배열·수정을 전부 포함합니다 — K2C4 를 부품으로 잘라 다른
모델과 합치는 순간, 그대로 내보내든 일부만 쓰든 상관없이 각색물이 됩니다. 방향은
문제없습니다 — CC-BY(K2C3) 를 CC-BY-SA(K2C4) 결과물에 포함시키는 건 허용되고, 반대만
금지입니다. → **최종 결합 3D 에셋은 CC-BY-SA-4.0 으로 배포합니다.**

#### K2 — Sketchfab Standard, 조치 완료(회수 결정)

Standard 라이선스 원문(검색 결과 기준, [Sketchfab License Agreement](https://sketchfab.com/licenses)):

> *"You may not use the 3D asset in a way that allows others to use or access
> the 3D asset as a stand-alone file (for instance, no sub-license or sale by
> you to others is allowed)."*

**모드(컴파일된 Unity AssetBundle)에 녹여 넣는 건 문제없습니다** — 이건 3D 마켓플레이스
업계에서 "Standard" 가 정확히 겨냥하는 용도(게임에 구워 넣기)입니다.

**문제였던 건 이 저장소가 공개(public) 상태로 K2 원본을 독립 파일로 배포하고 있던
것**입니다. Standard 라이선스가 금지하는 "stand-alone file 로 접근 가능하게 하는 것"
에 해당할 수 있었습니다(K2C3/K2C4 는 CC-BY 계열이라 원래 문제없었음).

✅ **2026-09-16 결정: 모델 분석이 끝났으므로 두 Release 를 삭제해서 회수합니다.**
분석에 쓴 가벼운 파일만 git 에 남기고 나머지는 그냥 지웁니다 — 아래
[원본 에셋(Release)](#원본-에셋-release--분석-완료로-회수-예정) 절 참조.

라이선스가 요구하는 크레딧 문구입니다. **배포물·공유처 어디에나 아래를 그대로 포함해야 합니다.**

```
This work is based on "Daewoo K2" (https://sketchfab.com/3d-models/daewoo-k2-258d30e1f3e04c13a60abd916425b0c2)
by GAMGO (https://sketchfab.com/gamgo_studio) — Sketchfab Standard License
(https://sketchfab.com/licenses)

This work is based on "K2C3" (https://sketchfab.com/3d-models/k2c3-39bb1eeed4b949c7a620b16667262faf)
by GAMGO (https://sketchfab.com/gamgo_studio) licensed under CC-BY-4.0
(http://creativecommons.org/licenses/by/4.0/)

This work is based on "K2C4" (https://sketchfab.com/3d-models/k2c4-f23ce806f7324a7088a84e7bd859eaf5)
by GAMGO (https://sketchfab.com/gamgo_studio) licensed under CC-BY-SA-4.0
(http://creativecommons.org/licenses/by-sa/4.0/)
```

이 결과물 전체를 배포할 때는 위 셋을 다 붙이는 동시에, **자체 라이선스 표시로
CC-BY-SA-4.0 을 명시**합니다 (SA 조항이 걸린 K2C4 를 포함하므로 결과물 전체가
BY-SA 를 따라야 함). Standard 라이선스 원문은 제가 직접 페이지를 열지 못하고(사내
프록시가 sketchfab.com 을 막음) **검색 결과로 재구성한 것**이라 정확한 표현은 형이
직접 [sketchfab.com/licenses](https://sketchfab.com/licenses) 에서 한 번 대조해
주세요.

### 제작자 댓글 (보관용 전사, 2026-09-16 스크린샷 확보)

Sketchfab 모델 페이지, 3년 전 댓글. **"게임 모드 제작에 써도 되는지"를 직접 질문하고
받은 답변**이라 이 프로젝트 용도와 정확히 일치합니다.

> **dotolwi** (3년 전)
> 게임에 모드를 만들려고 하는데 혹시 이 모델을 사용해도 괜찮은지 여쭐수 있을까요?
>
> **GAMGO** (@gamgo, Model author, 3년 전)
> @dotolwi 답변이 늦어 죄송합니다. 제 모델중 다운로드 가능한 모든 3D 모델은 제한없이
> 이용가능하십니다. 덧글 감사합니다

원본 스크린샷은 별도 보관합니다 — 계정이나 모델이 내려가면 이 전사만 근거로 남습니다.
다만 이 댓글이 라이선스 조건(특히 K2C4 의 SA)을 공식적으로 면제해주는 문서는 아니므로,
**동봉된 `license.txt` 를 1차 근거로 삼고 이 댓글은 보강 근거로 취급합니다.**

> ✅ K2 의 `license.txt` 확인 완료 (2026-09-16) — **Sketchfab Standard**, CC 아님.
> 위 라이선스 표를 최종으로 삼습니다.

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

## 현재 상태 (2026-09-21 갱신)

| 단계 | 상태 |
|---|---|
| 모델 확보 (K2 / K2C3 / K2C4, FBX·glTF) | ✅ |
| 라이선스 확인 (3종 전부) | ✅ 셋 다 다름 — 위 표 참조 |
| **K2 · K2C3 · K2C4 모델 구조 분석** | ✅ 완료 |
| 라이선스 위험 해소 (Release 삭제 결정) | ✅ 완료 — 실제 삭제 완료 |
| 블렌더 부품 분리·묶기 (**K2C3만**) | 🟡 v012까지 진행 — 212개 조각 분리, 임시 리깅(본 5개), HK416 재장전 클립 리타기팅 프리뷰. 미분류 부품 16개 남음. **K2·K2C4는 아직 시작 전** |
| Unity 프리팹·번들 | 🟡 `k2c3_visual.bundle` 정적 외형 빌드 성공, **인게임 확인 결과 크기가 비정상(너무 큼)·부품이 뭉쳐 보이는 버그 발견** (아래 "다음 작업 배정" 참고). 부착 지점(mod_*)·손 IK·콜라이더 있는 진짜 게임용 프리팹도 아직 없음 |
| 서버 모드 — K2C3 시험용 무기 1개 | ✅ 서버 등록/API 검증 통과, SPT 4.1.6에 설치, **인게임 확인 완료**(피스키퍼 판매·외형 스왑 작동 확인) |
| 서버 모드 — 부품 갈아끼우기(K2/K2C4 슬롯 시스템) | 🟡 `Server/Generate-Family-Data.ps1` + `K2Mod.cs` 확장 코드 작성 완료, **`dotnet build` 실제 성공(경고 0, 오류 0)까지 검증**. 로컬 PC에서 스크립트 실행 + `Verify-Server.ps1` 검증만 남음 |
| 클라 모드(외형 스왑) | ✅ 시험판 존재 + **로컬 `dotnet build` 성공, 인게임 작동 확인**(HK416 메시를 K2C3 외형으로 덮어씌우는 방식, 부품 교체 시 겉모습은 아직 그대로) |
| 빌드 인프라 (`.csproj`/`.sln`) | ✅ `Server/Client`의 `.csproj`가 실제로 존재하지 않던 것을 발견해 복원, `K2-Project.sln` 신규 생성, Release 빌드 시 SPT 폴더로 자동 배포(SAIN 방식), 사람마다 다른 설치 경로는 `LocalSettings.props`로 한 번만 설정 |

### 다음 작업 배정

- **C33님 (최우선, 2026-09-21 실전 테스트로 발견)**: 인게임에서 K2C3 외형이 **너무 크고 부품이 뭉쳐 보이는 버그** 확인됨. `Blender/export_visual.py`가 참조하는 `K2C3_DraftRig`/`K2C3_DonorFitRig`에 465mm 실척 보정(v006에서 찾은 scale≈0.126)이 안 걸려있는 것으로 보임 — 자세한 진단은 `Docs/AI-Knowledge/NOTES.md` 8절 참고. 그다음 K2C3 블렌더 정리 마무리(미분류 16개, 가동부 확정) + **K2 원본/K2C4 단축형도 K2C3처럼 부품 분리·정리 시작** + Unity에서 부착 지점(mod_*)·손 IK·탄피배출구 있는 실제 게임용 프리팹 완성.
- **R_F님**: ✅ K2C3 시험용 무기 인게임 확인 완료(피스키퍼 판매/외형 스왑 작동 확인, 크기 버그는 위 항목). ✅ `Server`/`Client` `.csproj` 복원 + 로컬 빌드 성공까지 완료. 남은 것: 로컬 PC에서 `Server/Generate-Family-Data.ps1` 실행 → `dotnet build` → `Verify-Server.ps1`로 K2/K2C4 부품 갈아끼우기 데이터 검증.

---

## 모델 분석 결과 (3종 전체, 실측 완료 2026-09-16)

| | K2 (원본) | K2C3 | K2C4 (단축) |
|---|---|---|---|
| 삼각형 | 9,646 | 12,749 | 12,636 |
| 메시 개수 | 3 | 2 | 2 |
| **loose part** | **48** | **212** | **184** |
| 본 / 애니메이션 | 없음 / 없음 | 없음 / 없음 | 없음 / 없음 |
| 정점 속성 | POSITION·NORMAL·TANGENT·TEXCOORD_0 (공통) | 〃 | 〃 |
| 텍스처 | 2048² PBR | 2048² PBR | 2048² PBR |
| 노드 이름 | ⚠️ **손상됨** (아래 참고) | 정상 | 정상 |

**셋 다 loose part 가 살아있어 블렌더 `P` → `By Loose Parts` 로 즉시 분리됩니다.**
K2 가 48개로 K2C3(212)·K2C4(184) 보다 훨씬 적은 건 문제가 아니라 실물 반영입니다 —
K2 의 핸드가드는 레일 이빨 없는 통짜 플라스틱이라 애초에 나눠질 이유가 적습니다.

**K2 의 노드 이름은 복구 불가능합니다.** 원래 있었을 한글 이름이 유니코드 대체문자
(U+FFFD, `\xef\xbf\xbd`) 로 바뀌어 있는데, 이건 원본 바이트 자체가 사라졌다는 뜻이라
되돌릴 수 없습니다. 부품 정체는 이름이 아니라 **월드 좌표 위치**로 판별했으므로
분석 결과에는 영향 없습니다.

### 부품 위치 지도 (0% = 총구, 100% = 개머리판 끝)

**K2C3** (최대 조각 2,048 tri = 핸드가드):

| 구간 | 삼각형 | 추정 정체 |
|---|---|---|
| 0 ~ 50% | 676 | **총열** |
| 16 ~ 25% | 486+ | 가늠쇠 · 가스블록 |
| 26 ~ 70% | **2,048** | **쿼드레일 핸드가드** |
| 30 ~ 50% | 작은 조각 139개 | 피카티니 레일 이빨 |
| 50 ~ 74% | **1,091** | **총몸(리시버)** |
| 51 ~ 65% | 135 / 117 / 90 | **장전손잡이 · 노리쇠 후보** |
| 64 ~ 73% | 390 | 권총손잡이 |
| 72 ~ 93% | 422 | 버퍼튜브 |
| 85 ~ 100% | 560 | **개머리판** |

**K2 (원본)** — 레일 없는 플라스틱 핸드가드, 고정 개머리판:

| 구간 | 삼각형 | 추정 정체 |
|---|---|---|
| 0 ~ 50% | 676 | **총열** |
| 16 ~ 21% | 522 | 가늠쇠 · 가스블록 |
| 24 ~ 51% | 942+656+264 | **플라스틱 핸드가드** (K2C3 의 레일 대응 부위) |
| 50 ~ 74% | 997 / 1,004 | **총몸(리시버)** |
| 52 ~ 65% | 144 / 135 / 90 | **장전손잡이 · 노리쇠 후보** |
| 65 ~ 75% | 446 | 권총손잡이 |
| **73 ~ 100%** | **1,062** | **측면 접이식 개머리판** (K2C3/C4 의 신축식보다 한 덩어리) |

**K2C4 (단축)** — K2C3 와 같은 계열이지만 총열이 짧고 핸드가드가 더 큽니다:

| 구간 | 삼각형 | 추정 정체 |
|---|---|---|
| 0 ~ 40% | 676 | **단축 총열** (K2C3 의 0~50% 보다 짧음 → 310mm 반영) |
| 13 ~ 18% | 486+156 | 가늠쇠 · 가스블록 |
| **25 ~ 65%** | **2,596** | **쿼드레일 핸드가드** (K2C3 보다 더 큼 — 짧은 총열만큼 앞으로 더 나와 있음) |
| 40 ~ 68% | 1,091 / 780 | **총몸(리시버)** |
| 41 ~ 60% | 135 / 156 / 144 | **장전손잡이 · 노리쇠 후보** |
| 57 ~ 68% | 390 | 권총손잡이 |
| 66 ~ 92% | 422 | 버퍼튜브 |
| **82 ~ 100%** | 560 / 114 | **신축식 개머리판** |

**세 모델 모두 핸드가드·총열·총몸·개머리판이 독립 셸입니다** → 목표 슬롯 구성(위 표)이
성립합니다. 특히 K2 의 접이식 개머리판(1,062 tri, 한 덩어리)과 K2C3/K2C4 의 신축식
개머리판(560+114 tri, 두 조각)이 **분리 방식 자체가 다르다**는 것도 확인했습니다 —
Unity 리깅 때 서로 다른 접힘/신축 로직이 필요합니다.

자세한 근거와 방법론은 [`Docs/K2-WEAPON-MOD-PROJECT.md`](Docs/K2-WEAPON-MOD-PROJECT.md) 참조.

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

## 저장소 구조 (2026-09-21 정리)

```
README.md                이 문서
INSTALL_KO.md            서버 시험판 설치 안내
VISUAL_TEST_KO.md         외형 시험(클라 플러그인) 설치·확인 안내
K2-Project.sln            Visual Studio/Rider용 솔루션(Server+Client 프로젝트)
LocalSettings.props.example  실제 SPT 설치 경로 설정 예시 — 복사해서
                              LocalSettings.props로 저장하고 본인 경로로 수정
                              (사람마다 다르므로 이 파일 자체는 git에 안 올라감)
Build-Release.ps1          Build-Visual.ps1 + Package-Visual.ps1을 순서대로 실행
Build-Visual.ps1           Unity 번들 + 클라/서버 dotnet build
Package-Visual.ps1         빌드 결과를 03_Releases/ 배포 ZIP으로 묶음(공유용)
                            — .sln으로 Release 빌드하면 이거 없이도 SPT 폴더로
                            자동 배포됨(csproj의 DeployToSpt 타겟, SAIN 방식)
Verify-Server.ps1          실행 중인 로컬 서버 API로 실제 등록 상태 검증
NuGet.Config                nuget.org 명시 지정(SPTushonka.* 패키지가 실제로
                             여기서 받아지는 것을 dotnet build로 확인함)

Server/                   서버 모드 (C#, SPTarkov.Server.*, net10.0)
  K2.Server.csproj           프로젝트 파일 (2026-09-21 복원 — 아래 "빌드" 참고)
  K2Mod.cs                  아이템/프리셋/상점 등록. Server/data/*.json을 읽음
  Generate-Data.ps1          K2C3 시험용 무기 데이터 생성(로컬 SPT DB 필요)
  Generate-Family-Data.ps1   K2/K2C4 부품 갈아끼우기 데이터 생성(로컬 SPT DB 필요)
  data/                       위 두 스크립트가 만드는 JSON (weapon/preset/assort/family_*)

Client/                   클라 BepInEx 플러그인 (K2.Visual, netstandard2.1)
  K2.Visual.csproj            프로젝트 파일 (2026-09-21 복원)
  VisualPlugin.cs             Harmony로 무기 생성 시점을 패치해 외형 번들을 덮어씌움

Unity/                    외형 번들 빌드용 Unity 프로젝트 (Unity 2022.3.43f1)
  Assets/Editor/BuildK2Visual.cs   번들 빌드 에디터 스크립트

Blender/                  블렌더 작업 스크립트 (MCP로 실행) + 작업현황.md
Assets-Local/             블렌더 작업 파일(.blend)·원본 glTF 등 (무거움, 이 컴퓨터 로컬 전용)
Artifacts/                빌드 로그·번들 산출물
UnityBuildCheck/          Unity DLL 대상 별도 컴파일 검사용 (Unity/처럼 자동 생성, 커밋 안 함)

Docs/                     기획·참고 문서 (예전 이름 "k2 project/", 2026-09-21에 정리)
  K2-WEAPON-MOD-PROJECT.md   기획·인수인계 문서 (분석 전문)
  모델링크 및 정보.md          원본 링크 / 제작진 / 진행도 기록
  로드맵.png  로드맵 1.png  로드맵 2.png      분석 결과 요약 이미지
  모델 사진/  K2.png  K2C3.png  K2C4.png     변형별 외형
  모델 원본 데이터/            분석에 쓴 가벼운 원본(scene.gltf·license.txt)
  AI-Knowledge/               Claude·c33님의 Codex(GPT)가 공유하는 이 프로젝트 전용
                              지식 메모(NOTES.md) — 중앙 KB(Cluade_For_spt)는 R_F 전용이라
                              Codex가 못 보므로, 이 저장소 안에 둬서 둘 다 읽게 함
```

### 원본 에셋 (Release) — 분석 완료로 회수 예정

FBX 원본은 **103MB** 라 git 에 커밋할 수 없어 Release 로 올렸습니다.

| 태그 | 파일 | 크기 | 상태 |
|---|---|---|---|
| `fbx` | `k2_fbx.7z` | 103 MB | ✅ **삭제 완료** (2026-09-16) |
| `glTF` | `k2_glTF.7z` (K2·K2C3·K2C4 전부) | 24.5 MB | ✅ **삭제 완료** (2026-09-16) |

**2026-09-16: 분석이 끝나서 두 Release 를 삭제했습니다.** (`GET /releases` 로 빈 배열
확인) K2 는 Sketchfab Standard 라이선스라 원본을 독립 파일로 계속 공개해 둘 이유가
없어지는 게 가장 큰 이유였습니다(K2C3/K2C4 는 CC-BY 계열이라 원래도 문제없었지만,
어차피 분석 끝난 원본을 같이 정리). **git 커밋과 달리 Release 는 지우면 히스토리에
남지 않고 그냥 없어집니다** — 지금 이 레포엔 K2 원본이 독립 파일로 존재하지 않습니다.

- 분석에 실제로 쓴 가벼운 파일(`scene.gltf` · `license.txt`, 6개 합쳐 48KB)은 삭제
  전에 git 본체의 [`Docs/모델 원본 데이터/`](Docs/모델%20원본%20데이터/)
  에 커밋해서 남겨뒀습니다 — 법적 근거 원본과 부품 지도 재계산용 설계도는 계속
  보관됩니다. `.bin`(정점 데이터)·텍스처·FBX 는 git 에 없고 팀원 로컬에만 있습니다
- **새로 원본이나 큰 산출물을 공유해야 하면**: 팀 내부 협업(형·C33)이 목적이면 Release
  대신 DM/사설 채널로 주고받는 걸 권합니다 — 이번처럼 K2 급 라이선스 조건이 있는
  에셋을 다시 public Release 에 올리면 같은 문제가 재발합니다

**원본 3D 에셋은 git 본체에 커밋하지 마세요.** 한 번 커밋하면 히스토리에 영구히 박혀서
Release 와 달리 지워도 안 없어집니다. 앞으로 나올 빌드된 AssetBundle 등 큰 바이너리는
전부 Release 로 올리고, 이번처럼 **다 쓴 뒤 지우면 됩니다.**

- git 본체 → 소스코드, 문서, `scene.gltf`, `license.txt` (텍스트라 가볍고 diff 가 됨)
- Release → FBX·텍스처 원본, 빌드된 AssetBundle (다 쓰면 지워도 무방)
- Git LFS 는 쓰지 않습니다 (무료 한도가 3D 에셋엔 금방 참)

---

## 참여 방법

공동작업 프로젝트입니다. 작업하기 전에 아래만 지켜주세요.

1. **작업 진행은 `Docs/모델링크 및 정보.md` 의 `<제작진행도>` 에 한 줄씩 기록**
   (날짜 / 작업자 / 무엇을 했는지)
2. **큰 바이너리는 커밋 금지** → Release 에 올리고 README 표에 추가
3. **문서는 한국어**로 작성
4. CC-BY 크레딧 문구는 **어떤 배포물에서도 빼지 않기**
5. 모델 분석을 새로 돌렸다면 결과를 `K2-WEAPON-MOD-PROJECT.md` 에 반영

### 다음 할 일

- [x] K2 · K2C4 도 glTF 구조 분석 (부품 지도 완성) — 2026-09-16
- [x] K2 · K2C4 의 `license.txt` 확인 — 셋 다 라이선스가 다름을 확인
- [x] Sketchfab 제작자 댓글 스크린샷 보관 (+ 전사 기록)
- [x] **K2 공개 배포 방식 결정 + 실제 삭제 완료** — `fbx`·`glTF` Release 둘 다 삭제
      (2026-09-16, 사용자가 GitHub 웹에서 직접 진행)
- [ ] `sketchfab.com/licenses` 원문 직접 대조 (Standard 조항, 지금은 검색 결과로 재구성함)
- [ ] 서버 모드 뼈대 생성 (모델과 무관하게 선행 가능)
- [ ] SPT 4.1.5 DB 에서 HK416A5 실제 템플릿 ID 확인 (기억에 의존 금지)

---

## 환경 메모

- 대상: **SPT 4.1.5** / 서버 `net10.0` / 클라(BepInEx) `netstandard2.1`
- NuGet 패키지는 `SPTushonka.*` 인데 **어셈블리 이름은 여전히 `SPTarkov.*`**
- 아이템 등록은 반드시 `OnLoadOrder.Preload` — 그 이후 단계면 서버가
  `DatabaseModifiedAfterCutoffException` 으로 죽습니다
