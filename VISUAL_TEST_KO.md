# K2C3 외형 시험 빌드

대상: SPT 4.1.6, 클라이언트/서버 0.2.0. 실제 F:/SP-Tushunka DLL로 빌드한다.

목표: 기존 K2 서버 아이템에 K2C3 정적 외형을 표시해 게임 로딩 경로를 검증한다.
이 단계는 전용 총기 프리팹이나 완성된 애니메이션이 아니다.

## 빌드

1. Unity Hub에서 계정 로그인 및 사용 가능한 라이선스 활성화.
2. Blender MCP에서 `Blender/export_visual.py` 실행. v012에 있는 원본 Scene과 정렬 정보를 사용한다.
3. `Build-Visual.ps1` 실행. Unity 2022.3.43f1 Windows 에디터가 필요하다.

결과는 `Artifacts/VisualBundle/k2c3_visual.bundle` 및 `Client/bin/Release/netstandard2.1/K2.Visual.dll`이다.
라이선스 없이 빌드할 수 없으며 DLL만 생성된 상태를 완성 릴리즈로 취급하지 않는다.

## 시험 설치 구성

기존 서버 프로토타입과 함께 아래 두 파일을 같은 폴더에 설치한다.

```text
BepInEx/plugins/K2-Project/K2.Visual.dll
BepInEx/plugins/K2-Project/k2c3_visual.bundle
SPT_Runtime/user/mods/K2-Project/ (기존 서버 모드)
```

외형은 아이템 ID `d21900000000000000000001`에만 적용한다. 기본 HK416은 바꾸지 않는다.
총기 본 아래의 기존 메시만 숨기며 원본 탄창은 보존한다. 캐릭터 팔은 대상이 아니다.
렌더러 상태는 오브젝트 재사용 시 복구한다. 번들이 누락되면 기존 외형을 유지하고 로그를 남긴다.

## 확인 순서

1. 로그에서 `[K2C3] 외형 번들 준비 완료` 확인.
2. K2 아이템 검사창과 장착 상태에서 외형 확인.
3. 일반 HK416과 번갈아 장착하고, 버리기/줍기 후에도 두 외형이 섞이지 않는지 확인.
4. 원본 탄창·팔이 보이는지, 총 크기·축·재질을 확인.

정적 외형이므로 K2 가동부/개머리판은 움직이지 않는다. 조준 위치·총구 효과는 아직 HK416 기준이다.
광학장비 등 다른 부착물 외형은 이번 시험에서 보존 대상이 아니다. 무기 부품 교체 완성본으로 배포하지 않는다.

모델: GAMGO의 K2C3, CC-BY-4.0.
https://sketchfab.com/3d-models/k2c3-39bb1eeed4b949c7a620b16667262faf
https://creativecommons.org/licenses/by/4.0/
