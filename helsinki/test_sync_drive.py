import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from sync_drive import (
    GoogleDriveAuth,
    GoogleDriveClient,
    compute_md5,
    sync_single_course,
)


class TestSyncDrive(unittest.TestCase):

    def test_compute_md5(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write("hello world")
            path = Path(f.name)
        try:
            self.assertEqual(compute_md5(path), "5eb63bbbe01eeed093cb22bb8f5acdc3")
        finally:
            path.unlink()

    def test_auth_plain_token(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write("ya29.sample_plain_token\n")
            path = Path(f.name)
        try:
            auth = GoogleDriveAuth(path)
            self.assertEqual(auth.access_token, "ya29.sample_plain_token")
        finally:
            path.unlink()

    def test_auth_json_token(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            json.dump({
                "access_token": "ya29.json_token",
                "refresh_token": "refresh_sample",
                "client_id": "client_id_sample",
                "client_secret": "client_secret_sample",
                "folder_id": "folder_12345",
            }, f)
            path = Path(f.name)
        try:
            auth = GoogleDriveAuth(path)
            self.assertEqual(auth.access_token, "ya29.json_token")
            self.assertEqual(auth.refresh_token, "refresh_sample")
            self.assertEqual(auth.folder_id_from_token, "folder_12345")
        finally:
            path.unlink()

    def test_sync_single_course_downloads(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            course_dir = Path(tmpdir) / "financial_economics_1"
            course_dir.mkdir()
            local_dl = course_dir / "downloads"
            local_dl.mkdir()

            mock_auth = MagicMock()
            mock_auth.access_token = "dummy_token"
            client = GoogleDriveClient(mock_auth)

            client.get_child_folder = MagicMock(side_effect=lambda pid, names: {"id": "dl_id", "name": "downloads"} if "downloads" in names else {"id": "bin_id", "name": "bin"})
            client.list_files = MagicMock(return_value=[{
                "id": "file_1_id",
                "name": "sample.pdf",
                "mimeType": "application/pdf",
                "md5Checksum": "abc1",
                "size": 100,
            }])

            downloaded = []
            def fake_download(file_id, mime, dest):
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(b"content")
                downloaded.append((file_id, dest))

            client.download_file = MagicMock(side_effect=fake_download)

            sync_single_course(client, "course_remote_id", "financial_economics_1", course_dir)

            self.assertEqual(len(downloaded), 1)
            self.assertTrue((local_dl / "sample.pdf").is_file())

    def test_sync_single_course_bin_upload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            course_dir = Path(tmpdir) / "maths_physics_3a"
            course_dir.mkdir()
            local_bin = course_dir / "bin"
            local_bin.mkdir()

            (local_bin / "exercise.org").write_bytes(b"org content")

            mock_auth = MagicMock()
            mock_auth.access_token = "dummy_token"
            client = GoogleDriveClient(mock_auth)

            client.get_child_folder = MagicMock(side_effect=lambda pid, names: None if "downloads" in names else {"id": "bin_id", "name": "bin"})
            client.list_files = MagicMock(return_value=[])

            uploaded = []
            def fake_upload(local_path, parent_id, existing_file_id=None):
                uploaded.append((local_path, parent_id))

            client.upload_file = MagicMock(side_effect=fake_upload)

            sync_single_course(client, "course_remote_id", "maths_physics_3a", course_dir)

            self.assertEqual(len(uploaded), 1)


if __name__ == "__main__":
    unittest.main()
