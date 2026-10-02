# Crazyflie 2.1 CrazySim ROS2 SIL

이 repository는 **Thin repository + pinned upstream + patches + custom ROS2 packages** 구조입니다. Crazyflie firmware, simulation, cflib, Crazyswarm2, drone-models 전체 source를 직접 포함하지 않습니다. bootstrap이 각 upstream의 정확한 commit을 가져와 patch를 적용하고, 사용자 작성 ROS2 package와 함께 검증된 SIL baseline을 재구성합니다.

## 설치 Quick Start

전제: Ubuntu 22.04.5 LTS, Python 3.10, ROS2 Humble 설치 완료. Git/CMake/compiler/venv/colcon/rosdep 등 [시스템 도구](docs/INSTALL.md)가 필요합니다.

```bash
git clone https://github.com/unLIMited72/crazyflie-ros2-sil.git ~/CrazySim
cd ~/CrazySim
./scripts/bootstrap.sh

source config/crazysim_env.bash
use_crazysim_ros
ros2 launch crazysim_bringup single_cf.launch.py
```

새 terminal에서:

```bash
cd ~/CrazySim
source config/crazysim_env.bash
use_crazysim_ros
./scripts/verify_baseline.sh
```

bootstrap은 source → patch → venv → firmware → ROS dependency → ROS2 build → 환경 검사를 수행합니다. 필수 시스템 패키지가 없으면 설치 방법을 안내합니다. ROS dependency 자동 설치를 명시적으로 허용하려면 `CRAZYSIM_INSTALL_SYSTEM_DEPS=1 ./scripts/bootstrap.sh`를 사용하십시오. 이때 rosdep이 sudo/APT를 요청할 수 있습니다. ROS2 자체는 설치하지 않습니다.

실행 예시의 `~/CrazySim`이 이미 정상 개발환경이라면 그 위에 clone하지 마십시오. 새로운 경로를 사용해도 config가 해당 clone 위치를 계산합니다.

## 1. 구현 범위와 고정 baseline

Crazyflie firmware SITL + MuJoCo + Flow Deck + AI Deck Camera + CPX camera-only + Crazyswarm2 + ROS2 image bridge를 통합합니다. ArUco/SLAM/tracking/multi-agent/GAP8 simulation은 추가하지 않습니다.

| 항목 | 값 |
|---|---|
| OS / ROS | Ubuntu 22.04.5 LTS / Humble |
| Vehicle | cf231 |
| Flight URI | udp://127.0.0.1:19850 |
| Firmware SITL | UDP 19950 |
| Camera transport | raw UDP 5200 → CPX TCP 5050 |
| ROS | ROS_DOMAIN_ID=25, rmw_fastrtps_cpp |
| Estimator / controller | Kalman=2 / PID=1 |
| Camera | 324×244, mono8, 기준 약 18 Hz |
| Startup delay | camera node 4초 / Crazyswarm2 7초 |

Public checkout의 실제 사용자 runtime 검증에서 283 frames, 324×244 mono8, 79056 bytes, **18.79 Hz**를 확인했습니다. 모든 PC에서 보장되는 빈도는 아닙니다. **정상 실행 PASS / Ctrl+C clean shutdown WARN**이며, 종료 시 segmentation fault(exit code 139)가 관찰됐습니다. takeoff/go_to/land는 NOT TESTED입니다. 근거와 범위는 [QA_REPORT](docs/QA_REPORT.md)에 구분합니다.

## 2. 시스템 구조

```mermaid
flowchart LR
  R[ROS2 / Crazyswarm2] --> C[cflib]
  C <-->|UDP 19850| S[CrazySim]
  S <-->|UDP 19950| F[Firmware SITL / Kalman / PID]
  S <--> M[MuJoCo / Flow Deck]
  M -->|324x244 mono8 / UDP 5200| P[CPX camera-only]
  P -->|TCP 5050| B[aideck_ros2_bridge]
  B --> I[/cf231/camera/image_raw]
```

UDP 19850은 cflib 연결 지점이며 firmware 내부 endpoint 19950과 다릅니다. [ARCHITECTURE](docs/ARCHITECTURE.md)에 source와 protocol 근거를 설명합니다.

## 3. Git에 포함되는 것

```text
config/               portable Bash 환경
scripts/              clone / patch / bootstrap / build / verify
patches/              특정 upstream revision용 local diff
requirements/         Python version lock
manifests/            full SHA / 실제 remote / patch hash
docs/                 설치·구조·출처·재현성
third_party/licenses/ patch에 필요한 원 license text
crazyswarm2_ws/src/
  crazysim_bringup/    사용자 통합 launch
  aideck_ros2_bridge/  사용자 camera receiver
```

