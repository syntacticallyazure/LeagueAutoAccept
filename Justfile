build:
    uv sync --group dev
    uv run pyinstaller lcu.spec

run:
    uv sync
    -uv run python ./src/main.py
