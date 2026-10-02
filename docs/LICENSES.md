# License와 고지

- [root LICENSE](../LICENSE): 사용자 original code, scripts/config/documentation에 대한 Apache-2.0 공식 원문.
- [THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md): fetched component URL/SHA/license/patch.
- [LICENSE_DESIGN](LICENSE_DESIGN.md): 적용 범위 및 Full Snapshot과의 차이.
- [patches/README](../patches/README.md): patch 원 license와 적용 순서.
- [SOURCE_PROVENANCE](SOURCE_PROVENANCE.md): recursive dependency 출처.
- [custom license scope](../manifests/custom_license_scope.json): 직접 관리 package 파일별 근거.

기존 OSRF test copyright/Apache header를 보존합니다. Bitcraze/Crazyswarm2 등의 고지와 patch license는 root Apache로 대체하지 않습니다. 동봉 license text는 공식 Apache 및 실제 baseline의 simulation MIT, Crazyswarm2 MIT, cflib GPL v2 전문입니다.

MuJoCo는 PyPI runtime dependency로 설치하며 model XML/mesh의 license를 대신하지 않습니다. snapshot에서 발견했던 drone-models/Nordic/legacy ST 관련 권리가 bootstrap으로 새로 부여되는 것은 아닙니다. PUBLIC READY WITH NOTES 같은 판정은 이 repository의 직접 공개 범위에 한정되며 법률 보증이 아닙니다.
