# K2-Project 공용 지식 메모 (Claude ↔ Codex/GPT)

이 파일은 **이 저장소(K2-Project) 작업에만 해당하는 지식**을 R_F님 쪽 Claude와
C33님 쪽 Codex(GPT)가 같이 보고 쓰는 곳입니다. R_F님의 중앙 지식 베이스
(`Cluade_For_spt` 저장소)는 R_F님 계정 전용이라 Codex가 접근할 수 없어서,
이 저장소 안에 별도로 둡니다. 여러 SPT 프로젝트에 공통으로 적용될 만큼
일반적인 지식이면 (두 번째로 같은 걸 다른 프로젝트에서도 마주치면) 그건
`Cluade_For_spt`의 `docs/kb/`로 옮겨질 수 있습니다 — 이 파일은 **K2-Project
한정** 지식만 다룹니다.

새 세션(Claude든 Codex든)은 이 프로젝트에서 작업을 시작하기 전에 이 파일을
먼저 훑어보세요. 작업하다 새로 알게 된 함정/결정이 있으면 여기에 추가하고,
최신 항목이 위로 오게 정렬하세요.

---

## 2026-09-21 — 서버 슬롯 시스템(K2/K2C4) 착수, 몇 가지 중요한 함정

### 1. 이 클라우드/컨테이너 세션에는 실제 게임이 없다
`Server/Generate-Data.ps1`·`Server/Generate-Family-Data.ps1`·`Verify-Server.ps1`은
모두 **로컬 PC(Windows, 실제 SPT 설치 + 서버 실행 중)에서만** 동작한다. 이유:
- `Generate-*.ps1`은 `../../02_Resources/SPT/SPT-4.1.5/SPT_Runtime/SPT_Data/database`
  (실제 게임 DB, 저장소 밖 상대 경로)를 직접 읽는다.
- `Verify-Server.ps1`은 `https://127.0.0.1:6978`(또는 6969)의 **실행 중인 서버**에
  API로 붙는다.
- Unity 빌드는 실제 Unity 라이선스 + 에디터가 필요하다(현재상태.md 참고).

그래서 클라우드 Claude 세션이 할 수 있는 건 **코드/데이터 스키마 작성**까지고,
"실제로 서버가 뜨는지 / dotnet build가 되는지"는 항상 로컬 PC에서 확인해야 한다.
클라우드 세션이 이 사실을 모르고 "빌드 검증 완료"라고 보고하면 거짓 보고가
되니 주의.

### 2. `.gitignore`의 "*.csproj"가 Server/Client의 손으로 쓴 csproj까지 삼켰다
원래 `.gitignore`의 `*.csproj`는 Unity가 자동 생성하는 걸 지우려는 규칙이었는데,
범위가 저장소 전체라서 `Server/K2.Server.csproj`·`Client/K2.Visual.csproj`(둘 다
사람이 직접 작성한 실제 프로젝트 파일)까지 **한 번도 git에 커밋된 적이 없었다.**
2026-09-21에 `Unity/*.csproj`·`UnityBuildCheck/*.csproj`로 범위를 좁혔지만,
**원본 .csproj 파일 내용 자체는 아무도 복원 못 했다** — 로컬에 그 파일을 갖고
있는 사람(R_F님 또는 C33님)이 다음에 커밋할 때 `git add Server/K2.Server.csproj
Client/K2.Visual.csproj`로 직접 올려야 한다. (`UnityBuildCheck/*.csproj`는 의도적으로
계속 무시 — Unity DLL 대상 컴파일 검사용 스캐폴드라 자동 생성/폐기 대상.)

이번에 `K2-Project.sln`(루트)을 새로 만들어서 두 프로젝트를 참조하게 했다 —
IDE(Visual Studio/Rider)에서 열 때 편하려고 만든 것이고, 실제 빌드는 여전히
`Build-Visual.ps1`이 `dotnet build`로 각 csproj를 직접 빌드한다(.sln 경유 안 함).

### 3. NuGet 패키지 소스는 이 저장소에 없다
`NuGet.Config`는 `<clear/>`만 있고 실제 패키지 소스가 없다 — 즉 SPTarkov 서버
SDK(`SPTushonka.*` 패키지, 실제 어셈블리 이름은 `SPTarkov.*`)를 어디서 받는지는
**로컬 PC의 전역 NuGet 설정에만 있다.** 이 정보가 저장소에 없으므로, 클라우드
세션이 `dotnet restore/build`를 시도해도 패키지를 못 받아서 실패한다(SDK가
설치돼 있어도 마찬가지). 이 문제를 만나면 "환경이 막혀서 못 함"이 맞는
진단이니, 로컬 PC에서 검증하라고 안내할 것 — 잘못된 패키지 소스를 추측해서
넣지 말 것.

