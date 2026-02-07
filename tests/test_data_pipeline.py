import json
import tempfile
import unittest
from pathlib import Path

from src.data_pipeline import (
    LocalFileSource,
    ManualInputSource,
    MeetingContextPipeline,
    create_non_google_pipeline,
)


class TestDataPipeline(unittest.TestCase):
    def test_manual_input_source_trims_space(self):
        source = ManualInputSource("  hello world  ")
        self.assertEqual(source.load(), "hello world")

    def test_local_json_is_normalized(self):
        with tempfile.TemporaryDirectory() as d:
            file_path = Path(d) / "sample.json"
            file_path.write_text('{"z":1,"a":2}', encoding="utf-8")
            loaded = LocalFileSource(file_path).load()
            self.assertEqual(json.loads(loaded), {"z": 1, "a": 2})

    def test_pipeline_aggregates_non_empty_blocks(self):
        pipeline = MeetingContextPipeline(
            [ManualInputSource(" first "), ManualInputSource(""), ManualInputSource("second")]
        )
        self.assertEqual(pipeline.build_context(), "first\n\nsecond")

    def test_factory_builds_pipeline_without_google_sources(self):
        pipeline = create_non_google_pipeline(
            manual_text="summary",
            file_paths=[],
            http_json_urls=[],
        )
        self.assertEqual(pipeline.build_context(), "summary")


if __name__ == "__main__":
    unittest.main()
