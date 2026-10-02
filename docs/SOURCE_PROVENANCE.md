# Source provenance

모든 URL과 SHA는 원본 nested repository에서 read-only git remote/rev-parse로 확인했습니다. branch는 참고값이며 설치는 full SHA로 고정합니다. 아래 source tree는 모두 **NOT VENDORED / FETCHED FROM UPSTREAM**입니다. 사용자 custom 두 package는 별도로 직접 관리합니다.

upstream full source와 asset의 license scope 문제를 root Apache로 해결한다고 주장하지 않습니다. 세부 해석은 LICENSE_DESIGN.md를 참조하십시오.

| Component / path | Origin | Pinned SHA | License | Vendored? | Local modification / patch | Runtime requirement |
|---|---|---|---|---|---|---|
| crazyflie-firmware | https://github.com/llanesc/crazyflie-firmware.git | aa6571dc465f06f7d1f9aaf7b0b861fbcd1b3d67 | GPL v3 main; vendor별 별도 조건 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyflie-firmware/vendor/unity | https://github.com/throwtheswitch/unity.git | 287e076962ec711cd2bdf08364a8df9ce51e106b | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/cmock | https://github.com/throwtheswitch/cmock.git | cb1ad78b974937e1ad717858fab73ec5380ef94b | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/cmock/vendor/unity | https://github.com/throwtheswitch/unity.git | 287e076962ec711cd2bdf08364a8df9ce51e106b | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/cmock/vendor/c_exception | https://github.com/throwtheswitch/cexception.git | dce9e8b26f2179439002e02d691429e81a32b6c0 | permissive 원문 + CException acknowledgment 조건 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/cmock/vendor/c_exception/vendor/unity | https://github.com/throwtheswitch/unity.git | 2c7629a0ae90ffe991b5fd08e4db8672f72ed64c | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/CMSIS | https://github.com/ARM-software/CMSIS_5.git | a65b7c9a3e6502127fdb80eb288d8cbdf251a6f4 | Apache-2.0 main; 하위 예외 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/FreeRTOS | https://github.com/FreeRTOS/FreeRTOS-Kernel.git | 3604527e3b31991c596cd420f32989ee890aca4a | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/libdw1000 | https://github.com/bitcraze/libdw1000.git | a77610327fb875a69543f3a8d19507683b68aff1 | Apache-2.0 main; 하위 예외 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/libdw1000/vendor/unity | https://github.com/throwtheswitch/unity.git | 7943c766b993c9a84e1f6661d2d2427f6f2df9d0 | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/libdw1000/vendor/cmock | https://github.com/throwtheswitch/cmock.git | 581642e08c6d2c71f63e6021f97c94829c0098b6 | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/libdw1000/vendor/cmock/vendor/unity | https://github.com/throwtheswitch/unity.git | 33325f4a0bc0931823867b11241dff3c2a0b60b7 | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/libdw1000/vendor/cmock/vendor/c_exception | https://github.com/throwtheswitch/cexception.git | ea0c4352f8912dcadac1c328901c51190084eb7b | permissive 원문 + CException acknowledgment 조건 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/vendor/libdw1000/vendor/cmock/vendor/c_exception/vendor/unity | https://github.com/throwtheswitch/unity.git | 47a778d606fbfabde459b0f725a67b18c1bce6ee | MIT; 파일별 copyright 유지 | NO | 직접 diff 없음 | build/test vendor; recursive pin 유지 |
| crazyflie-firmware/tools/crazyflie-simulation | https://github.com/llanesc/crazyflie-simulation.git | 89d8cf79fb722bf4bd7e363ade7d90d6c45d6d5d | MIT main; Apache/BSD/Zlib source 예외 | NO | patches/crazyflie-simulation/0001-baseline.patch, patches/crazyflie-simulation/0002-path-portability.patch | 기본 source dependency |
| crazyflie-firmware/tools/crazyflie-simulation/simulator_files/mujoco/drone-models | https://github.com/utiasDSL/drone-models.git | 512c864ffa55081ef4e80fadde2e861f22f45943 | metadata MIT classifier; 원문/asset grant 미확정 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyswarm2_ws/src/crazyswarm2 | https://github.com/llanesc/crazyswarm2.git | 2334b7a32432fd3f9e1133c52361ddcc27ca3cf7 | MIT main; 개별 header 예외 | NO | patches/crazyswarm2/0001-baseline.patch | 기본 source dependency |
| crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools | https://github.com/llanesc/crazyflie_tools.git | c684de4a81e57106453f8e604e1daa3f5b16d800 | MIT main; 개별 header 예외 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp | https://github.com/llanesc/crazyflie_cpp.git | 38b625ceda620868166feb9c0bf82df153d08203 | MIT main; 개별 header 예외 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp/crazyflie-link-cpp | https://github.com/llanesc/crazyflie-link-cpp.git | 4821cbd48ad667ec19c760b10414b8c0b138b309 | MIT main; 개별 header 예외 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp/crazyflie-link-cpp/libusb | https://github.com/libusb/libusb.git | 683e3cf21ed37d4492c20cea8de810c4d95ae8b6 | LGPL v2.1 계열 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp/crazyflie-link-cpp/pybind11 | https://github.com/pybind/pybind11.git | 5b0a6fc2017fcc176545afe3e09c9f9885283242 | BSD-3-Clause main; 파일별 예외 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyflie-lib-python | https://github.com/bitcraze/crazyflie-lib-python.git | 3c1cb0d024fef6f45d08f0ad236a22ac395dd924 | GPL v2 전문 / v2-or-later header / GPLv3 metadata; binary 별도 | NO | 직접 diff 없음 | 기본 source dependency |
| crazyflie-lib-python-fpv | https://github.com/bitcraze/crazyflie-lib-python.git | 70d10a13a5f61258dd9677a875b85ff32bfae135 | GPL v2 전문 / v2-or-later header / GPLv3 metadata; binary 별도 | NO | patches/crazyflie-lib-python-fpv/0001-baseline.patch | optional legacy; 기본 launch 참조 없음 |

