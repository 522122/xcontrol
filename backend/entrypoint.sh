#!/bin/sh
set -e

go version

cd /backend

if [ -d "xcontrol-cli" ]; then
  cd xcontrol-cli
  git pull
else
    git clone https://github.com/522122/xcontrol-cli.git
    cd xcontrol-cli
fi

go build -o /backend/out/cli
