import os
import unittest

from uuid import uuid4

from scripts.build_and_push_docker import build_and_push

from dotenv import load_dotenv


class TestBuildAndPushDocker(unittest.TestCase):
    def test_build_and_push_docker(self):
        build_and_push(
            username=os.getenv("DOCKER_USERNAME"),
            token=os.getenv("DOCKER_PASSWORD"),
            tags=f"carlitog/basic-app:{uuid4()},carlitog/basic-app:latest",
            platforms="linux/arm64",
            path="./basic_app",
        )


if __name__ == "__main__":
    load_dotenv()
    unittest.main()