## Custom package provenance

crazysim_bringup과 aideck_ros2_bridge는 기존 개발환경의 custom package입니다. 이번 사용자 지시를 근거로 original runtime/launch 및 repository-owned scripts/docs/config는 Apache-2.0입니다. ROS template test는 OSRF Apache header를 유지합니다. source에 새 copyright holder 이름을 만들지 않았습니다.

Python runtime/launch의 원문을 검토했고, bridge의 CPX packet/image header 사용과 cflib source 복사를 구분했습니다. upstream protocol constants를 사용하는 사실만으로 GPL 구현을 복사한 것으로 판단하지 않습니다. 비교 범위와 잔여 한계는 LICENSE_DESIGN.md에 명시합니다.

## FPV 선택 이유

현재 custom launch는 sitl_camera.sh와 aideck_camera_node만 사용하고, sitl_camera.sh는 simulation/crazysim_cpx.py --camera-only를 실행합니다. 두 package 및 필수 설치 script의 runtime 경로에 crazyflie-lib-python-fpv나 fpv.py 호출이 없습니다. CPX 설명 문서의 fpv.py 예시는 과거 호환 client 설명이며 실행 dependency가 아닙니다. 따라서 manifest/patch는 보존하고 mandatory bootstrap에서는 제외했습니다.

## Full Snapshot 전용 변경의 제외

firmware versionTemplate의 snapshot fallback, 각 .gitattributes 자동변환 차단, cflib pyproject fallback은 nested .git 없는 snapshot을 위한 조치였습니다. 여기서는 실제 upstream Git checkout이므로 적용하지 않습니다. 경로 quoting과 CRAZYSIM_ROOT 처리는 재현성에 필요하여 보존했습니다.
