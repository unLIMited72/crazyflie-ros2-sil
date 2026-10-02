# Public Repository QA 결과

검사일: 2026-10-02. **Release readiness: PUBLIC READY WITH NOTES**. 이 판정은 직접 배포하는 Thin repository의 license/고지 범위에 대한 release-readiness 감사이며 법률 보증이 아닙니다. downloaded upstream의 권리 문제가 자동 해결됐다는 뜻은 아닙니다.

## 실제 수행한 재현성 검사

새 `qa/repro` clone-equivalent에는 처음에 Public의 직접 관리 파일만 복사했습니다. 원본/Full Snapshot의 upstream tree, venv, build 산출물은 사용하지 않았습니다. 실제 GitHub remote에서 23개 필수 recursive source를 새로 획득하고 exact SHA checkout, patch, venv, firmware, rosdep, colcon, verify를 수행했습니다. 이후 optional FPV를 별도 획득해 총 24개 SHA/patch도 검사했습니다.

시스템 APT 설치/sudo나 기존 /etc/ros 및 ~/.ros 변경 없이 clone 내부 rosdep cache를 사용했습니다. 기존 시스템의 ROS/APT dependency는 재사용했으므로 새 OS image의 APT 설치 자체를 시험한 것은 아닙니다. 테스트한 scripts/config/custom runtime 및 실행 lock/manifest bytes는 최종 Public 파일과 같습니다.

| 검사 | 결과 | 근거 |
|---|---|---|
| Shell syntax | PASS | 배포 대상 .sh/.bash bash -n |
| Shellcheck | PASS | warning 이상; 동적 source 경로 SC1090/SC1091 제외 |
| Python syntax | PASS | 배포 Python 전체 AST parse; baseline runtime AST 동일 |
| Secret scan | PASS (검사 범위) | private key/token 패턴; 기존 공개 maintainer metadata는 유지 |
| Absolute personal path | PASS | 직접 배포 파일에 개인 home 절대 경로/로그인 문자열 없음 |
| Large file / asset scan | PASS | 20 MiB 초과 없음; mesh/image/blob/ELF 동봉 없음 |
| Pinned SHA / remote | PASS | 필수 23개 및 optional 포함 24개 실제 checkout |
| Patch apply | PASS | simulation 2개, Crazyswarm2 1개, optional FPV 1개; 결과 hash/mode |
| Patch idempotency | PASS | 두 번째 source setup에서 3개 patched repo SKIP |
| 실패 안전성 | PASS | 잘못된 SHA/remote/patch checksum/변경된 source를 거부, 강제 덮어쓰기 없음 |
| Fresh bootstrap | PASS | source acquisition부터 verify_environment까지 완료 |
| Bootstrap 재실행 | PASS | reclone/reset 없이 완료 |
| Firmware build | PASS | CMake cf2 target 생성 |
| ROS2 build | PASS | 7 packages, venv Python, 현재 clone prefix |
| Package license 설치 | PASS | 두 custom package share에 root Apache 전문 설치 |
| CPX camera 오프라인 | PASS | 실제 packet builder → fragmented stream → 244×324 NumPy, 잘린 payload 거부 |
| camera-only 오프라인 | PASS | network mock; CRTP forwarding/thread 차단 |
| MuJoCo scene 오프라인 | PASS | scene 4개 + 실제 upstream mesh compile, nbody=6/ncam=2 |
| SIL 통합 GUI launch | PASS | 최초 격리 검사 이후 사용자가 Public checkout에서 실제 launch 확인 |
| 실제 ROS topic/camera Hz | PASS | 사용자 runtime 검증 보고: 283 frames, 18.79 Hz, 324×244 mono8 |
| Clean shutdown | WARN | Ctrl+C/KeyboardInterrupt 이후 segmentation fault, exit code 139 관찰 |

## Public checkout 실제 runtime 확인

최초 Thin 구성 당시 자동 검사는 전역 pkill 영향 때문에 GUI launch를 실행하지 않았습니다. 이후 사용자가 Public checkout에서 bootstrap 및 실제 SIL launch를 완료했고, 이번 게시 요청에서 다음 결과를 제공했습니다. 아래 runtime PASS는 그 사용자 검증 보고를 근거로 반영한 것이며, 게시 담당 agent가 이번 작업에서 비행이나 SIL을 재실행했다는 뜻은 아닙니다.

