#!/usr/bin/env bash

# Copyright 2022, DragonflyDB authors.  All rights reserved.
# See LICENSE for licensing terms.

## Building the dockements using docker as the build env
# Option
#	-b|--build [tagname] build the docker image locally, default to dragonfly_docs_builder
#	-r|--run <local volum> [image name] run the container and generate the build

IMAGE_NAME=dragonfly_docs_builder
LOCAL_VOLUME=/tmp/docs/content/commands
CURRENT_RELATIVE=`dirname "$0"`
ABS_SCRIPT_PATH=`( cd "$CURRENT_RELATIVE" && pwd )`

function build_image {
	if [ "$1" != "" ]; then
		IMAGE_NAME=$1
	fi
	echo "building a new image for the container [$IMAGE_NAME]"
	docker build -t ${IMAGE_NAME} .
	return $?
}

function generate_docs {
	if [ "$2" != "" ]; then
		IMAGE_NAME=$2
		LOCAL_VOLUME=$1
	else
		if [ "$1" != "" ]; then
			LOCAL_VOLUME=$1
		fi
	fi	
	echo "generating the documents using the docker image [$LOCAL_VOLUME] [$IMAGE_NAME]"
	if [ ! -d ${LOCAL_VOLUME} ]; then
		mkdir -p ${LOCAL_VOLUME} || {
			echo failed to generate local volume dir at ${LOCAL_VOLUME}
			return 1
		}
	fi
	docker run --rm -t -v ${LOCAL_VOLUME}:/tmp/docs/content/commands \
                ${IMAGE_NAME} ./generate_docs.sh -o /tmp/docs/content/commands
	return $?
}


if [ $# -lt 1 ]; then
	echo "usage: -b|--build [tagname] | -r|--run <local volum> [image name]"
	exit 1
fi

while [[ $# -gt 0 ]]; do
  case $1 in
	  -b|--build)
		  build_image $2
		  exit $?
		  ;;
	  -r|--run)
		  generate_docs $2 $3
		  exit $?
		  ;;
	   *)
		   echo "usage: -b|--build [tagname] | -r|--run <local volum> [image name]"
		   exit 1
		   ;;
   esac
done

