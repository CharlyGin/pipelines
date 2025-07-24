import os

from argparse import ArgumentParser


def build_and_push(
    username: str,
    token: str,
    tags: str,
    platforms: str,
    path: str,
    dockerfile_path: str | None = None,
    skip_scout: bool = False,
):
    print(
        """ /$$$$$$$                      /$$                          
| $$__  $$                    | $$                          
| $$  \ $$  /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$   /$$$$$$ 
| $$  | $$ /$$__  $$ /$$_____/| $$  /$$/ /$$__  $$ /$$__  $$
| $$  | $$| $$  \ $$| $$      | $$$$$$/ | $$$$$$$$| $$  \__/
| $$  | $$| $$  | $$| $$      | $$_  $$ | $$_____/| $$      
| $$$$$$$/|  $$$$$$/|  $$$$$$$| $$ \  $$|  $$$$$$$| $$      
|_______/  \______/  \_______/|__/  \__/ \_______/|__/      
                                                            """
    )

    print("############################# CHECKING DOCKER #############################")
    status: int = os.system("which docker")
    exitcode: int = os.waitstatus_to_exitcode(status=status)
    if exitcode < 0:
        print("Docker not found. Installing ...")
        os.system("apt update")
        os.system(
            "apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
        )

        status: int = os.system("which docker")
        exitcode: int = os.waitstatus_to_exitcode(status=status)
        if exitcode < 0:
            print("Failed to detect docker.")
            exit(-1)

    print("######################## LOGIN ######################")
    status: int = os.system(f"docker login --username {username} --password {token}")
    exitcode: int = os.waitstatus_to_exitcode(status=status)
    if exitcode < 0:
        print("Failed to login.")
        exit(-1)

    print("############################# BUILD IMAGE(S) #############################")
    status: int = os.system(
        f"docker buildx build --tag {tags} \
              --push \
              --platform {platforms} \
              {f'--file {dockerfile_path}' if dockerfile_path else ''} \
              {path}"
    )
    exitcode: int = os.waitstatus_to_exitcode(status=status)
    if exitcode < 0:
        print("Failed to build.")
        exit(-1)

    if skip_scout:
        exit(0)

    print("############################# SCOUT #############################")
    os.system("docker scout quickview")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="build_and_push_docker",
        description="build and push to docker repo",
    )

    parser.add_argument(
        "-t",
        "--tags",
        type=str,
        help="image tags",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--platforms",
        type=str,
        help="image platforms",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="dockerfile location",
        required=True,
    )
    parser.add_argument(
        "--path",
        type=str,
        help="build path",
        required=True,
        default=".",
    )
    parser.add_argument(
        "--skip-scout",
        action="store_true",
        help="Skip docker scout analysis after image build",
    )

    args = parser.parse_args()

    build_and_push(
        tags=args.tags,
        path=args.path,
        platforms=args.platforms,
        dockerfile_path=args.file,
        skip_scout=args.skip_scout,
    )
