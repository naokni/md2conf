"""
Publish Markdown files to Confluence wiki.

Copyright 2022-2026, Levente Hunyadi

:see: https://github.com/hunyadi/md2conf
"""

import json
import unittest
from unittest.mock import patch

from requests import Session

from md2conf.api_base import ConfluenceSessionShared
from md2conf.api_types import ConfluenceVersion
from md2conf.api_v1 import ConfluenceSessionV1
from md2conf.api_v2 import ConfluenceSessionV2
from md2conf.options_api import ConfluenceSessionOptions
from md2conf.serializer import object_to_json_payload


class TestConfluenceVersionMessage(unittest.TestCase):
    def assert_version_message(self, api: ConfluenceSessionShared, api_version: ConfluenceVersion, path: str) -> None:
        with patch.object(api, "_put") as put:
            api.update_page(
                "1131155861",
                "<p>one two three</p>",
                title="Test page",
                version=2,
                message="Release 1.2",
            )

        put.assert_called_once()
        self.assertEqual(put.call_args.args[:2], (api_version, path))
        payload = json.loads(object_to_json_payload(put.call_args.args[2]))
        self.assertEqual(payload["version"]["message"], "Release 1.2")

    def test_v1_update_page_propagates_version_message(self) -> None:
        with Session() as http_session:
            api = ConfluenceSessionV1(
                http_session,
                options=ConfluenceSessionOptions(),
                domain="example.atlassian.net",
                base_path="/wiki/",
                space_key="SPACE",
            )
            self.assert_version_message(api, ConfluenceVersion.VERSION_1, "/content/1131155861")

    def test_v2_update_page_propagates_version_message(self) -> None:
        with Session() as http_session:
            api = ConfluenceSessionV2(
                http_session,
                options=ConfluenceSessionOptions(),
                api_url="https://example.atlassian.net/wiki/",
                domain="example.atlassian.net",
                base_path="/wiki/",
                space_key="SPACE",
            )
            self.assert_version_message(api, ConfluenceVersion.VERSION_2, "/pages/1131155861")


if __name__ == "__main__":
    unittest.main()
