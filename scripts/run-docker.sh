#! /bin/bash

# Args:
#   -p port(s)
#   -e environment var(s)

ENV="prometheus_multiproc_dir=/metrics"
PORTS="8000:8000"
IMAGE="egor045/traveller_api:latest"
NAME="api_dev"

POSITIONAL=()
while [[ $# -gt 0 ]] ; do
    key="$1"
    case $key in
        -e|--env)
            ENV="$2"
            shift
            shift;;
        -p|--publish)
            PORTS="$2"
            shift
            shift
            ;;
	-n|--name)
	    NAME="$2"
	    shift
	    shift
	    ;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done

if [ "$POSITIONAL" != "" ] ; then
    IMAGE="$POSITIONAL"
fi

set -- "${POSITIONAL[@]}"
echo Running docker image $IMAGE with env=$ENV, port=$PORTS

/usr/bin/docker run --rm --name $NAME -p $PORTS -e $ENV $IMAGE
