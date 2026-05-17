"""
GitHub Issue 自动分级脚本。

在 GitHub Actions 中读取 issue 事件，按严重度和类型打标签。
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

LABELS = {
    "priority:P0": ("b60205", "立即处理：无法启动、数据损坏、安全或大面积不可用"),
    "priority:P1": ("d93f0b", "高优先级：核心流程失败或稳定复现"),
    "priority:P2": ("fbca04", "中优先级：影响明确但有绕过方案"),
    "priority:P3": ("0e8a16", "低优先级：体验、文案、轻微改进"),
    "type:bug": ("d73a4a", "缺陷报告"),
    "type:feature": ("a2eeef", "功能建议"),
    "type:question": ("d4c5f9", "问题或咨询"),
    "needs:repro": ("ededed", "需要复现步骤或更多信息"),
}


def _load_issue():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if event_path and os.path.exists(event_path):
        with open(event_path, "r", encoding="utf-8-sig") as f:
            event = json.load(f)
        if "issue" in event:
            return event["issue"]
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            return json.load(f)
    raise SystemExit("No issue payload found")


def classify(issue: dict) -> list[str]:
    title = issue.get("title") or ""
    body = issue.get("body") or ""
    text = f"{title}\n{body}".lower()
    labels: list[str] = []

    if re.search(r"bug|错误|报错|失败|崩溃|闪退|无法|不能|exception|traceback|crash|error|failed", text):
        labels.append("type:bug")
    elif re.search(r"建议|希望|增加|优化|feature|enhancement|request", text):
        labels.append("type:feature")
    else:
        labels.append("type:question")

    if re.search(r"无法启动|打不开|启动失败|数据丢失|文件损坏|安全|泄露|所有人|全量|crash on startup|data loss|security", text):
        labels.append("priority:P0")
    elif re.search(r"上传失败|下载失败|合成失败|授权失败|登录失败|稳定复现|blocking|blocker|核心流程", text):
        labels.append("priority:P1")
    elif "type:bug" in labels:
        labels.append("priority:P2")
    else:
        labels.append("priority:P3")

    if "type:bug" in labels and not re.search(r"步骤|复现|日志|截图|版本|traceback|log", text):
        labels.append("needs:repro")
    return labels


def _api(method: str, path: str, payload: dict | None = None):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    if not token or not repo:
        print("GITHUB_TOKEN/GITHUB_REPOSITORY missing, dry-run only")
        return None
    url = f"https://api.github.com/repos/{repo}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        if exc.code == 422:
            return None
        raise


def ensure_label(name: str):
    color, description = LABELS.get(name, ("ededed", ""))
    _api("POST", "/labels", {"name": name, "color": color, "description": description})


def apply_labels(issue_number: int, labels: list[str]):
    for label in labels:
        ensure_label(label)
    _api("POST", f"/issues/{issue_number}/labels", {"labels": labels})


def main():
    issue = _load_issue()
    labels = classify(issue)
    issue_number = int(issue.get("number") or os.getenv("ISSUE_NUMBER") or 0)
    print("labels=" + ",".join(labels))
    if issue_number:
        apply_labels(issue_number, labels)


if __name__ == "__main__":
    main()
