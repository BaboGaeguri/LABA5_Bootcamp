# smolVLA 환경 요구사항 (arm_2week_plan 기준)

> 기준 문서: `smolVLA/arm_2week_plan.md`  
> 작성일: 2026-04-21  
> 목적: smolVLA 작업을 위한 요구사항 정의 문서

## 1) 문서 역할

- 이 문서: 요구사항(What is required)
- 하드웨어 실측/보유 현황: `smolVLA/docs/storage/02_hardware.md`
- 소프트웨어 실측/설정 현황: `smolVLA/docs/storage/03_software.md`

## 2) 기본 요구사항

- 개발 OS는 Ubuntu 네이티브를 사용한다.
- 로봇 문맥은 SO-ARM(SO-100/SO-101)을 기준으로 한다.
- 2주차 목표는 Orin에서 SO-ARM + smolVLA 추론 동작 확인이다.

## 3) 하드웨어 요구사항

### A. 로봇/입출력

- SO-ARM follower, leader 구성 가능해야 한다.
- 모터는 Feetech STS3215 계열(BOM 기어비 포함) 사용을 기본으로 한다.
- ST/SC 시리얼 버스 서보 드라이버 보드(팔 1대당 1개)가 필요하다.
- 카메라 1대 이상을 연결 가능해야 한다.

### B. 컴퓨팅

- 개발용 Ubuntu PC 1대 이상이 필요하다.
- 배포/실행용 Jetson Orin 계열 장치 1대가 필요하다.
- 루트/데이터 저장을 위한 SSD 기반 스토리지가 필요하다.

## 4) 소프트웨어 요구사항

- Python 3.12 환경을 기준으로 한다.
- lerobot + smolvla + training + feetech 의존성 그룹을 사용한다.
- SSH 원격 접속(Orin)이 가능해야 한다.

## 5) 검증 대상 체크리스트

- [ ] Orin에서 smolVLA 추론 실행 확인
- [ ] SO-ARM 제어 경로(모터/카메라/시리얼) 정상 확인
- [ ] 데이터 저장 경로(SSD) 정책 확정
- [ ] 학습 PC <-> Orin 모델 반입/실행 흐름 검증

## 6) 근거 문서

- `docs/source/so101.mdx:20`
- `docs/source/so101.mdx:33`
