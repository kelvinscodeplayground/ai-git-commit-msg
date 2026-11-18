# ai-git-helper

A command-line tool that writes Git commit messages for your staged changes using a local LLM served by [Ollama](https://ollama.com).

`git-helper` reads the output of `git diff --staged`, sends it to an Ollama model with a commit-message prompt, and streams the generated message to your terminal. It does not run `git commit` for you, so you can review or edit the message before committing.

## Features

- Generates a commit message from your staged diff.
- Runs fully locally: the diff is sent only to the Ollama server you configure.
- Streams the response as it is generated.
- Follows common Git conventions: short imperative subject line, optional wrapped body.

## Requirements

- Python 3.15 or newer
- [uv](https://docs.astral.sh/uv/)
- Git
- `curl` on your `PATH` (used to talk to the Ollama API)
- A running Ollama server with at least one model pulled, for example:

  ```sh
  ollama pull llama3
  ```

## Installation

Clone the repository and install the dependencies:

```sh
git clone <repository-url>
cd ai-git-helper
uv sync
```

### Install a prebuilt release

Download the `.whl` file from the [releases page](https://github.com/kelvinscodeplayground/ai-git-helper/releases), then install it as a tool:

```sh
uv tool install ./ai_git_helper-<version>-py3-none-any.whl
```

Or install directly from the release URL:

```sh
uv tool install https://github.com/kelvinscodeplayground/ai-git-helper/releases/download/v<version>/ai_git_helper-<version>-py3-none-any.whl
```

Replace `<version>` with the release version, for example `1.0.0`. After installing, run `git-helper` from any Git repository. Create the config file as described below.

To upgrade, run the install command again with `--force` and the newer wheel. To remove it, run `uv tool uninstall ai-git-helper`.

## Configuration

Create the config file at `~/.config/ai-git-helper/config.ini`:

```ini
[ollama]
host = http://localhost:11434
model = llama3
```

| Key     | Section  | Default                  | Description                                         |
| ------- | -------- | ------------------------ | --------------------------------------------------- |
| `host`  | `ollama` | `http://localhost:11434` | Base URL of the Ollama server.                      |
| `model` | `ollama` | _(none, required)_       | Name of the Ollama model used to generate messages. |

If `model` is not set, the tool exits with an error.

## Usage

1. Stage your changes:

   ```sh
   git add path/to/file
   ```

2. Generate a commit message:

   ```sh
   uv run git-helper
   ```

   The generated message is printed to the terminal.

3. Use the message to commit, for example:

   ```sh
   git commit -m "$(uv run git-helper)"
   ```

   Or copy the output and run `git commit` yourself to edit it first.

If nothing is staged, the tool exits with an error because the diff is empty.

## How it works

1. `get_git_diff()` in `src/ai_git_helper/main.py` runs `git diff --staged`.
2. `get_config()` loads `~/.config/ai-git-helper/config.ini`.
3. `ollama.request()` in `src/ai_git_helper/model/ollama.py` posts the diff to the Ollama `/api/generate` endpoint through `curl`, using the commit prompt in `src/ai_git_helper/model/prompts.py` as the system prompt.
4. The streamed tokens are printed as they arrive.

## Project structure

```
src/ai_git_helper/
├── __init__.py
├── main.py              # CLI entry point (Typer app) and Git/config helpers
└── model/
    ├── ollama.py        # Ollama API client (streaming)
    └── prompts.py       # Commit message system prompt
```

## Development

Run the tool from source with `uv run git-helper`. Dependencies are managed with `uv` and locked in `uv.lock`.

## Credits

The commit message prompt is adapted from the [Zed Editor](https://github.com/zed-industries/zed) prompt, Copyright (c) Zed Industries, Inc., licensed under GPL-3.0.

## License

This project is licensed under the GNU General Public License v3.0. See [license.md](license.md).
