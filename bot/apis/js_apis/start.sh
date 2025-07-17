#!/bin/sh

mkdir -p /app
cd /app || exit
cp -r /code/. .

bun install
bun start
