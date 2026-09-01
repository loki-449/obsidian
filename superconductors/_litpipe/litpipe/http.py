"""带限速和重试的 HTTP 会话。所有对外请求都走这里。"""

from __future__ import annotations

import time
from typing import Any

import requests

from .config import Config

_UA = "litpipe/0.1 (personal research tool; contact: {email})"


class Client:
    def __init__(self, cfg: Config):
        net = cfg.section("network")
        self.timeout = net.get("timeout", 30)
        self.retries = net.get("retries", 3)
        self.min_interval = net.get("min_interval", 0.5)
        self.email = net.get("contact_email") or ""
        self._last = 0.0

        self.session = requests.Session()
        self.session.headers["User-Agent"] = _UA.format(email=self.email or "n/a")
        proxy = net.get("proxy")
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    def _throttle(self) -> None:
        gap = time.monotonic() - self._last
        if gap < self.min_interval:
            time.sleep(self.min_interval - gap)
        self._last = time.monotonic()

    def get(self, url: str, **kwargs: Any) -> requests.Response | None:
        """失败返回 None 而不是抛异常 —— 单个源挂掉不该拖垮整条管道。"""
        kwargs.setdefault("timeout", self.timeout)
        last_error: Exception | None = None
        for attempt in range(self.retries):
            self._throttle()
            try:
                resp = self.session.get(url, **kwargs)
            except requests.RequestException as exc:
                last_error = exc
            else:
                if resp.status_code == 429 or resp.status_code >= 500:
                    last_error = RuntimeError(f"HTTP {resp.status_code}")
                else:
                    return resp
            time.sleep(2 ** attempt)
        print(f"  [http] 放弃 {url} ({last_error})")
        return None

    def get_json(self, url: str, **kwargs: Any) -> Any:
        resp = self.get(url, **kwargs)
        if resp is None or resp.status_code != 200:
            return None
        try:
            return resp.json()
        except ValueError:
            return None

    def download(self, url: str, dest, **kwargs: Any) -> bool:
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("allow_redirects", True)
        self._throttle()
        try:
            with self.session.get(url, stream=True, **kwargs) as resp:
                if resp.status_code != 200:
                    return False
                ctype = resp.headers.get("Content-Type", "")
                if "pdf" not in ctype.lower() and not url.lower().endswith(".pdf"):
                    return False
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("wb") as fh:
                    for chunk in resp.iter_content(1 << 15):
                        fh.write(chunk)
        except requests.RequestException:
            return False
        # 少于 10 KB 基本是错误页伪装成 PDF
        if dest.exists() and dest.stat().st_size < 10_000:
            dest.unlink(missing_ok=True)
            return False
        return dest.exists()
