#! /bin/bash

# Get current branch (use in docker build)
git_latest_commit=`git rev-parse HEAD`
git_branch=`git rev-parse --abbrev-ref HEAD`
docker_tag="$git_branch_$git_latest_commit"
# image_name='egor045/traveller_rest_api'
image_name='traveller_rest_api'
docker_file='Dockerfile'

echo 'Building image '$image_name:$docker_tag' from '$docker_file

/usr/bin/docker build \
    -t $image_name:$docker_tag \
    -f $docker_file \
    .

