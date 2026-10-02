# Third-Party Notices

이 repository의 사용자 original code에는 root Apache-2.0을 적용합니다. third-party component 및 upstream-derived patch에는 해당 project/file의 기존 license가 적용됩니다. 아래 source tree는 직접 동봉하지 않으며 bootstrap에서 upstream으로부터 획득합니다. 다운받은 tree의 원 license/header/NOTICE는 유지합니다.

root Apache가 모든 source/model/binary를 재라이선스하지 않습니다. 직접 배포 범위와 downloaded tree의 사용·재배포 조건은 별개입니다. [LICENSE_DESIGN](docs/LICENSE_DESIGN.md)을 참고하십시오.

## 직접 포함된 third-party 관련 내용

- simulation MIT patch: Bitcraze, Copyright (c) 2022 Bitcraze. [원문](third_party/licenses/crazyflie-simulation-MIT.txt).
- Crazyswarm2 MIT patch: Copyright (c) 2014 whoenig. [원문](third_party/licenses/crazyswarm2-MIT.txt).
- legacy fpv.py patch: Bitcraze의 GPL v2-or-later header scope. [GPL v2 전문](third_party/licenses/cflib-GPL-2.0.txt). Root Apache로 대체하지 않음.
- custom package의 ROS template tests: Copyright 2015/2017 Open Source Robotics Foundation, Inc. 기존 Apache-2.0 header와 disclaimer를 유지했습니다. [Apache 전문](LICENSE).

## Runtime dependency

MuJoCo 3.13.0은 PyPI 설치 dependency이며 source/wheel을 이 repository에 vendor하지 않습니다. 설치 wheel의 Apache-2.0 LICENSE 및 LICENSES_THIRD_PARTY.md가 적용됩니다. MuJoCo model XML/mesh는 별도 provenance를 따릅니다.

## Fetched upstream component 목록

### crazyflie-firmware

- Upstream URL: https://github.com/llanesc/crazyflie-firmware.git
- Pinned commit: `aa6571dc465f06f7d1f9aaf7b0b861fbcd1b3d67`
- License: GPL v3 main; vendor별 별도 조건
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: setup_sources의 exact checkout
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/unity

- Upstream URL: https://github.com/throwtheswitch/unity.git
- Pinned commit: `287e076962ec711cd2bdf08364a8df9ce51e106b`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/cmock

- Upstream URL: https://github.com/throwtheswitch/cmock.git
- Pinned commit: `cb1ad78b974937e1ad717858fab73ec5380ef94b`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/cmock/vendor/unity

- Upstream URL: https://github.com/throwtheswitch/unity.git
- Pinned commit: `287e076962ec711cd2bdf08364a8df9ce51e106b`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/cmock/vendor/c_exception

- Upstream URL: https://github.com/throwtheswitch/cexception.git
- Pinned commit: `dce9e8b26f2179439002e02d691429e81a32b6c0`
- License: permissive 원문 + CException acknowledgment 조건
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/cmock/vendor/c_exception/vendor/unity

- Upstream URL: https://github.com/throwtheswitch/unity.git
- Pinned commit: `2c7629a0ae90ffe991b5fd08e4db8672f72ed64c`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/CMSIS

- Upstream URL: https://github.com/ARM-software/CMSIS_5.git
- Pinned commit: `a65b7c9a3e6502127fdb80eb288d8cbdf251a6f4`
- License: Apache-2.0 main; 하위 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/FreeRTOS

- Upstream URL: https://github.com/FreeRTOS/FreeRTOS-Kernel.git
- Pinned commit: `3604527e3b31991c596cd420f32989ee890aca4a`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/libdw1000

- Upstream URL: https://github.com/bitcraze/libdw1000.git
- Pinned commit: `a77610327fb875a69543f3a8d19507683b68aff1`
- License: Apache-2.0 main; 하위 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/libdw1000/vendor/unity

- Upstream URL: https://github.com/throwtheswitch/unity.git
- Pinned commit: `7943c766b993c9a84e1f6661d2d2427f6f2df9d0`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/libdw1000/vendor/cmock

- Upstream URL: https://github.com/throwtheswitch/cmock.git
- Pinned commit: `581642e08c6d2c71f63e6021f97c94829c0098b6`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/libdw1000/vendor/cmock/vendor/unity

- Upstream URL: https://github.com/throwtheswitch/unity.git
- Pinned commit: `33325f4a0bc0931823867b11241dff3c2a0b60b7`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/libdw1000/vendor/cmock/vendor/c_exception