### 4. mod_barrel / mod_handguard / mod_sight_rear는 무기 본체가 아니라 "리시버" 아이템에 달려 있다
`Server/data/preset.json`(실제 서버 DB에서 뽑은, 검증된 HK416A5 기본 프리셋)을
보면 구조가 이렇다:

```
무기 루트(WeaponId, d21900...0001)
├─ mod_pistol_grip, mod_magazine, mod_reciever, mod_stock, mod_charge  ← 무기 루트에 직접
└─ mod_reciever 슬롯에 꽂힌 리시버(5bb20d53d4351e4502010a69)
   ├─ mod_barrel  ← 총열은 여기(리시버) 아래
   │  └─ mod_muzzle, mod_gas_block  ← 총열 아래
   ├─ mod_handguard  ← 핸드가드도 여기(리시버) 아래
   └─ mod_sight_rear
```

그래서 새 부품(총열/핸드가드)을 "장착 가능하게" 만들려면, **무기 아이템이
아니라 리시버 아이템(`5bb20d53d4351e4502010a69`)의 슬롯 필터**에 새 부품
ID를 추가해야 한다. `mod_stock`은 무기 루트에 바로 있으니 거기만 예외.
`K2Mod.cs`의 `RegisterFamilyParts()`가 이미 이 구조로 짜여 있음 — 나중에
바꿀 때 이 계층을 다시 헷갈리지 말 것.

**부작용**: 이 리시버 아이템은 우리 K2 무기만의 복제본이 아니라 HK416A5가
공유하는 원본 템플릿이다. 여기 필터를 추가하면 **실제(진짜) HK416A5도** 이
시험용 K2 부품을 낄 수 있게 된다. 지금은 시험 단계라 허용하고 로그로만
남겼음 — 최종 배포 전에는 "K2 전용 리시버를 새로 클론해서 그쪽에만 필터를
건다"로 바꿔야 할 수 있음(아직 결정 안 함).

### 5. `Preset` 객체의 `_id`를 C# 코드에서 프로퍼티로 믿지 말 것
`weapon.json`/`preset.json`을 보면 JSON 키가 `_id`/`_parent`/`_tpl`처럼 언더스코어로
시작한다. 기존 `K2Mod.cs`는 이 값을 **역직렬화된 객체의 프로퍼티로 읽지 않고**,
항상 **따로 하드코딩한 `MongoId` 상수**(`presetId = new MongoId("d219...0002")`)로
비교/등록한다. `NewItemFromCloneDetails`의 `NewId`/`ItemTplToClone`(카멜케이스 JSON
키: `newId`/`itemTplToClone`)는 프로퍼티로 직접 읽어도 검증됐지만, `Preset`/`Item`
계열의 언더스코어 키는 실제 C# 프로퍼티 매핑을 확인한 적이 없다. 새 코드를 짤 때도
이 관례(언더스코어 필드는 하드코딩 상수로 비교, 파일마다 객체 하나씩)를 그대로
따를 것 — 배열로 묶거나 `.Id` 프로퍼티를 새로 믿지 말 것.

### 6. 실제 진행 상태는 파일이 여기저기 흩어져 있다 — 확인할 때 다 봐야 함
"어디까지 됐는지"를 판단할 때 아래 4개 파일을 다 봐야 전체 그림이 나온다
(README의 상태 표만 보면 늦게 갱신됐을 수 있음, 2026-09-21에 한 번 갱신함):
- `README.md` "현재 상태" 표 — 요약
- `Docs/모델링크 및 정보.md`의 `<제작진행도>` — 날짜별 작업 로그(C33/R_F/Codex 전부)
- `Unity/현재상태.md` — Unity/클라 빌드·게임 설치 진행
- `Blender/작업현황.md` — 블렌더 버전별(v001~v012) 진행

### 7. 블렌더 작업은 지금까지 K2C3에만 했다
`Blender/작업현황.md`의 모든 항목(v001~v012)은 **K2C3만** 대상이다. K2(원본)와
K2C4(단축형)는 아직 glTF 구조 분석(README의 "모델 분석 결과" 표)만 끝났고,
블렌더에서 loose-part 분리도 시작 안 했다. "부품 갈아끼우기" 기획을 실제로
쓰려면 이 두 모델도 K2C3처럼 손대야 한다 — README "다음 작업 배정"의 C33님
항목 참고.
