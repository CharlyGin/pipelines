import unittest

from datetime import datetime

from scripts.tag_and_release import tag_and_release


def gen_name(test: str) -> str:
    return datetime.today().strftime(f"{test}-%d-%m-%Y-%H-%M-%S-%f")


class TestTagAndRelease(unittest.TestCase):
    def test_release_success(self):
        tag_and_release(
            tag=gen_name("test_release_success"),
            pre_release=False,
            app="./basic_app",
        )

    def test_pre_release_success(self):
        tag_and_release(
            tag=gen_name("pre_release_success"),
            pre_release=True,
            app="./basic_app",
        )

    def test_release_build_zip_success(self):
        name: str = gen_name("release_build_zip_success")
        tag_and_release(
            tag=name,
            pre_release=False,
            app="./basic_app",
            build_dir_to_zip="./dist",
            zip_name=f"{name}.zip",
        )


if __name__ == "__main__":
    unittest.main()
