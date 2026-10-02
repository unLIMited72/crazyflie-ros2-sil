# 문제 해결

| 증상 | 확인 및 조치 |
|---|---|
| ROS2 Humble이 source되지 않음 | /opt/ros/humble/setup.bash 존재 확인 후 config/crazysim_env.bash를 source. ROS 설치 자체는 사전 준비 |
| use_crazysim_ros 없음 | function 등록 전임. 현재 clone의 config 파일을 source. .bash_aliases를 자동 읽지 않는 shell이면 직접 source |
| .venv 없음 | setup_python.sh 또는 bootstrap 실행. venv 복사로 해결하지 않음 |
| colcon build 실패 | 첫 오류 package와 workspace log 확인. rosdep check 및 Python 3.10 확인. 메모리 부족 시 CRAZYSIM_BUILD_JOBS=1 |
| package not found | build_ros2.sh 완료 후 환경 source. ros2 pkg prefix가 현재 clone 아래인지 확인 |
| TCP 5050 사용 중 | ss -ltnp로 기존 camera/FPV client/server 확인. 본인 기존 launch terminal에서 정상 종료 |
| UDP 19850 충돌 | ss -lunp로 기존 CrazySim 인스턴스 확인. 같은 host의 baseline을 동시에 실행하지 않음 |
| camera topic 없음 | camera node가 4초 뒤 시작하는지, CPX --camera-only와 TCP 5050 연결 log 확인 |
| camera Hz 0 | TCP 연결뿐 아니라 MuJoCo renderer → UDP 5200 frame 생성 확인. best_effort QoS 구독 사용 |
| camera 실행 후 tof/flow 중단 | 아래 CRTP ownership 설명 참조. fpv.py 동시 실행 중단 |
| scene path 오류 | 실제 절대 경로 또는 run_single_cf.sh scene_obstacles.xml 사용. relative asset 경로도 확인 |
| MuJoCo window 미표시 | GUI DISPLAY/Wayland/X11/OpenGL driver 확인. SSH/headless 환경에서는 GUI 표시 보장 불가 |
| ROS_DOMAIN_ID 불일치 | 모든 terminal에서 echo "$ROS_DOMAIN_ID"; baseline 25로 일치 |
| RMW 불일치 | echo "$RMW_IMPLEMENTATION"; rmw_fastrtps_cpp package 설치와 모든 terminal 값 확인 |
| NumPy ABI 또는 cv_bridge 오류 | baseline bridge는 cv_bridge를 사용하지 않음. 다른 overlay/사용자 site 오염 확인 |
| cflib version/UDP driver 오류 | pip show cflib와 cflib.__file__ 확인. fpv 구버전 설치 대신 setup_python.sh 재실행 |
| source SHA/patch FAIL | 해당 nested repo의 git status/diff, remote, HEAD 확인. setup_sources.sh --check로 검증. 강제 reset/clean 없음 |

## Camera와 flight communication ownership

camera 정상 영상만으로 flight communication 정상 여부를 판단하지 마십시오. 과거 FPV는 cflib 연결과 arming/hover timer를 함께 만들었습니다. CPX의 CRTP forwarding이 켜져 있으면 Crazyswarm2의 응답/로그 경로와 경쟁합니다.

현재 script는 crazysim_cpx.py --camera-only를 사용합니다. _crtp_to_cpx_loop는 실행하지 않고 CPX_F_CRTP를 UDP로 보내지 않습니다. 다음을 순서대로 확인하십시오.

1. fpv.py 및 두 번째 CPX client를 실행하고 있지 않은지 확인.
2. CPX log에 Camera-only mode: CRTP bridge disabled가 있는지 확인.
3. Crazyswarm2 backend가 cflib이며 URI가 udp://127.0.0.1:19850인지 확인.
4. firmware 19950 / raw camera 5200 / CPX 5050 역할을 혼동하지 않았는지 확인.
5. launch를 본인 terminal에서 종료하고 단일 launch로 재실행한 뒤 tof/flow/camera를 함께 확인.

## Terminal 간 환경

```bash
source /actual/clone/path/config/crazysim_env.bash
export ROS_DOMAIN_ID=25
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
use_crazysim_ros
ros2 pkg prefix crazysim_bringup
./scripts/verify_environment.sh
./scripts/verify_baseline.sh
```

CRAZYSIM_ROOT가 이전 clone으로 설정돼 있으면 unset 후 현재 config를 source하십시오. 다른 프로젝트 .bashrc 전체를 가져오지 않습니다. verify_baseline이 timeout(124)으로 끝나면 DDS/RMW 초기화 또는 수신 대기 문제를 확인하십시오.

## CPX의 오래된 시작 로그

일부 upstream 시작 로그에 camera TCP 5200이라는 표기가 남아 있지만 실제 CameraRenderer와 _frame_to_cpx_loop는 SOCK_DGRAM/UDP 5200을 사용합니다. CPX client 연결은 TCP 5050입니다. 기능 보존을 위해 로그 문구만을 고치는 patch는 추가하지 않았습니다.

## Ctrl+C 종료 시 segmentation fault

Public runtime 검증에서 정상 연결·camera 수신 후 Ctrl+C/KeyboardInterrupt 종료 중 CrazySim/MuJoCo segmentation fault, exit code 139가 관찰됐습니다. Runtime operation PASS와 clean shutdown WARN을 구분합니다. 해결된 문제로 표시하지 않으며 이번 공개 준비에서 기능 수정은 하지 않았습니다. takeoff/go_to/land 검증과는 별도입니다. core dump는 ignore 대상이며 commit하거나 배포 archive에 포함하지 마십시오.
