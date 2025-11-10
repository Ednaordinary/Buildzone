#!/usr/bin/env bash

handle_uv() {
    uv venv .venv
    source .venv/bin/activate
    if [[ $(uv pip list | grep "pygame") == "" ]]; then
        uv pip install -r requirements.txt
    fi
}

handle_pip() {
    python3 -m venv .venv
    source .venv/bin/activate
    if [[ $(pip list | grep "pygame") == "" ]]; then
        pip install -r requirements.txt
    fi
}

if [[ ! $VIRTUAL_ENV ]]; then
    if [[ $(command -v uv) ]]; then
        handle_uv
    elif [[ $(command -v pip) ]]; then
        handle_pip
    else
        echo "I don't know other package managers. Quitting..."
    fi
fi

