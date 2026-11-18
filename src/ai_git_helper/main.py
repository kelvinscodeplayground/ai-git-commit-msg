import configparser
import pathlib
import subprocess

import typer

from ai_git_helper.model import ollama, prompts

app = typer.Typer()


@app.command()
def commit_msg(model: str | None = None):
    if model is None:
        model = "ollama"

    diff = get_git_diff()
    config = get_config()
    print(ollama.request(prompt=diff, sys_prompt=prompts.COMMIT_MESSAGE, config=config))


def get_config() -> configparser.ConfigParser:
    config_dir = pathlib.Path.home() / ".config" / "ai-git-helper" / "config.ini"

    config = configparser.ConfigParser()
    if config_dir.exists():
        config.read(config_dir)

    return config


def get_git_diff() -> str:
    output = subprocess.run(
        ["git", "diff", "--staged"], check=True, text=True, capture_output=True
    )
    return output.stdout


def main() -> None:
    try:
        app()
    except Exception as e:  # noqa: BLE001
        typer.secho(f"Error: {e}", fg=typer.colors.RED, bold=True, err=True)
        raise SystemExit(1)
