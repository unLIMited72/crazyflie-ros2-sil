# GitHub 공개 전 체크리스트

- [x] 사용자 original code의 Apache-2.0 선택 반영
- [x] root Apache와 upstream-derived patch 범위 구분
- [x] 실제 remote / full SHA / recursive dependency manifest 생성
- [x] mesh/texture/blob/upstream 전체 source를 직접 배포에서 제외
- [x] 기존 OSRF template 및 patch 원 license 보존
- [x] Fresh bootstrap / firmware / ROS2 build 확인
- [x] 사용자 보고: 실제 SIL launch, 두 ROS node 및 주요 topic 확인
- [x] 사용자 보고: camera 324×244 mono8, 79056 bytes, 283 frames, 18.79 Hz 확인
- [x] Runtime operation PASS / clean shutdown WARN 구분
- [x] takeoff/go_to/land 및 maneuver 센서 응답은 NOT TESTED로 기록
- [x] 실제 GitHub URL 확정 및 clone placeholder 교체
- [x] 사용자의 최초 stage/commit/Public repository 생성/push 승인 확인
- [ ] 게시 후 원격 main commit / PUBLIC visibility 최종 확인
- [ ] 게시된 repository에서 별도 fresh clone 재현 시험
- [ ] takeoff/go_to/land 및 Flow/ToF maneuver 응답 시험
- [ ] Ctrl+C clean shutdown issue 조사

게시 절차에서는 ignore, dry-run, 실제 staged tree, 파일 수/크기, binary/core/credential/license 검사를 모두 통과한 뒤 commit합니다. 공개 maintainer metadata와 기존 Git identity는 임의 변경하지 않습니다. 원격 생성과 push는 분리하고 목적지를 다시 확인합니다.

대상: https://github.com/unLIMited72/crazyflie-ros2-sil

다운로드한 upstream, qa, .venv/build/cache/core를 별도 zip/container로 공개하는 허가를 뜻하지 않습니다. Public working directory 전체를 압축해 업로드하지 마십시오.