bootstrap 후 `crazyflie-firmware/`, `crazyflie-lib-python/`, `crazyswarm2_ws/src/crazyswarm2/`가 생성됩니다. 이들은 downloaded third-party source이므로 Git status에 나타나지 않는 것이 정상입니다. 하위 drone-models/mesh도 upstream submodule로 가져옵니다. 다운로드된 디렉터리나 .venv/build/cache를 GitHub archive에 추가하지 마십시오.

## 4. Source와 patch 준비

```bash
./scripts/setup_sources.sh
./scripts/setup_sources.sh --check
```

실제 remote와 40자리 commit은 [upstream_sources.yaml](manifests/upstream_sources.yaml)에 있습니다. branch 이름은 참고값이고 checkout 입력은 항상 SHA입니다. `git pull`이나 최신 branch tracking을 사용하지 않습니다.

기존 checkout의 remote/HEAD/staged 변경/예상 patch 결과가 다르면 중단합니다. reset/clean/강제 덮어쓰기를 하지 않습니다. 정상 재실행은 이미 적용된 patch를 SKIP합니다. [patch 적용 순서](patches/README.md)를 참고하십시오.

## 5. Python 가상환경

ROS Python과 MuJoCo/cflib의 패키지 버전을 함께 재현하기 위해 `.venv`를 생성합니다. baseline처럼 `--system-site-packages`로 ROS APT 패키지를 공유하고 사용자 site-packages는 차단합니다.

```bash
./scripts/setup_python.sh
source .venv/bin/activate
python --version
python -c 'import mujoco, numpy, cflib'
```

성공 기준은 Python 3.10과 import 성공입니다. 직접 dependency는 requirements.txt, 실제 설치 버전은 requirements-lock.txt, packaging 도구는 build-tools.txt에 있습니다. cflib는 현재 clone 안의 pinned source를 editable install합니다. absolute local path를 requirements에 저장하지 않습니다. camera bridge는 cv_bridge/OpenCV가 필요하지 않습니다.

## 6. Firmware와 ROS2 build

```bash
./scripts/setup_firmware.sh
./scripts/setup_ros_dependencies.sh
./scripts/build_ros2.sh
./scripts/verify_environment.sh
```

firmware는 Gazebo까지 포함하는 all 대신 MuJoCo baseline에 필요한 `cf2` target을 빌드합니다. ROS2는 venv Python을 지정해 `colcon build --symlink-install`하며 optional Python bindings/C++ examples는 OFF입니다.

성공 기준은 `sitl_make/build/cf2` 생성과 현재 checkout 아래의 custom package prefix입니다. 수정 뒤 `./scripts/rebuild_ros2.sh`는 build/install/log를 삭제하지 않는 증분 build입니다.

## 7. Shell 환경

```bash
source config/crazysim_env.bash
use_crazysim_ros
```

config 파일 위치에서 root를 계산하며 `CRAZYSIM_ROOT`로 override할 수 있습니다. 이전 clone의 값이 남았다면 `unset CRAZYSIM_ROOT` 후 source하십시오. ROS_DOMAIN_ID와 RMW 기본값은 각각 25와 rmw_fastrtps_cpp입니다.

`use_crazysim`은 venv, `use_crazyswarm`은 현재 ROS workspace, `use_crazysim_ros`는 둘 다 활성화합니다. bootstrap은 .bashrc/.bash_aliases를 변경하지 않습니다. 영구 설정 예시는 [shell_aliases_example.bash](config/shell_aliases_example.bash)에 있습니다. PX4/Gazebo/ESP-IDF 등 기존 개인 shell 설정을 복사하지 않습니다.

## 8. 실행과 scene 변경

```bash
./scripts/run_single_cf.sh
./scripts/run_single_cf.sh scene_obstacles.xml
# 원래 launch interface:
ros2 launch crazysim_bringup single_cf.launch.py scene:=/path/to/scene_obstacles.xml
```

scene.xml이 기본이며 scene_dark.xml, scene_obstacles.xml, scene_walls.xml은 pinned simulation source에 있습니다. obstacles의 collision은 contype=1/conaffinity=1이고 box size는 half-size입니다.

기존 sitl_camera.sh에는 전역 pkill이 있으므로 다른 CrazySim/cf2 실행과 병행하지 마십시오. 이번 작업에서는 이를 기능 변경으로 고치지 않았습니다.

## 9. 정상 동작 확인

