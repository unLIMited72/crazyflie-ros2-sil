# 협업과 변경 원칙

main은 검증된 baseline, feature/*는 기능, fix/*는 bug fix, docs/*는 문서 branch입니다. PR에는 변경 목적, 관련 upstream SHA, patch 적용/재실행 검사, build 및 실제 runtime 검사 여부를 구분해 기록합니다.

직접 관리하는 package는 crazysim_bringup과 aideck_ros2_bridge입니다. 사용자 original code는 Apache-2.0이며 기존 third-party template/header는 유지합니다. source/asset를 새로 복사할 때는 먼저 출처와 재배포 조건을 확인합니다.

## Downloaded source 수정

상위 Git은 firmware/cflib/Crazyswarm2 checkout을 ignore합니다. 각 upstream 디렉터리의 git status/diff에서 변경을 확인하십시오. 수정 전 pinned commit을 확인하고 필요한 diff만 patches로 보존합니다. nested .git이나 source tree 전체를 git add -f 하지 않습니다.

patch를 갱신하면 manifest의 patch SHA256, 순서, expected_modified_files hash/mode도 함께 갱신해야 합니다. 자동 source verifier는 알려지지 않은 tracked 변경을 의도적으로 거부합니다. 개발 작업을 삭제하여 검사를 통과시키지 마십시오.

변경 PR은 새 checkout에서 setup_sources → 두 번째 setup_sources(SKIP) → setup_sources --check → bootstrap을 확인해야 합니다. 잘못된 SHA/patch/source를 넣었을 때 강제 적용 없이 FAIL하는지도 확인합니다.

## Commit 금지 대상

.venv, build, install, log, cache, qa, downloaded upstream, mesh/texture/blob를 commit하지 않습니다. release zip/container에 이 항목을 포함하면 Thin repository의 라이선스 감사 범위를 벗어납니다.

root LICENSE를 third-party derived patch의 license로 바꾸지 않습니다. 실제 GitHub URL이 정해지기 전 README placeholder를 임의 URL로 바꾸지 않습니다.
