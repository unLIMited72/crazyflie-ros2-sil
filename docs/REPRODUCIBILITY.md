# 재현성 설계

Full Snapshot 대신 실제 remote + 40자리 SHA + 재현 가능한 patch를 사용합니다. 이 방식은 third-party source/mesh/blob를 직접 게시하지 않으면서 현재 baseline의 source version을 추적합니다. upstream의 availability와 허가 조건까지 대신 보장하지는 않습니다.

## 재구성 입력

- manifests/upstream_sources.yaml: 24개 recursive component의 URL, SHA, branch 참고값, parent, optional 여부, patch 순서·hash, 적용 후 파일 hash/mode.
- requirements/requirements.txt: 직접 의존성 설명.
- requirements/requirements-lock.txt: 실행 Python package version.
- requirements/build-tools.txt: pip/setuptools/wheel/setuptools-scm version.
- manifests/system_baseline.txt: Ubuntu/Python/ROS 관찰 baseline.
- custom ROS packages: repository에서 직접 관리.

YAML manifest는 JSON 표기(YAML 1.2 subset)를 사용하므로 bootstrap 초기에는 PyYAML 없이 Python stdlib로 읽습니다.

## 적용 순서

1. crazyflie-firmware pinned checkout 및 recursive submodule.
2. Crazyswarm2 pinned checkout 및 recursive dependency.
3. cflib pinned checkout.
4. 모든 recursive remote/HEAD를 manifest와 비교.
5. simulation 0001-baseline.patch → 0002-path-portability.patch.
6. crazyswarm2 0001-baseline.patch.
7. 선택한 경우에만 legacy FPV 0001-baseline.patch.
8. 결과 파일의 SHA256/실행 권한과 예상 tracked diff 목록 확인.
9. venv → cf2 → rosdep → colcon → 환경 검사.

firmware root/cflib main에는 직접 local diff가 없어 빈 patch를 만들지 않습니다. simulation/drone-models 등 submodule SHA는 상위 gitlink와 manifest를 함께 확인합니다. git submodule update에 --remote를 사용하지 않습니다.

## 그대로 보존한 동작

cf231, UDP URI 19850, firmware 19950, raw camera 5200, CPX 5050, Kalman 2/PID 1, camera 324×244 mono8, camera delay 4초/server delay 7초를 유지합니다. scene 4개와 Flow Deck implementation은 pinned upstream 그대로입니다. CPX --camera-only의 CRTP 분리는 baseline patch로 재현합니다.

Full Snapshot 전용 .gitattributes bytes 보정, firmware versionTemplate의 snapshot manifest fallback, cflib pyproject fallback은 가져오지 않았습니다. 이 구조에서는 upstream 자체의 .git이 존재합니다. setup_python은 baseline 관찰 cflib distribution version을 명시합니다.

## 재실행과 개발 변경

setup_sources --check는 네트워크나 patch 쓰기 없이 모든 존재하는 mandatory/optional source를 검사합니다. root checkout이 다른 SHA거나 staged/알 수 없는 tracked 변경이면 FAIL입니다. 올바른 patch가 이미 적용돼 있으면 재적용하지 않습니다.

현재 검사는 tracked source와 patch target을 다룹니다. build가 만든 ignored/untracked 산출물은 삭제하지 않습니다. 새 파일로 upstream의 동작을 확장했다면 baseline verification과 별도로 해당 내용을 검토·기록해야 합니다.

## 검증 기준과 한계

Ubuntu 22.04.5 LTS, Python 3.10, ROS2 Humble 환경에서 fresh clone-equivalent를 사용해 실제 bootstrap/build를 시험합니다. 상세 결과는 QA_REPORT.md입니다.

필수 node: /crazyflie_server, /aideck_camera_node. 필수 topic: /cf231/pose, /cf231/status, /cf231/tof, /cf231/flow, /cf231/camera/image_raw. camera는 324×244 mono8/79056 bytes를 검사합니다. 18 Hz는 성능 관찰값입니다.

commit/patch/Python version을 고정해도 APT/ROS 업데이트, rosdep 데이터, PyPI wheel availability, compiler, GPU/OpenGL, 네트워크 상태까지 bit-for-bit 고정되지는 않습니다. Ubuntu image/container lock과 wheel hash lock은 이번 baseline 범위에 추가하지 않았습니다. fetch된 source를 포함해 배포하는 container/archive는 Thin repository와 다른 재배포 범위이므로 별도 라이선스 검토가 필요합니다.
