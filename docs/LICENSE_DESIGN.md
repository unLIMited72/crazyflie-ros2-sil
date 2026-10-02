# Thin Repository의 라이선스 설계

## 공개하는 범위

사용자는 이번 작업에서 사용자 작성 original code를 Apache-2.0으로 공개한다고 명시했습니다. 이 지시를 근거로 crazysim_bringup metadata의 TODO/MIT를 Apache-2.0으로 통일했고, aideck_ros2_bridge의 기존 Apache 선언을 유지했습니다. root LICENSE는 공식 Apache 원문입니다.

package의 runtime/launch, setup metadata, resource marker를 검사했습니다. bridge는 자체 socket/frame 재조립/NumPy/ROS 메시지 구현이며 CPX ID 및 image header를 사용합니다. 확인한 baseline upstream에서 runtime 파일을 그대로 복사했다는 증거는 발견하지 못했습니다. 프로토콜 사용 자체를 source 복사라고 간주하지 않습니다. 사용자의 소유 선언과 실제 파일 검사에 근거한 적용이며 모든 외부 코드와의 독립 작성 관계를 증명하는 감사는 아닙니다.

ROS template test에는 Open Source Robotics Foundation의 Apache header가 있으므로 그대로 보존했습니다. 이를 사용자 original code라고 주장하거나 copyright를 바꾸지 않았습니다. setup.py 등 template 형태는 동일 Apache 조건을 유지합니다. 새 copyright 이름/기관은 생성하지 않았습니다. [파일별 범위](../manifests/custom_license_scope.json)를 참고하십시오.

## upstream-derived patch

simulation 및 Crazyswarm2 patch는 각각 MIT scope, legacy fpv.py patch는 원 GPL v2-or-later header scope를 따릅니다. 원문은 third_party/licenses에 보존합니다. root Apache는 patch의 기존 license를 대체하지 않습니다. patch 내용/연결되는 file/commit은 patches/README와 manifest에 기록합니다.

## Full Snapshot blocker의 변화

| 과거 직접 동봉 대상 | 이번 공개 repository | 남는 조건 |
|---|---|---|
| drone-models / mesh / texture | NOT VENDORED, firmware→simulation submodule로 upstream acquisition | upstream의 누락 license/asset 권리가 새로 해결된 것은 아님 |
| Nordic nrf51-s110-and-bl.bin | NOT VENDORED, cflib pinned checkout에서 acquisition | exact binary의 사용/재배포 조건은 upstream 기준 |
| legacy ST/ARM firmware source | NOT VENDORED, firmware recursive clone | downloaded source의 개별 조건 확인 |
| Crazyswarm2/cflib full trees | NOT VENDORED | original license/header를 downloaded tree에 보존 |
| custom bringup TODO/MIT | 사용자 선택에 따라 Apache-2.0 정합화 | 소유자 지시 및 보존된 template attribution |
| custom bridge | 기존 Apache-2.0 유지 | 기존 OSRF 고지 유지 |

따라서 과거 Full Snapshot의 DISTRIBUTION BLOCKED 판정을 새 Thin repository의 직접 배포 판정으로 그대로 복사하지 않습니다. 반대로 다운로드 경로를 바꿨다는 이유로 unknown asset의 권리가 생겼다고 주장하지도 않습니다.

## readiness의 범위

이 Thin repository 자체는 custom code + text patch + manifest + license notice를 공개하는 범위로 평가합니다. downloaded trees, QA repro, venv, build 산출물, container image, zip 전체 묶음은 범위 밖입니다. 공개 판정은 QA_REPORT.md에 기록하며 법률 보증이 아닙니다.

upstream 권리가 미확정인 파일을 추가로 재배포하려면 기존 LICENSE_AUDIT의 원 문제를 다시 확인해야 합니다. bootstrap을 통해 얻은 자료에도 upstream 조건이 적용됩니다.
