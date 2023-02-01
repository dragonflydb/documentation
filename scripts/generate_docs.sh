#!/usr/bin/env bash

# Copyright 2022, DragonflyDB authors.  All rights reserved.
# See LICENSE for licensing terms.

## This would generate files that would be used for the web site as documentation for the supported commands
## The build process is based on 2 components:
## 1. The input files taken from repo https://github.com/dragonflydb/redis-doc
## 2. The python script generate_commands_docs.py found under this directory
## Command line options:
##	--clone  This would clone the files from https://github.com/dragonflydb/redis-doc.git into local directory and run on it (the default)
##	--remote This would use the above URL to fatch files withtout copying them locally
##	-- output <dir name> This would place the generated files at the <dir name> default to /tmp/<date>/docs/content
##	--local <input dir> Run this using a local files at location <input dir>
##	--clean This would remove the build and log files
## Please note that the log from the python script is at /tmp/build_commands_documents_messages

function generate_docs {
	# create python virtual env for this
	cd ${ABS_SCRIPT_PATH}
	virtualenv docenv || {
		echo "failed to create virtual env to run python script"
		return 1
	}
	./docenv/bin/pip3 install -r requirements.txt || {
		echo "failed to install dependencies for the python script"
		rm -rf docenv
		return 1
	}
	mkdir -p ${OUTPUT_DIR} || {
		rm -rf docenv
		echo "failed to generate output directory at ${OUTPUT_DIR}"
		return 1
	}
	if [ "${RUN_LOCAL}" = "no" ]; then
		./docenv/bin/python3 generate_commands_docs.py --output_dir ${OUTPUT_DIR}
	else
		./docenv/bin/python3 generate_commands_docs.py --output_dir ${OUTPUT_DIR} --local ${INPUT_DIR}
	fi
	result=$?
	rm -rf ./docenv
	return ${result}

}

function do_cleanup {
	echo "cleaninng up"
	rm -rf ${GIT_CLONED_PATH} /tmp/build_commands_documents_messages.log ${OUTPUT_DIR}
	echo "finish cleaning ${GIT_CLONED_PATH} tmp/build_commands_documents_messages.log and ${OUTPUT_DIR}"
	return 0
}
function do_git_clone {
	current_dir=${PWD}
	echo "cloning into ${GIT_CLONED_PATH}"
	if [ ! -d ${GIT_CLONED_PATH}/redis-doc ]; then
		mkdir -p ${GIT_CLONED_PATH} || {
			echo "failed to create ${GIT_CLONED_PATH} to clone files into"
			return  1
		}
		cd ${GIT_CLONED_PATH} && git clone https://github.com/dragonflydb/redis-doc.git || {
			echo "failed to clone from redis docs"
			return  1
		}
	else
		cd ${GIT_CLONED_PATH}/redis-doc && git pull || {
			echo "failed to update docs repo"
			return 1
		}
	fi
	cd ${current_dir}
	
}

################# MAIN	########################################################

CURRENT_RELATIVE=`dirname "$0"`
ABS_SCRIPT_PATH=`( cd "$CURRENT_RELATIVE" && pwd )`

# Default values
CURRENT_DATE=$(date +%s)
OUTPUT_DIR=/tmp/${CURRENT_DATE}/docs/content
GIT_CLONED_PATH=/tmp/build_commands_docs/docs_repo
RUN_LOCAL="yes"
DO_CLONE="yes"
INPUT_DIR=${GIT_CLONED_PATH}/redis-doc

##	Process command line args
while [[ $# -gt 0 ]]; do
  case $1 in
	  -c|--clone)
		  DO_CLONE="yes"
		  RUN_LOCAL="yes"
		  INPUT_DIR=${GIT_CLONED_PATH}/redis-doc
		  shift
		  ;;
	  -r|--remote)
		  RUN_LOCAL="no"
		  DO_CLONE="no"
		  shift
		  ;;
	   -o|--output)
		   OUTPUT_DIR=$2
		   shift
		   shift
		   ;;
	    -l|--local)
	    	RUN_LOCAL="yes"
		DO_CLONE="no"
		INPUT_DIR=$2
		shift
		shift
		;;
	     -c|--clean)
		DO_DELETE="yes"
		shift
		;;
	      *)
		 echo "usage: [-l|--local <path to input files>] [-c|--clone (default option)] [-r|--remote] [-o|--output <path to output files>] [-d|--delete]"
		 exit 1
		 ;;
	esac
done

echo "Running cleanup ${DO_DELETE}, cloning ${DO_CLONE}, runing on local files ${RUN_LOCAL}, output will be writing to ${OUTPUT_DIR} taking files from ${INPUT_DIR}"

##	Run
if [ "${DO_DELETE}" = "yes" ]; then
	do_cleanup
	exit  0
fi


if [ "${DO_CLONE}" = "yes" ]; then
	do_git_clone
	if [ $? -ne 0 ]; then
		echo "failed to clone doc repo locally"
		exit 1
	else
		echo "successfully cloned doc repo to ${INPUT_DIR}"
	fi

fi

generate_docs

if [ $? -ne 0 ]; then
	echo "failed to generate docs"
	exit 1
else
	echo "successfully generated docs to ${OUTPUT_DIR}"
	exit 0
fi

