set dotenv-load := true

alias b := build
alias r := run
alias c := clean

default:
    just -f Justfile --list

build:
    uv sync
    uv pip install -r requirements[dev].txt
    uv run pyinstaller lcu.spec
    # cp ./dist/lcu.exe ${INSTALL_DIR}

run:
    uv sync
    uv run python main.py

clean:
    rm -rfv .venv build dist