- Upstream URL: https://github.com/throwtheswitch/cexception.git
- Pinned commit: `ea0c4352f8912dcadac1c328901c51190084eb7b`
- License: permissive 원문 + CException acknowledgment 조건
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/vendor/libdw1000/vendor/cmock/vendor/c_exception/vendor/unity

- Upstream URL: https://github.com/throwtheswitch/unity.git
- Pinned commit: `47a778d606fbfabde459b0f725a67b18c1bce6ee`
- License: MIT; 파일별 copyright 유지
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-firmware/tools/crazyflie-simulation

- Upstream URL: https://github.com/llanesc/crazyflie-simulation.git
- Pinned commit: `89d8cf79fb722bf4bd7e363ade7d90d6c45d6d5d`
- License: MIT main; Apache/BSD/Zlib source 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: patches/crazyflie-simulation/0001-baseline.patch, patches/crazyflie-simulation/0002-path-portability.patch

### crazyflie-firmware/tools/crazyflie-simulation/simulator_files/mujoco/drone-models

- Upstream URL: https://github.com/utiasDSL/drone-models.git
- Pinned commit: `512c864ffa55081ef4e80fadde2e861f22f45943`
- License: metadata MIT classifier; 원문/asset grant 미확정
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyswarm2_ws/src/crazyswarm2

- Upstream URL: https://github.com/llanesc/crazyswarm2.git
- Pinned commit: `2334b7a32432fd3f9e1133c52361ddcc27ca3cf7`
- License: MIT main; 개별 header 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: setup_sources의 exact checkout
- Local modification / patch: patches/crazyswarm2/0001-baseline.patch

### crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools

- Upstream URL: https://github.com/llanesc/crazyflie_tools.git
- Pinned commit: `c684de4a81e57106453f8e604e1daa3f5b16d800`
- License: MIT main; 개별 header 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp

- Upstream URL: https://github.com/llanesc/crazyflie_cpp.git
- Pinned commit: `38b625ceda620868166feb9c0bf82df153d08203`
- License: MIT main; 개별 header 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp/crazyflie-link-cpp

- Upstream URL: https://github.com/llanesc/crazyflie-link-cpp.git
- Pinned commit: `4821cbd48ad667ec19c760b10414b8c0b138b309`
- License: MIT main; 개별 header 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp/crazyflie-link-cpp/libusb

- Upstream URL: https://github.com/libusb/libusb.git
- Pinned commit: `683e3cf21ed37d4492c20cea8de810c4d95ae8b6`
- License: LGPL v2.1 계열
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyswarm2_ws/src/crazyswarm2/crazyflie/deps/crazyflie_tools/crazyflie_cpp/crazyflie-link-cpp/pybind11

- Upstream URL: https://github.com/pybind/pybind11.git
- Pinned commit: `5b0a6fc2017fcc176545afe3e09c9f9885283242`
- License: BSD-3-Clause main; 파일별 예외
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: 상위 pinned gitlink의 recursive submodule
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-lib-python

- Upstream URL: https://github.com/bitcraze/crazyflie-lib-python.git
- Pinned commit: `3c1cb0d024fef6f45d08f0ad236a22ac395dd924`
- License: GPL v2 전문 / v2-or-later header / GPLv3 metadata; binary 별도
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: setup_sources의 exact checkout
- Local modification / patch: 없음 (하위 component 별도)

### crazyflie-lib-python-fpv

- Upstream URL: https://github.com/bitcraze/crazyflie-lib-python.git
- Pinned commit: `70d10a13a5f61258dd9677a875b85ff32bfae135`
- License: GPL v2 전문 / v2-or-later header / GPLv3 metadata; binary 별도
- Distribution model: NOT VENDORED / FETCHED FROM UPSTREAM
- How obtained: optional --with-legacy-fpv
- Local modification / patch: patches/crazyflie-lib-python-fpv/0001-baseline.patch

## Asset와 binary

drone-models의 STL/model/texture, cflib Nordic binary, legacy firmware source는 Public Git 후보에 포함하지 않습니다. upstream의 불명확한 권리가 해결됐다는 선언은 아닙니다. 다운로드한 directory, QA repro, cache 또는 build 산출물을 공개 archive에 묶으면 이 Thin repository의 범위를 벗어나므로 별도 검토가 필요합니다.

실제 remote는 개발 baseline의 llanesc 등 fork를 포함합니다. Bitcraze 공식 repo로 임의 치환하면 검증된 SHA/수정이 사라질 수 있어 변경하지 않았습니다. utiasDSL/drone-models URL은 현재 learnsyslab으로 redirect되지만 manifest에는 원본에서 관찰한 URL을 유지합니다.
