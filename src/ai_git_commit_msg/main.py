# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import configparser
import pathlib
import subprocess

import typer

from ai_git_commit_msg.model import ollama

app = typer.Typer()


@app.command()
def entry(model: str | None = None):
    if model is None:
        model = "ollama"

    diff = get_git_diff()
    config_dir = pathlib.Path.home() / ".config" / "ai-git-commit-msg" / "config.ini"

    config = configparser.ConfigParser()
    if config_dir.exists():
        config.read(config_dir)

    print(ollama.request(diff, config))


def get_git_diff() -> str:
    output = subprocess.run(
        ["git", "diff", "--staged"], check=True, text=True, capture_output=True
    )
    return output.stdout


def main() -> None:
    app()
