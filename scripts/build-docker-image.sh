#! /bin/bash

# Get current branch (use in docker build)
WRKDIR=/home/arthur/projects/egor-45_trav_api
git_latest_commit=`git rev-parse HEAD`
git_branch=`git rev-parse --abbrev-ref HEAD`
docker_tag="$git_branch_$git_latest_commit"
# image_name='egor045/traveller_rest_api'
image_name='traveller_api'
docker_file='Dockerfile'

cd $WRKDIR

cat ./scripts/api_version.py_template | \
    sed -e "s/GIT_LATEST_COMMIT/$git_latest_commit/" > \
    traveller_api/api_version.py
echo 'Building image '$image_name:$docker_tag' from '$docker_file

/usr/bin/docker build \
    -t $image_name:$docker_tag \
    -f $docker_file \
    .

