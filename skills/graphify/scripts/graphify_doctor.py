#!/usr/bin/env python3
"""Inspect Graphify installation and project graph state."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".turbo",
    "graphify-out",
}

INTERESTING_EXTS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".md",
    ".mdx",
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".gdoc",
    ".gsheet",
    ".gslides",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".mp3",
    ".mp4",
    ".wav",
    ".m4a",
}

GOOGLE_NATIVE_EXTS = {".gdoc", ".gsheet", ".gslides"}
MEDIA_EXTS = {".mp3", ".mp4", ".wav", ".m4a"}


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 20) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except FileNotFoundError as exc:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": str(exc)}
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "returncode": None,
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": f"timed out after {timeout}s",
        }


def compact_text(value: str, limit: int = 1200) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + "...[truncated]"


def read_text(path: Path, limit: int = 4096) -> str | None:
    try:
        return path.read_text(errors="replace")[:limit]
    except OSError:
        return None


def cli_shebang(cli: str | None) -> str | None:
    if not cli:
        return None
    try:
        first = Path(cli).read_text(errors="replace").splitlines()[0]
    except (OSError, IndexError):
        return None
    if first.startswith("#!"):
        return first[2:].strip()
    return None


def import_version(python_path: str | None) -> dict[str, Any]:
    if not python_path:
        return {"ok": False, "reason": "no python interpreter found from graphify CLI"}
    cmd = [
        python_path,
        "-c",
        (
            "import importlib.metadata as m; "
            "print(m.version('graphifyy'))"
        ),
    ]
    result = run(cmd)
    if result["ok"]:
        return {"ok": True, "package": "graphifyy", "version": result["stdout"]}
    return {"ok": False, "stderr": compact_text(result["stderr"])}


def find_git_head(project: Path) -> str | None:
    result = run(["git", "rev-parse", "HEAD"], cwd=project, timeout=10)
    if result["ok"]:
        return result["stdout"].strip()
    return None


def load_graph_metadata(graph_json: Path) -> dict[str, Any]:
    if not graph_json.exists():
        return {}
    try:
        data = json.loads(graph_json.read_text(errors="replace"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"error": str(exc)}

    meta: dict[str, Any] = {}
    if isinstance(data, dict):
        graph = data.get("graph")
        if isinstance(graph, dict):
            for key in ("built_at_commit", "built_at", "version", "graphify_version"):
                if key in graph:
                    meta[key] = graph[key]
        for key in ("built_at_commit", "built_at", "version", "graphify_version"):
            if key in data:
                meta[key] = data[key]
        nodes = data.get("nodes")
        links = data.get("links") or data.get("edges")
        if isinstance(nodes, list):
            meta["node_count"] = len(nodes)
        if isinstance(links, list):
            meta["edge_count"] = len(links)
    return meta


def count_files(project: Path, limit: int = 10000) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    total = 0
    stopped = False
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            total += 1
            suffix = Path(filename).suffix.lower() or "[no-ext]"
            if suffix in INTERESTING_EXTS:
                counts[suffix] += 1
            if total >= limit:
                stopped = True
                break
        if stopped:
            break
    return {
        "total_seen": total,
        "truncated": stopped,
        "interesting_extensions": dict(sorted(counts.items())),
    }


def google_pointer_summary(project: Path) -> dict[str, Any]:
    total = 0
    converted = 0
    missing: list[str] = []
    for path in project.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in GOOGLE_NATIVE_EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(project).parts):
            continue
        total += 1
        target = path.with_suffix(".md")
        if target.exists():
            converted += 1
        else:
            missing.append(str(path.relative_to(project)))
    return {
        "total": total,
        "converted_to_markdown": converted,
        "missing_markdown": missing,
    }


def codex_config_state() -> dict[str, Any]:
    config = Path.home() / ".codex" / "config.toml"
    text = read_text(config)
    if text is None:
        return {"path": str(config), "exists": False}
    return {
        "path": str(config),
        "exists": True,
        "multi_agent_true": bool(re.search(r"(?m)^\s*multi_agent\s*=\s*true\s*$", text)),
    }


def inspect(project: Path) -> dict[str, Any]:
    project = project.resolve()
    cli = shutil.which("graphify")
    shebang = cli_shebang(cli)
    python_path = None
    if shebang:
        python_path = shebang.split()[0]

    help_result = run([cli, "--help"], timeout=20) if cli else None
    combined_help = ""
    if help_result:
        combined_help = "\n".join([help_result.get("stdout", ""), help_result.get("stderr", "")])

    stale_match = re.search(
        r"warning:\s*skill is from graphify\s+([^,]+),\s*(?:but\s+)?package is\s+([0-9][0-9A-Za-z_.-]*)",
        combined_help,
        flags=re.IGNORECASE,
    )
    stale_skill_version = stale_match.group(1).rstrip(".") if stale_match else None
    stale_package_version = stale_match.group(2).rstrip(".") if stale_match else None

    out_dir = Path(os.environ.get("GRAPHIFY_OUT", project / "graphify-out"))
    if not out_dir.is_absolute():
        out_dir = project / out_dir

    graph_json = out_dir / "graph.json"
    report = out_dir / "GRAPH_REPORT.md"
    needs_update = out_dir / "needs_update"
    graphifyignore = project / ".graphifyignore"
    graph_meta = load_graph_metadata(graph_json)
    git_head = find_git_head(project)

    findings: list[str] = []
    if not cli:
        findings.append("graphify CLI was not found on PATH")
    if stale_match:
        findings.append(
            f"installed platform skill may be stale: skill {stale_skill_version}, package {stale_package_version}"
        )
    if not graph_json.exists():
        findings.append("graphify-out/graph.json was not found")
    if graph_json.exists() and not report.exists():
        findings.append("graph.json exists but GRAPH_REPORT.md was not found")
    if needs_update.exists():
        findings.append("graphify-out/needs_update exists; graph may be stale")
    if git_head and graph_meta.get("built_at_commit") and graph_meta["built_at_commit"] != git_head:
        findings.append("graph built_at_commit differs from current git HEAD")

    result = {
        "project": str(project),
        "graphify": {
            "cli": cli,
            "cli_shebang": shebang,
            "tool_import": import_version(python_path),
            "help_ok": help_result["ok"] if help_result else False,
            "help_excerpt": compact_text(combined_help, 1200) if combined_help else "",
            "stale_skill_warning": {
                "present": bool(stale_match),
                "skill_version": stale_skill_version,
                "package_version": stale_package_version,
            },
        },
        "codex": codex_config_state(),
        "graph": {
            "out_dir": str(out_dir),
            "graph_json_exists": graph_json.exists(),
            "report_exists": report.exists(),
            "needs_update_exists": needs_update.exists(),
            "metadata": graph_meta,
            "current_git_head": git_head,
        },
        "project_hygiene": {
            "graphifyignore_exists": graphifyignore.exists(),
        },
        "google_workspace": google_pointer_summary(project),
        "project_files": count_files(project),
        "findings": findings,
    }
    result["recommendations"] = recommendations(result)
    return result


def recommendations(report: dict[str, Any]) -> list[str]:
    recs: list[str] = []
    project = shlex.quote(report["project"])
    graphify = report["graphify"]
    graph = report["graph"]
    codex = report["codex"]
    hygiene = report["project_hygiene"]
    google_workspace = report["google_workspace"]
    files = report["project_files"]
    ext_counts = files["interesting_extensions"]
    total = int(files["total_seen"])
    media_count = sum(ext_counts.get(ext, 0) for ext in MEDIA_EXTS)

    if not graphify["cli"]:
        recs.append('Install Graphify with: uv tool install --force "graphifyy[office,video,mcp]" && graphify install --platform codex')
    elif graphify["stale_skill_warning"]["present"]:
        recs.append("Refresh the package-managed platform skill with: graphify install && graphify codex install")

    if codex["exists"] and not codex["multi_agent_true"]:
        recs.append("Enable Codex skill calls by adding multi_agent = true under [features] in ~/.codex/config.toml")

    missing_google = google_workspace["missing_markdown"]
    if missing_google:
        recs.append(f"Export or convert {len(missing_google)} Google Workspace pointer files before indexing; .gdoc/.gsheet/.gslides are not native document contents")

    if total > 500 and not hygiene["graphifyignore_exists"]:
        recs.append("Create a .graphifyignore before a full run, or start with a focused subfolder")

    if media_count > 20:
        recs.append(f"Index media deliberately: {media_count} audio/video files may require transcription time and disk space")

    if not graph["graph_json_exists"]:
        recs.append(f"Build the initial graph with: cd {project} && graphify extract .")
    elif graph["needs_update_exists"]:
        recs.append(f"Refresh changed files with: cd {project} && graphify update .")
    elif graph["metadata"].get("built_at_commit") and graph["current_git_head"] and graph["metadata"]["built_at_commit"] != graph["current_git_head"]:
        recs.append(f"Graph commit differs from HEAD; refresh with: cd {project} && graphify update .")

    if graph["graph_json_exists"] and not graph["report_exists"]:
        recs.append(f"Rebuild report/clusters with: cd {project} && graphify cluster-only .")
    if graph["report_exists"]:
        recs.append("Read graphify-out/GRAPH_REPORT.md before answering architecture or relationship questions")

    deduped: list[str] = []
    seen: set[str] = set()
    for rec in recs:
        if rec not in seen:
            deduped.append(rec)
            seen.add(rec)
    return deduped


def print_text(report: dict[str, Any]) -> None:
    print(f"Project: {report['project']}")
    graphify = report["graphify"]
    print(f"Graphify CLI: {graphify['cli'] or 'not found'}")
    if graphify["tool_import"].get("ok"):
        print(f"Package: {graphify['tool_import']['package']} {graphify['tool_import']['version']}")
    else:
        print(f"Package import: {graphify['tool_import'].get('reason') or graphify['tool_import'].get('stderr') or 'failed'}")
    stale = graphify["stale_skill_warning"]
    if stale["present"]:
        print(f"Stale skill warning: skill {stale['skill_version']}, package {stale['package_version']}")

    codex = report["codex"]
    print(f"Codex config: {codex['path']} ({'exists' if codex['exists'] else 'missing'})")
    if codex["exists"]:
        print(f"Codex multi_agent=true: {codex['multi_agent_true']}")

    graph = report["graph"]
    print(f"Graph output: {graph['out_dir']}")
    print(f"graph.json: {graph['graph_json_exists']}")
    print(f"GRAPH_REPORT.md: {graph['report_exists']}")
    print(f"needs_update: {graph['needs_update_exists']}")
    if graph["metadata"]:
        print(f"Graph metadata: {json.dumps(graph['metadata'], sort_keys=True)}")

    hygiene = report["project_hygiene"]
    print(f".graphifyignore: {hygiene['graphifyignore_exists']}")

    google_workspace = report["google_workspace"]
    print(
        "Google Workspace pointers: "
        f"{google_workspace['converted_to_markdown']}/{google_workspace['total']} have Markdown derivatives"
    )

    files = report["project_files"]
    print(f"Files seen: {files['total_seen']}{' (truncated)' if files['truncated'] else ''}")
    if files["interesting_extensions"]:
        print(f"Interesting extensions: {json.dumps(files['interesting_extensions'], sort_keys=True)}")

    if report["findings"]:
        print("Findings:")
        for finding in report["findings"]:
            print(f"- {finding}")
    else:
        print("Findings: none")

    if report["recommendations"]:
        print("Recommended next steps:")
        for recommendation in report["recommendations"]:
            print(f"- {recommendation}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".", help="Project path to inspect")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    project = Path(args.project).expanduser()
    if not project.exists():
        print(f"Project path does not exist: {project}", file=sys.stderr)
        return 2

    report = inspect(project)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
