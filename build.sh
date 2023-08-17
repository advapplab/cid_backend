#/bin/bash

repo='cfleu198'

docker build -f Dockerfile --no-cache -t $repo/cid_api .
