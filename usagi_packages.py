"""Offline, single-file package manager for UsagiLang (Python 3.10+).

The package store is project-local. There is NO remote package registry,
dependency resolution, or automatic execution of downloaded code.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
from typing import Any

MANIFEST = "usagi-packages.json"
NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


class PackageError(Exception):
    pass


def project_root(start: Path) -> Path:
    start = start.resolve()
    if start.is_file():
        start = start.parent
    for directory in (start, *start.parents):
        if (directory / MANIFEST).is_file():
            return directory
    raise PackageError(f"{MANIFEST} 파일이 없어요. pkg init을 실행하세요.")


def load(root: Path) -> dict[str, Any]:
    path = root / MANIFEST
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PackageError(f"패키지 파일을 읽지 못했어요: {exc}") from None
    if not isinstance(manifest, dict) or not isinstance(manifest.get("dependencies"), dict):
        raise PackageError("패키지 파일의 dependencies 형식이 잘못됐어요.")
    return manifest


def save(root: Path, manifest: dict[str, Any]) -> None:
    target = root / MANIFEST
    tmp = root / (MANIFEST + ".tmp")
    tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    tmp.replace(target)


def validate_name(name: str) -> None:
    if not NAME.fullmatch(name):
        raise PackageError("패키지 이름은 영문자/숫자/_/-만 사용하고 숫자로 시작할 수 없어요.")


def safe_file(root: Path, relative: str) -> Path:
    item = Path(relative)
    if item.is_absolute() or item.suffix != ".usagi":
        raise PackageError("패키지 경로는 프로젝트 안의 상대 .usagi 파일이어야 해요.")
    resolved = (root / item).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise PackageError("프로젝트 밖의 파일에 접근할 수 없어요.")
    if not resolved.is_file():
        raise PackageError(f"패키지 파일이 없어요: {resolved}")
    return resolved


def resolve(name: str, importer: Path | None) -> Path:
    validate_name(name)
    root = project_root(importer if importer is not None else Path.cwd())
    manifest = load(root)
    path = manifest["dependencies"].get(name)
    if not isinstance(path, str):
        raise PackageError(f"설치되지 않은 패키지: {name}")
    return safe_file(root, path)


def command(argv: list[str], output: Any) -> int:
    if not argv:
        raise PackageError("사용법: pkg init | add NAME FILE | list | verify | remove NAME")
    operation = argv[0]
    root = Path.cwd().resolve()
    if operation == "init":
        if len(argv) != 1:
            raise PackageError("사용법: pkg init")
        if (root / MANIFEST).exists():
            raise PackageError("이미 패키지 파일이 있어요.")
        save(root, {"format": 1, "dependencies": {}})
        print(f"🐰 {MANIFEST} 생성!", file=output)
        return 0

    root = project_root(root)
    manifest = load(root)
    deps = manifest["dependencies"]
    if operation in ("add", "install"):
        if len(argv) != 3:
            raise PackageError("사용법: pkg add NAME SOURCE.usagi")
        name, source = argv[1:]
        validate_name(name)
        if name in deps:
            raise PackageError("같은 이름의 패키지가 이미 있어요. 먼저 remove를 사용하세요.")
        path = safe_file(root, source)
        store = root / ".usagi" / "packages"
        store.mkdir(parents=True, exist_ok=True)
        dest = store / (name + ".usagi")
        if dest.resolve() == path:
            raise PackageError("자기 자신을 설치할 수 없어요.")
        if dest.exists():
            raise PackageError("이미 같은 이름의 패키지 파일이 있어요.")
        shutil.copyfile(path, dest)
        deps[name] = dest.relative_to(root).as_posix()
        try:
            save(root, manifest)
        except OSError:
            dest.unlink()
            raise
        print(f"🐰 설치됨: {name}", file=output)
        return 0

    if operation == "remove":
        if len(argv) != 2:
            raise PackageError("사용법: pkg remove NAME")
        name = argv[1]
        old = deps.pop(name, None)
        if old is None:
            raise PackageError(f"설치되지 않은 패키지: {name}")
        save(root, manifest)
        # Never delete arbitrary paths stored in a possibly edited manifest.
        expected = (root / ".usagi" / "packages" / (name + ".usagi")).resolve()
        if isinstance(old, str) and (root / old).resolve() == expected:
            expected.unlink(missing_ok=True)
        print(f"🐰 제거됨: {name}", file=output)
        return 0

    if operation in ("list", "verify"):
        if len(argv) != 1:
            raise PackageError(f"사용법: pkg {operation}")
        for name, relative in sorted(deps.items()):
            validate_name(name)
            if not isinstance(relative, str):
                raise PackageError(f"잘못된 패키지 항목: {name}")
            path = safe_file(root, relative)
            print(f"{name}: {path.relative_to(root)}", file=output)
        if operation == "verify":
            print("🐰 모든 로컬 패키지 경로 확인 완료", file=output)
        return 0

    raise PackageError(f"알 수 없는 pkg 명령: {operation}")