| 항목 | 결과 | 확인 내용 |
|---|---|---|
| Bootstrap / firmware / ROS2 build | PASS | Public checkout에서 완료 |
| /crazyflie_server | PASS | cf231 connected, logging initialized, fully connected |
| /aideck_camera_node | PASS | 실제 camera stream 연결 |
| stabilizer.controller / estimator | PASS | PID=1 / Kalman=2 |
| /cf231/pose | PASS | topic 확인 |
| /cf231/status | PASS | topic 확인 |
| /cf231/tof | PASS | topic 확인 |
| /cf231/flow | PASS | topic 확인 |
| /cf231/camera/image_raw | PASS | 실제 image 수신 |
| Camera metadata / 수신율 | PASS | 324×244, mono8, 79056 bytes, 283 frames, 18.79 Hz |
| takeoff / go_to / land | NOT TESTED | 이번 Public 최종 검증에서 별도 maneuver 근거 없음 |
| 수평 이동 중 Flow 수치 응답 | NOT TESTED | topic 존재를 maneuver 검증으로 간주하지 않음 |
| 실제 이륙 중 ToF 고도 응답 | NOT TESTED | 별도 비행 검증 필요 |

### Known shutdown issue

Runtime startup/operation은 PASS이며, Ctrl+C 종료의 clean shutdown은 WARN입니다. KeyboardInterrupt 후 CrazySim/MuJoCo process에서 segmentation fault (core dumped), exit code 139가 관찰됐습니다. 정상 실행 중 기능에 대한 영향은 보고되지 않았으나 종료 문제가 해결되었다고 주장하지 않습니다. 추후 cleanup issue로 검토해야 합니다. 기존 전역 pkill 주의사항도 유지합니다.

core/core.* 및 runtime 산출물은 Git ignore 대상이며 공개 payload에서 제외합니다. 이번 게시 작업에서는 source 기능을 변경하거나 이 종료 문제를 수정하지 않았습니다.

## 보호 QA

SOURCE_ROOT modified: **NO**. EXPORT_ROOT modified: **NO**.

원본 20,943개, 기존 Export 24,625개 파일/심볼릭 링크를 작업 전후 hash로 비교했습니다. source/.git/.venv를 포함하며 build/install/log/cache/qa/__pycache__와 private tool 설정 디렉터리는 제외했습니다. 원본 26개 Git repository의 HEAD/remote/branch/status와 Export staged index SHA/status가 그대로입니다. 접근 시간 등 읽기 부수 metadata는 hash 동일성 주장 대상이 아닙니다.

## Git와 배포 범위

초기 구성은 Public에서만 main으로 git init한 상태였습니다. 이번 게시 작업은 사용자의 명시적 승인에 따라 최종 payload 검사 후 최초 commit, GitHub Public repository 생성, origin 확인, main push 순서로 수행합니다. 대상은 https://github.com/unLIMited72/crazyflie-ros2-sil 이며 기존 repository를 덮어쓰거나 force push하지 않습니다.

bootstrap 다운로드, .venv/build/install/log/cache, qa 전체는 ignore됩니다. 이 디렉터리 전체를 zip으로 묶어 공개하지 마십시오. 직접 배포 후보 파일 수/크기/해시는 manifests/public_payload.json에 별도로 기록합니다.

## 남는 note

- upstream 사용·재배포 조건은 원 project/file 기준이며, drone-models/Nordic/legacy source의 미확정 권리를 새로 부여하지 않습니다.
- 직접 배포 custom은 사용자 Apache 선택에 근거하며 OSRF template/derived patch 원 고지를 유지합니다.
- immutable source SHA와 Python version에도 upstream/PyPI/APT availability, GPU 및 ROS patch version 차이는 남습니다.
- 실제 node/topic/camera는 위 사용자 runtime 보고로 확인했습니다. 비행 maneuver와 clean shutdown 개선은 별도 후속 항목입니다.

상세 로컬 로그는 qa/fresh_bootstrap.log, bootstrap_rerun.log, optional_fpv.log, offline_smoke.log, repro_tests.json, final_qa.json에 있으며 Git 배포에서 제외합니다.
