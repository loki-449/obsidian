"""配置加载。所有路径统一解析成绝对 Path。"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent      # _litpipe/
CONFIG_DIR = ROOT / "config"


def _load(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            f"缺少配置文件 {path}。settings.yaml 可从 settings.example.yaml 复制。"
        )
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


@dataclass
class Config:
    settings: dict[str, Any] = field(default_factory=dict)
    profile: dict[str, Any] = field(default_factory=dict)
    taxonomy: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "Config":
        return cls(
            settings=_load("settings.yaml"),
            profile=_load("field_profile.yaml"),
            taxonomy=_load("taxonomy.yaml"),
        )

    # -- 路径 ------------------------------------------------------------
    @property
    def vault(self) -> Path:
        return Path(self.settings["paths"]["vault"]).resolve()

    @property
    def notes_dir(self) -> Path:
        return self.vault / self.settings["paths"]["notes_dir"]

    @property
    def moc_dir(self) -> Path:
        return self.vault / self.settings["paths"].get("moc_dir", "00_MOC")

    @property
    def attachments_dir(self) -> Path:
        return self.vault / self.settings["paths"]["attachments_dir"]

    @property
    def zotero_data_dir(self) -> Path:
        return Path(self.settings["paths"]["zotero_data_dir"]).resolve()

    @property
    def zotero_db(self) -> Path:
        return self.zotero_data_dir / "zotero.sqlite"

    @property
    def work_dir(self) -> Path:
        d = self.vault / self.settings["paths"]["work_dir"]
        d.mkdir(parents=True, exist_ok=True)
        return d

    @property
    def pdf_cache(self) -> Path:
        d = self.vault / self.settings["resolve"]["pdf_cache"]
        d.mkdir(parents=True, exist_ok=True)
        return d

    # -- 常用分支 --------------------------------------------------------
    def section(self, *keys: str) -> dict[str, Any]:
        node: Any = self.settings
        for key in keys:
            node = node.get(key, {}) if isinstance(node, dict) else {}
        return copy.deepcopy(node) if isinstance(node, dict) else {}

    @property
    def thresholds(self) -> tuple[float, float]:
        th = self.profile.get("thresholds", {})
        return float(th.get("auto_accept", 6.0)), float(th.get("review", 3.0))
