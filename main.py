import os
import subprocess


def run():
    os.chdir("project")
    subprocess.run(["uvicorn", "settings:app", "--reload"])


if __name__ == "__main__":
    run()
