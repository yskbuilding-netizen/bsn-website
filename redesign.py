"""
BSN(빌사남) 그룹 홈페이지 리뉴얼 스크립트
- 기존 페이지(id=25) 내용을 backup_page_25.html 로 백업
- 새 디자인으로 교체
"""
import os
import sys
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

# === .env 읽기 ===
ENV_PATH = Path(r"C:\Users\yskbu\OneDrive\Desktop\기타업무\AI\.env")
env = {}
for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip()

WP_URL = env["WP_SITE_URL"].rstrip("/")
WP_USER = env["WP_USERNAME"]
WP_PASS = env["WP_APP_PASSWORD"]
PAGE_ID = 25

token = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "bsn-redesign/1.0",
}

def api(method, path, body=None):
    url = f"{WP_URL}/wp-json/wp/v2{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[HTTP {e.code}] {e.read().decode('utf-8', 'ignore')}")
        raise

# === 1. 백업 ===
print(">> 현재 홈페이지 가져오는 중...")
current = api("GET", f"/pages/{PAGE_ID}?context=edit")
backup_path = Path(__file__).parent / "backup_page_25.html"
raw = current["content"].get("raw") or current["content"].get("rendered", "")
backup_path.write_text(
    f"<!-- title: {current['title'].get('raw') or current['title'].get('rendered','')} -->\n"
    f"<!-- modified: {current['modified']} -->\n\n"
    + raw,
    encoding="utf-8",
)
print(f"   백업 완료 -> {backup_path}")

# === 2. 새 콘텐츠 로드 ===
content_path = Path(__file__).parent / "new_content.html"
new_content = content_path.read_text(encoding="utf-8")

# === 3. 업데이트 ===
print(">> 새 디자인으로 업데이트 중...")
result = api("POST", f"/pages/{PAGE_ID}", {
    "title": "BSN(빌사남) 그룹",
    "content": new_content,
})
print(f"   완료! {result['link']}")
print("\n브라우저에서 확인하세요: " + result["link"])
