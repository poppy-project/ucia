import unittest


class ImportTestCase(unittest.TestCase):
    def test_import(self):
        import rosa # noqa F401
        from rosa import Rosa # noqa F401

    def test_has_version(self):
        from rosa import __version__ # noqa F401
