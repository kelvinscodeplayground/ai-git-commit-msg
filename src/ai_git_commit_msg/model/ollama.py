# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import subprocess
from configparser import ConfigParser

from ai_git_commit_msg.model.prompts import SYS_PROP


def request(prompt: str, config: ConfigParser) -> str:
    host = (
        config.get("ollama", "host", fallback="http://localhost:11434")
        + "/api/generate"
    )
    model = config.get("ollama", "model", fallback=None)

    if not model:
        raise ValueError("ollama_model is not set in the config file")

    prompt_obj = {
        "model": model,
        "system": SYS_PROP,
        "prompt": prompt,
        "stream": False,
    }
    # post to host via curl

    # fmt: off
    output = subprocess.run([
        "curl", "-X", "POST", host,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(prompt_obj),
    ], check=True, capture_output=True, text=True)
    # fmt: on

    response = json.loads(output.stdout)

    return response["response"]
