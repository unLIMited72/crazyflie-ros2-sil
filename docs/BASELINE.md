# 고정 SIL baseline

| 항목 | 값 |
|---|---|
| vehicle | cf231 |
| launch model | cf2x_P250 |
| cflib URI | udp://127.0.0.1:19850 |
| firmware SITL port | UDP 19950 |
| camera raw / CPX | UDP 5200 / TCP 5050 |
| ROS_DOMAIN_ID | 25 |
| RMW_IMPLEMENTATION | rmw_fastrtps_cpp |
| estimator | stabilizer.estimator=2, Kalman |
| controller | stabilizer.controller=1, PID |
| camera | 324 × 244, mono8, 79,056 bytes |
| camera baseline 빈도 | 사용자 검증 기준 약 18 Hz |
| startup | camera node 4.0초, Crazyswarm2 7.0초 |
| default scene | scene.xml |

Mellinger(controller=2)로 변경하지 않았습니다. launch는 flowdeck을 활성화하며, pose는 firmware 추정값입니다. core topic은 /cf231/pose, /cf231/status, /cf231/tof, /cf231/flow, /cf231/camera/image_raw입니다.

카메라 header `<BHHBBI`는 11 bytes: magic=0xBC, width=324, height=244, depth=8, format=0, size=79056. source 검사와 runtime 검사는 구분합니다. 이 Public checkout에서 실제 수행한 검증은 QA_REPORT.md를 따릅니다.

scene.xml, scene_dark.xml, scene_obstacles.xml, scene_walls.xml은 simulation upstream commit에 이미 들어 있는 tracked file입니다. local 생성이라고 분류하지 않습니다.
