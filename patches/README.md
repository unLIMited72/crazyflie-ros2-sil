# Upstream-derived patches

각 patch는 특정 upstream revision에 대한 수정사항입니다. 원본 파일 및 수정본에는 해당 upstream project/file의 기존 license가 적용됩니다. repository root Apache-2.0은 이 license를 대체하지 않습니다. binary/model/mesh payload를 포함하지 않습니다.

patch 포장은 2026-10-02에 수행했습니다. baseline의 원 수정일과 이 포장일을 동일한 날짜라고 주장하지 않습니다. 원본 개발환경은 읽기 전용이며 git diff --binary HEAD로 local tracked diff를 추출했습니다. patch 적용은 scripts/manage_sources.py가 담당합니다.

| 순서 / path | 적용 repo / SHA | 내용 | 원 license |
|---|---|---|---|
| 1. patches/crazyflie-simulation/0001-baseline.patch | crazyflie-firmware/tools/crazyflie-simulation / 89d8cf79fb722bf4bd7e363ade7d90d6c45d6d5d | read-only source baseline의 local diff 복원 | MIT main; Apache/BSD/Zlib source 예외 |
| 2. patches/crazyflie-simulation/0002-path-portability.patch | crazyflie-firmware/tools/crazyflie-simulation / 89d8cf79fb722bf4bd7e363ade7d90d6c45d6d5d | Export에서 검증한 scene/executable 경로 quoting; 기능 기본값 동일 | MIT main; Apache/BSD/Zlib source 예외 |
| 1. patches/crazyswarm2/0001-baseline.patch | crazyswarm2_ws/src/crazyswarm2 / 2334b7a32432fd3f9e1133c52361ddcc27ca3cf7 | read-only source baseline의 local diff 복원 | MIT main; 개별 header 예외 |
| 1. patches/crazyflie-lib-python-fpv/0001-baseline.patch | crazyflie-lib-python-fpv / 70d10a13a5f61258dd9677a875b85ff32bfae135 | read-only source baseline의 local diff 복원 | GPL v2 전문 / v2-or-later header / GPLv3 metadata; binary 별도 |

## 변경 의미

- simulation 0001: sitl_camera initial x/y, Flow Deck/camera 통합, CPX --camera-only의 CRTP forwarding 분리.
- simulation 0002: scene argument를 Bash array로 전달하고 firmware 실행 경로를 quote. baseline 포트·controller·timing 변경 없음.
- Crazyswarm2 0001: cf231 UDP URI, cf_sim, ToF/flow logging, Kalman/PID 설정.
- legacy FPV 0001: 기존 time import/Qt enum 수정. optional source로만 보존하며 기본 camera receiver는 aideck_ros2_bridge.

firmware root와 cflib main은 직접 local diff가 없어 patch가 없습니다. 하위 simulation patch가 firmware sensor implementation 전체를 대체하지 않습니다. scene 4개/Flow Deck sensor source는 pinned upstream에 이미 포함돼 있습니다.

## 재실행과 검증

manifest의 patch checksum을 먼저 검사합니다. 깨끗한 pinned tree에 git apply --check 후 순서대로 적용하고 target 파일의 hash/실행 권한을 확인합니다. 완성된 patch 상태에서는 전체 시리즈를 SKIP하므로 0002 적용 후 0001 역적용 여부에 의존하지 않습니다. 중간 실패나 개발 변경이 있으면 강제 이어쓰기 대신 중단합니다.

## 원문

- [simulation MIT](../third_party/licenses/crazyflie-simulation-MIT.txt): Copyright (c) 2022 Bitcraze.
- [Crazyswarm2 MIT](../third_party/licenses/crazyswarm2-MIT.txt): Copyright (c) 2014 whoenig.
- [cflib GPL v2 전문](../third_party/licenses/cflib-GPL-2.0.txt): fpv.py의 원 GPL v2-or-later header와 함께 해석. Bitcraze copyright를 대체하지 않음.

GPL patch를 다른 license로 재선언하지 않습니다. patch 삭제행에 기존 copyright/permission/SPDX 고지를 제거한 내용이 없는지 QA에서 확인합니다. 필요한 upstream context와 modification이 포함되므로 단순히 우리 코드라는 이유로 Apache를 붙이지 마십시오.
