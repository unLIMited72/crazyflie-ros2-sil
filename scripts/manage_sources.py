#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact upstream/patch 검증. 기존 checkout을 reset/clean/pull하지 않습니다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(message):
    raise RuntimeError(message)

def run(args, cwd=None, capture=True):
    env = os.environ.copy()
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    result = subprocess.run(args, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE if capture else None,
                            stderr=subprocess.PIPE if capture else None)
    if result.returncode:
        fail(f"명령 실패: {' '.join(map(str, args))}\n{result.stderr or ''}")
    return result.stdout.strip() if capture else ''

def git(path, *args):
    return run(['git', '--no-optional-locks', '-C', str(path), *args])

def inside(relative):
    p = ROOT / relative
    if Path(relative).is_absolute() or not p.resolve().is_relative_to(ROOT) or '..' in Path(relative).parts:
        fail(f'허용 범위 밖 경로: {relative}')
    # Do not write through symlinks, even to another checkout inside ROOT.
    for ancestor in [p, *p.parents]:
        if ancestor == ROOT:
            break
        if ancestor.is_symlink():
            fail(f'symlink 경로 거부: {ancestor}')
    return p

def state(entry):
    p = inside(entry['path'])
    if not (p / '.git').exists():
        if p.exists() and any(p.iterdir()):
            fail(f"Git이 아닌 기존 경로: {entry['path']}; 덮어쓰지 않습니다.")
        return 'missing'
    if Path(git(p, 'rev-parse', '--show-toplevel')).resolve() != p.resolve():
        fail(f"독립 upstream checkout이 아님: {entry['path']}")
    if not Path(git(p, 'rev-parse', '--absolute-git-dir')).resolve().is_relative_to(ROOT):
        fail(f"외부 Git metadata 연결 거부: {entry['path']}")
    if git(p, 'remote', 'get-url', 'origin') != entry['url']:
        fail(f"remote 불일치: {entry['path']}")
    head = git(p, 'rev-parse', 'HEAD')
    if head != entry['commit']:
        fail(f"unexpected source revision: {entry['path']} ({head}); 기존 branch/HEAD를 변경하지 않습니다.")
    if git(p, 'diff', '--cached', '--name-only', '--ignore-submodules=all'):
        fail(f"staged 변경 발견: {entry['path']}; 사용자 index 보존을 위해 중단합니다.")
    changed = set(git(p, 'diff', 'HEAD', '--name-only', '--ignore-submodules=all').splitlines())
    expected = entry['expected_modified_files']
    if not changed:
        return 'clean'
    if changed != set(expected):
        fail(f"예상 밖 tracked 변경: {entry['path']}: {sorted(changed)}")
    for name, metadata in expected.items():
        f = p / name
        if not f.is_file() or f.is_symlink() or hashlib.sha256(f.read_bytes()).hexdigest() != metadata['sha256']:
            fail(f"patch 결과와 다른 파일: {entry['path']}/{name}; 강제 수정하지 않습니다.")
        if bool(f.stat().st_mode & 0o111) != metadata['executable']:
            fail(f"예상 밖 실행 권한: {entry['path']}/{name}")
    return 'patched'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='다운로드/적용 없이 검증')
    parser.add_argument('--with-legacy-fpv', action='store_true', help='실행 비필수인 구버전 FPV source도 준비')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'manifests/upstream_sources.yaml').read_text())
    if manifest['schema'] != 1:
        fail('지원하지 않는 manifest schema')
    entries = [e for e in manifest['sources'] if not e['optional'] or args.with_legacy_fpv or inside(e['path']).exists()]
    # Validate every existing checkout and all patch bytes BEFORE any source mutation.
    states = {}
    for e in entries:
        if len(e['commit']) != 40 or any(x not in '0123456789abcdef' for x in e['commit']):
            fail('40-character commit SHA가 필요합니다.')
        if not e['url'].startswith('https://github.com/'):
            fail('manifest에 검토되지 않은 upstream URL')
        for patch in e['patches']:
            data = inside(patch['path']).read_bytes()
            if hashlib.sha256(data).hexdigest() != patch['sha256']:
                fail(f"patch checksum 불일치: {patch['path']}")
            if b'GIT binary patch' in data:
                fail('binary patch는 이 Thin repository에서 허용하지 않습니다.')
        states[e['path']] = state(e)
    if args.check:
        for e in entries:
            actual = states[e['path']]
            desired = 'patched' if e['patches'] else 'clean'
            if actual != desired:
                fail(f"source/patch 미준비: {e['path']} ({actual}, 필요: {desired})")
            print(f"[PASS] SHA/patch {e['path']} {e['commit']}")
        return
    for e in entries:
        if e['parent'] is not None:
            continue
        p = inside(e['path'])
        if states[e['path']] == 'missing':
            print(f"[FETCH] {e['name']} exact commit 준비", flush=True)
            run(['git', '-c', 'core.autocrlf=false', 'clone', '--no-checkout', e['url'], str(p)], capture=False)
            run(['git', '-C', str(p), '-c', 'core.autocrlf=false', 'checkout', '--detach', e['commit']], capture=False)
        # Existing child heads were validated above. Missing submodules can be initialized safely.
        children = [x for x in entries if x['path'].startswith(e['path'] + '/')]
        if any(states[x['path']] == 'missing' for x in children):
            run(['git', '-C', str(p), '-c', 'core.autocrlf=false', 'submodule', 'update', '--init', '--recursive'], capture=False)
    # Recheck every recursively acquired revision BEFORE applying any patch.
    for e in entries:
        actual = state(e)
        if actual == 'missing':
            fail(f"submodule 획득 실패: {e['path']}")
    for e in entries:
        p = inside(e['path'])
        actual = state(e)
        if actual == 'patched':
            print(f"[SKIP] patch 이미 적용됨: {e['name']}")
            continue
        for patch in e['patches']:
            patchfile = inside(patch['path'])
            run(['git', '-C', str(p), 'apply', '--check', str(patchfile)])
            run(['git', '-C', str(p), 'apply', '--whitespace=nowarn', str(patchfile)])
            print(f"[PASS] patch 적용: {patch['path']}")
        actual = state(e)
        if actual != ('patched' if e['patches'] else 'clean'):
            fail(f"적용 후 hash 검증 실패: {e['path']}")
    print('[PASS] 모든 필수 upstream SHA와 patch 결과가 일치합니다.')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError) as exc:
        print(f'[FAIL] {exc}', file=sys.stderr)
        sys.exit(1)