```bash
ros2 node list
ros2 topic list
ros2 topic info /cf231/camera/image_raw
ros2 topic hz /cf231/camera/image_raw
ros2 topic echo /cf231/camera/image_raw --once
./scripts/verify_baseline.sh
```

필수 node는 /crazyflie_server, /aideck_camera_node입니다. 필수 topic은 /cf231/pose, /cf231/status, /cf231/tof, /cf231/flow, /cf231/camera/image_raw입니다. camera는 width=324, height=244, encoding=mono8, payload=79056 bytes를 확인합니다. verify_baseline은 timeout을 두고 수신하며 flight command를 보내지 않습니다.

## 10. Flow Deck와 camera

ToF는 `range.zrange → /cf231/tof`입니다. sensors_sitl.c는 flowData.dpixelx/dpixely/stdDevX/stdDevY/dt를 구성해 estimatorEnqueueFlow()로 Kalman에 전달합니다. ROS logging은 kalman_pred.measNX/measNY/predNX/predNY → /cf231/flow이며 motion.deltaX/Y로 변경하지 않습니다. stdDev는 고정이고 dynamic SQUAL/texture-dependent quality는 없습니다.

camera는 MuJoCo → UDP 5200 → crazysim_cpx.py --camera-only → CPX APP/TCP 5050 → aideck_ros2_bridge 경로입니다. 11-byte header `<BHHBBI`는 magic=0xBC, 324×244, depth=8, format=0, size=79056입니다.

camera-only는 CRTP forwarding thread와 CPX_F_CRTP→UDP forwarding을 비활성화하여 Crazyswarm2의 flight/logging ownership을 유지합니다. fpv.py를 최종 receiver로 사용하지 않습니다.

## 11. Legacy FPV dependency

crazyflie-lib-python-fpv는 과거 receiver 실험용 동일 Bitcraze upstream의 구버전입니다. 현재 single_cf.launch.py/bridge는 이를 참조하지 않아 필수 bootstrap에서 제외했습니다. 기록과 patch는 보존합니다.

```bash
./scripts/setup_sources.sh --with-legacy-fpv
```

이는 source 준비만 수행하며 구버전 cflib를 현재 venv에 설치하지 않습니다. legacy fpv.py에는 arming/hover 경로가 있으므로 현재 SIL과 동시에 실행하지 마십시오.

## 12. 개발·재현성·실기체 방향

custom launch는 crazysim_bringup, camera는 aideck_ros2_bridge에서 수정합니다. downloaded source 수정은 상위 Git status에 보이지 않으므로 해당 nested repo의 git diff를 확인하고 검토한 patch로 갱신하십시오. [DEVELOPMENT](docs/DEVELOPMENT.md), [REPRODUCIBILITY](docs/REPRODUCIBILITY.md), [SOURCE_PROVENANCE](docs/SOURCE_PROVENANCE.md)를 따르십시오.

실기체 전환은 flight를 Crazyradio/CRTP로, camera를 AI Deck HM01B0/GAP8/ESP32/Wi-Fi로 바꾸고 상위 ROS interface를 가능한 유지하는 방향입니다. 이번 repository에서 실기체 interface를 새로 구현하거나 검증하지 않았습니다.

## 13. Troubleshooting

[진단 문서](docs/TROUBLESHOOTING.md)에 ROS source/venv/package not found, build, port 충돌, camera 0 Hz, Flow 중단, scene/GUI, ROS domain/RMW 불일치를 정리했습니다. source/patch 검사가 FAIL이면 기존 개발 변경을 먼저 확인하고 자동 삭제하지 마십시오.

## 14. 라이선스 및 공개 범위

사용자 original package·script·config·documentation은 [Apache License 2.0](LICENSE)으로 공개합니다. 기존 OSRF Apache template notice는 유지합니다. upstream-derived patch에는 해당 원 project/file의 라이선스가 적용되며 root Apache가 이를 대체하지 않습니다.

[THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)에 URL/SHA/license/획득 방식/patch를 기록합니다. [LICENSE_DESIGN](docs/LICENSE_DESIGN.md)은 Full Snapshot의 mesh/Nordic/legacy source 직접 재배포를 제외한 이유와 남는 조건을 설명합니다. upstream에서 다운로드할 수 있다는 사실 자체가 사용·재배포 허가를 새로 부여하지는 않습니다.

현재 판정과 시험 결과는 [QA_REPORT](docs/QA_REPORT.md), 게시 전 항목은 [GITHUB_PUBLISH_CHECKLIST](docs/GITHUB_PUBLISH_CHECKLIST.md)를 확인하십시오. 이 공개 범위에 대한 readiness 검토는 법률 보증이 아닙니다.
