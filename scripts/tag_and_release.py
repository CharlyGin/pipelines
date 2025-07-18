import os
import zipfile

from argparse import ArgumentParser


def tag_and_release(
    tag: str,
    pre_release: bool,
    app: str,
    build_dir_to_zip: str | None = None,
    zip_name: str = "archive.zip",
):
    print(
        """ /$$$$$$$$                         /$$$           /$$$$$$$            /$$                                        
 |__  $$__/                        /$$ $$         | $$__  $$          | $$                                        
    | $$  /$$$$$$   /$$$$$$       |  $$$          | $$  \\ $$  /$$$$$$ | $$  /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ 
    | $$ |____  $$ /$$__  $$       /$$ $$/$$      | $$$$$$$/ /$$__  $$| $$ /$$__  $$ |____  $$ /$$_____/ /$$__  $$
    | $$  /$$$$$$$| $$  \\ $$      | $$  $$_/      | $$__  $$| $$$$$$$$| $$| $$$$$$$$  /$$$$$$$|  $$$$$$ | $$$$$$$$
    | $$ /$$__  $$| $$  | $$      | $$\\  $$       | $$  \\ $$| $$_____/| $$| $$_____/ /$$__  $$ \\____  $$| $$_____/
    | $$|  $$$$$$$|  $$$$$$$      |  $$$$/$$      | $$  | $$|  $$$$$$$| $$|  $$$$$$$|  $$$$$$$ /$$$$$$$/|  $$$$$$$
    |__/ \\_______/ \\____  $$       \\____/\\_/      |__/  |__/ \\_______/|__/ \\_______/ \\_______/|_______/  \\_______/
                    /$$  \\ $$                                                                                      
                    |  $$$$$$/                                                                                      
                    \\______/                                                                                       """
    )

    # Checking dependencies
    print("========================= CHECKING DEPENDENCIES ========================")
    dependencies: list[str] = ["git", "gh"]
    missing_dependencies: list[str] = []
    for dependency in dependencies:
        status: int = os.system(f"which {dependency}")
        exitcode: int = os.waitstatus_to_exitcode(status=status)
        if exitcode < 0:
            missing_dependencies.append(dependencies)

    if missing_dependencies:
        print(
            f"Please install the following dependencies : {', '.join(missing_dependencies)}"
        )
        exit(-1)

    cur_path: str = os.path.abspath(".")
    os.chdir(app)

    # Create the git tag and push
    print("============================ CREATE GIT TAG ===========================")
    tag: str = tag + ("-pre" if pre_release else "")

    os.system(f"git tag {tag}")
    os.system("git push origin --tags")

    # Zip app
    print("================================ ZIP APP ===============================")
    print(f"Build Dir : {build_dir_to_zip}")
    if build_dir_to_zip:
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(build_dir_to_zip):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=build_dir_to_zip)
                    zipf.write(file_path, arcname)

    # Create a release
    print("=========================== CREATE RELEASE =============================")
    os.system(
        f'gh release create {tag} \
              --title "{"Pre-" if pre_release else ""}Release {tag}" \
              {"--prerelease" if pre_release else ""} \
              --notes "" \
              {zip_name if build_dir_to_zip else ""}'
    )

    os.chdir(cur_path)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="tag_and_release",
        description="tag your git repo",
    )

    parser.add_argument(
        "-t", "--tag", type=str, help="tag name you want", required=True
    )
    parser.add_argument(
        "-z",
        "--zip-name",
        type=str,
        help="Name of zip file. Default: archive.zip",
        default="archive.zip",
    )
    parser.add_argument("-b", "--build-dir", type=str, help="build directory to zip")
    parser.add_argument(
        "-p",
        "--pre-release",
        action="store_true",
        help="the final release will be a pre-release",
    )
    parser.add_argument("-a", "--app", type=str, help="path to app", required=True)

    args = parser.parse_args()
    tag_and_release(
        tag=args.tag,
        pre_release=args.pre_release,
        app=args.app,
        build_dir_to_zip=args.build_dir,
        zip_name=args.zip_name,
    )
