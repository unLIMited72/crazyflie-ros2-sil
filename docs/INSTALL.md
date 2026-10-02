# 설치 안내

## 전제와 시스템 도구

Ubuntu 22.04.x / Python 3.10 / ROS2 Humble 설치 완료가 전제입니다. bootstrap은 ROS2 자체를 설치하지 않으며 /opt/ros/humble/setup.bash가 없으면 중단합니다.

| Package | source 근거 / 목적 |
|---|---|
| git | pinned upstream와 recursive submodule 획득 |
| python3-dev, python3-venv, python3-pip | ROS Python build 및 venv |
| build-essential, cmake, pkg-config | firmware sitl_make CMake의 C/C++/Threads/PkgConfig |
| python3-colcon-common-extensions, python3-rosdep | ROS workspace build / package.xml dependency |
| libusb-1.0-0-dev | crazyflie-link-cpp CMake |
| libboost-program-options-dev | crazyflie_tools CMake |
| libeigen3-dev | crazyflie CMake |
| libgl1, libglfw3 | MuJoCo GUI |
| ros-humble-rmw-fastrtps-cpp | baseline RMW |

새 PC의 시스템 준비가 필요한 경우 사용자가 실행합니다.

```bash
sudo apt update
sudo apt install git python3-dev python3-venv python3-pip \
  build-essential cmake pkg-config python3-colcon-common-extensions python3-rosdep \
  libusb-1.0-0-dev libboost-program-options-dev libeigen3-dev \
  libgl1 libglfw3 ros-humble-rmw-fastrtps-cpp
```

SIL 경로에는 Gazebo/PX4/ESP-IDF를 추가 설치하지 않습니다. bootstrap에서 이 APT 명령을 무조건 실행하지 않습니다.

## 설치 순서

```bash
git clone https://github.com/unLIMited72/crazyflie-ros2-sil.git ~/CrazySim
cd ~/CrazySim
./scripts/bootstrap.sh
```

source가 없으면 실제 remote에서 clone하고 SHA checkout, recursive submodule, patch 순서로 준비합니다. 모든 기존 checkout은 수정 전 remote/HEAD/expected diff를 검사합니다. 다운로드 실패나 충돌은 FAIL로 중단하며 reset/clean하지 않습니다.

Python은 --system-site-packages venv를 만들어 ROS APT 모듈을 공유하고 사용자 site를 차단합니다. lock의 MuJoCo/NumPy 등을 설치한 뒤 pinned cflib를 editable install합니다. 구버전 FPV cflib는 설치하지 않습니다.

firmware는 cf2 target만, ROS workspace는 7개 package를 symlink build합니다. CMake Python interpreter는 venv로 고정하고 optional link-cpp Python bindings와 C++ examples는 OFF입니다. 빌드 병렬도는 CRAZYSIM_BUILD_JOBS=2이며 메모리가 부족하면 1로 낮춥니다.

## rosdep

setup_ros_dependencies.sh는 clone의 cache/rosdep와 cache/ros_home에 공식 ros/rosdistro 데이터를 준비합니다. 시스템 /etc/ros 및 기존 ~/.ros를 쓰지 않습니다. 이미 dependency가 있으면 check만 통과합니다.

누락된 ROS dependency 설치를 허용하는 새 PC에서는:

```bash
CRAZYSIM_INSTALL_SYSTEM_DEPS=1 ./scripts/bootstrap.sh
```

이 옵션에서만 rosdep install --from-paths crazyswarm2_ws/src --ignore-src -r -y --rosdistro humble을 실행합니다. APT/sudo 사용은 해당 PC에서 사용자가 승인합니다. 기본 bootstrap은 누락 목록을 표시하고 중단합니다. mutable rosdep/APT 저장소는 version 완전 고정 대상이 아니므로 [재현성 한계](REPRODUCIBILITY.md)를 확인하십시오.

## 성공 기준

```bash
source config/crazysim_env.bash
use_crazysim_ros
./scripts/verify_environment.sh
ros2 pkg prefix crazysim_bringup
ros2 pkg prefix aideck_ros2_bridge
```

prefix가 현재 clone의 install 아래여야 합니다. 이후 GUI session에서 launch하고 verify_baseline.sh로 실제 node/topic/image 수신을 확인합니다.

## 재실행

bootstrap은 이미 맞는 source/patch를 SKIP하고 기존 venv/build를 재사용합니다. source HEAD 또는 tracked 내용이 예상과 다르면 중단합니다. 사용자의 수정은 자동 폐기하지 않습니다. fetch/checkout 도중 끊겨 예상 상태가 아닌 checkout이 생겼다면 별도 경로에 새 clone을 만들거나 상태를 검토한 후 직접 복구하십시오.
