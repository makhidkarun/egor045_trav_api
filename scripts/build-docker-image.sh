#! /bin/bash

# Get current branch (use in docker build)

docker_tag=`git rev-parse --abbrev-ref HEAD`
image_name='egor045/traveller_rest_api'
docker_file='Dockerfile'

echo 'Building image $image_name:$branch from $docker_file'

/usr/bin/docker build \
    -t $image_name:$branch \
    -f $docker_file \
    .

