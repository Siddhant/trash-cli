import unittest

from tests.put.support.fake_fs.fake_fs import FakeFs


class TestFakeFs(unittest.TestCase):
    def setUp(self):
        self.fs = FakeFs()

    def test(self):
        result = self.fs.ls("/")
        assert result == [".", ".."]

    def test_create_dir(self):
        self.fs.mkdir("/foo")
        result = self.fs.ls("/")
        assert result == [".", "..", "foo"]

    def test_find_dir_root(self):
        assert '/' == self.fs.find_dir_or_file('/').name

    def test_find_dir_root_subdir(self):
        self.fs.mkdir("/foo")
        assert 'foo' == self.fs.find_dir_or_file('/foo').name

    def test_create_dir_in_dir(self):
        self.fs.mkdir("/foo")
        self.fs.mkdir("/foo/bar")
        result = self.fs.ls("/foo")
        assert result == [".", "..", "bar"]

    def test_create_file(self):
        self.fs.mkdir("/foo")
        self.fs.mkdir("/foo/bar")
        self.fs.atomic_write("/foo/bar/baz", "content")

        result = self.fs.read("/foo/bar/baz")

        assert result == "content"

    def test_chmod(self):
        self.fs.make_file("/foo")
        self.fs.chmod("/foo", 0o755)

        assert oct(self.fs.get_mod("/foo")) == oct(0o755)

    def test_is_dir_when_file(self):
        self.fs.make_file("/foo")

        assert self.fs.isdir("/foo") == False

    def test_is_dir_when_dir(self):
        self.fs.mkdir("/foo")

        assert self.fs.isdir("/foo") == True

    def test_exists_false(self):
        assert self.fs.exists("/foo") == False

    def test_exists_true(self):
        self.fs.make_file("/foo")

        assert self.fs.exists("/foo") == True

    def test_remove_file(self):
        self.fs.make_file("/foo")
        self.fs.remove_file("/foo")

        assert self.fs.exists("/foo") == False

    def test_makedirs(self):
        self.fs.makedirs("/foo/bar/baz")

        assert self.fs.isdir("/foo/bar/baz")