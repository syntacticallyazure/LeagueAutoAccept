set dotenv-load := true

alias b := build
alias r := run
alias c := clean
alias d := deploy

default:
    just -f Justfile --list

build:
    uv sync
    uv run pyinstaller lcu.spec

run:
    uv sync
    uv run python main.py

clean:
    git clean -fdx;

deploy:
    cp -v ./dist/lcu.exe ${INSTALL_DIR}
