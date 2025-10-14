set dotenv-load := true

alias b := build
alias r := run
alias d := deploy

default:
    just -f Justfile --list

build:
    uv sync --group dev
    uv run pyinstaller lcu.spec

run:
    uv sync
    uv run python ./src/main.py

deploy:
    cp -v ./dist/lcu.exe ${INSTALL_DIR}
