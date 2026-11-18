import json
import subprocess
from configparser import ConfigParser


def request(prompt: str, sys_prompt: str, config: ConfigParser) -> str:
    host = (
        config.get("ollama", "host", fallback="http://localhost:11434")
        + "/api/generate"
    )
    model = config.get("ollama", "model", fallback=None)

    if not model:
        raise ValueError("ollama_model is not set in the config file")

    if prompt is None or prompt.strip() == "":
        raise ValueError("Prompt is empty")

    prompt_obj = {
        "model": model,
        "system": sys_prompt,
        "prompt": prompt,
    }
    # post to host via curl

    # fmt: off
    proc = subprocess.Popen([
        "curl", "-sS", "-N", "-X", "POST", host,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(prompt_obj),
    ], stdout=subprocess.PIPE, text=True)
    # fmt: on

    chunks: [str] = []
    for line in proc.stdout:
        if not line.strip():
            continue

        obj = json.loads(line)
        token = obj.get("response", "")
        chunks.append(token)
        print(token, end="", flush=True)

        if obj.get("done"):
            break

    proc.wait()

    return "".join(chunks)
