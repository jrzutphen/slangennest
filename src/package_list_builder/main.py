from argparse import ArgumentParser
from pwinput import pwinput

from webdav3.client import Client

def main():
    parser = ArgumentParser(
        description="Build a list of packages in a directory",
        epilog="Example: main.py https://webdav.example.com/ username password /path/to/target/",
    )
    parser.add_argument("url", help="WebDAV server URL")
    parser.add_argument("username", help="WebDAV server username")
    parser.add_argument("password", help="WebDAV server password", nargs="?")
    parser.add_argument("target", default="/", help="Target directory to list", nargs="?")

    args = parser.parse_args()

    if not args.password:
        args.password = pwinput()

    client = Client({
        "webdav_hostname": args.url,
        "webdav_login": args.username,
        "webdav_password": args.password,
    })

    files = client.list(args.target)

    with open("build/packages.txt", "w", encoding="utf-8") as output:
        for file in files:
            if file.endswith(".tar.gz"):
                output.write(file + "\n")

if __name__ == "__main__":
    main()
