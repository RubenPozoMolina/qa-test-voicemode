#!/bin/bash
export install_dir="/usr/local/bin"
export json=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
export url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(endswith("linux64.tar.gz"))')
echo $url
curl -s -L "$url" | tar -xz
chmod +x geckodriver
sudo mv geckodriver "$install_dir"

