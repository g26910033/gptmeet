from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import json
from urllib.request import urlopen


class DataSource(Protocol):
    """Abstract source for meeting context data."""

    def load(self) -> str:
        ...


@dataclass(slots=True)
class ManualInputSource:
    """Use direct user-provided text as the only data source."""

    text: str

    def load(self) -> str:
        return self.text.strip()


@dataclass(slots=True)
class LocalFileSource:
    """Read context from a local file.

    Supported formats:
    - .txt / .md : plain text
    - .json      : compact JSON string
    """

    path: Path

    def load(self) -> str:
        suffix = self.path.suffix.lower()
        content = self.path.read_text(encoding="utf-8")
        if suffix == ".json":
            return json.dumps(json.loads(content), ensure_ascii=False)
        return content.strip()


@dataclass(slots=True)
class HttpJsonSource:
    """Fetch JSON context from any HTTP endpoint.

    This intentionally replaces Google Docs/Sheets integrations with a
    generic endpoint pattern so the system remains provider-agnostic.
    """

    url: str

    def load(self) -> str:
        with urlopen(self.url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return json.dumps(payload, ensure_ascii=False)


class MeetingContextPipeline:
    """Aggregate and normalize meeting context without Google dependencies."""

    def __init__(self, sources: list[DataSource]) -> None:
        self.sources = sources

    def build_context(self) -> str:
        blocks: list[str] = []
        for source in self.sources:
            data = source.load()
            if data:
                blocks.append(data)
        return "\n\n".join(blocks)


def create_non_google_pipeline(
    manual_text: str = "",
    file_paths: list[str] | None = None,
    http_json_urls: list[str] | None = None,
) -> MeetingContextPipeline:
    """Factory for a fully Google-free pipeline configuration."""

    file_paths = file_paths or []
    http_json_urls = http_json_urls or []

    sources: list[DataSource] = []

    if manual_text.strip():
        sources.append(ManualInputSource(manual_text))

    for path in file_paths:
        sources.append(LocalFileSource(Path(path)))

    for url in http_json_urls:
        sources.append(HttpJsonSource(url))

    return MeetingContextPipeline(sources)
