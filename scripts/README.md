# Building Commands Docs

## Overview
This directory contains a collection of scripts and dockerfile to generate the files that would be used for the website to show commands documents.
Using these scripts we can generate them either from local location or by accessing the file on the remote repository.

## Requirements
If you would like to run these scripts locally without using a docker image, you must install the following on you local machine (assuming your running on Ubuntu Linux):
- Python 3 (sudo apt install -y python)
- Python pip (wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py)
- Python virtual env (python3 -m pip install virtualenv)
- Git (sudo apt install -y git)

## Building Documents
### Building with Docker
The script generate_by_docker.sh allow building inside docker.
This script accept 2 options:
- --build [image name]: This option would build the docker image.
- --run [volume name] [image name]: this option would generate the files using the script generate_docs.sh and using option --clone for it.
Note that you can run the --build option and then use the docker image to run the script with other options.
For example:
Building the image:
```
./generate_by_docker.sh -b
```
Building the image with specific image name:
```
./generate_by_docker.sh -b build_image
```

Generating documentation using the image:
```
./generate_by_docker.sh -r
```
Generating the docs using you own volume:
```
./generate_by_docker.sh -b /path/to/my/host/volume
```
Generating the docks using your own volume and your own image name:
```
./generate_by_docker.sh -b /path/to/my/host/volume build_image
```

### Running from Terminal
The script generate_docs.sh is the "engine" for running the python script.
This would simplify the running of the python script and add some more options.
With this script, when running without command line options, it would clone [redis-doc](https://github.com/dragonflydb/redis-doc), to the local host, 
and write the result to /tmp/<unix timestamp>/docs/content directory.
The options for this script are:
- --clone  This would clone the files from https://github.com/dragonflydb/redis-doc.git into local directory and run on it (the default)
- --remote This would use the above URL to fetch files without copying them locally
- --output "dir name" This would place the generated files at the "dir name", default to /tmp/"current utc timestamp"/docs/content
- --local "input dir" Run this using a local files at location "input dir"
- --clean This would remove the build and log files
Note that the default is to run with --clone option

For example:
Building the documents using data from the [redis-doc](https://github.com/dragonflydb/redis-doc)
```
./generate_docs.sh
```

Building the documents using data from the [redis-doc](https://github.com/dragonflydb/redis-doc) with explicit cloning
```
./generate_docs.sh --clone
```

Building the documents using data from the [redis-doc](https://github.com/dragonflydb/redis-doc) without doing any cloning
```
./generate_docs.sh --remote
```

Building the documents using data from the [redis-doc](https://github.com/dragonflydb/redis-doc) after you already have it locally
```
./generate_docs.sh --local /path/to/files/from/redis-doc
```

Building the documents using data from the [redis-doc](https://github.com/dragonflydb/redis-doc) and setting output directory
./generate_docs.sh --clone --output /path/to/write/content

Cleaning up (this is best run with the option of the output directory since this cannot be derived directly)
./generate_docs.sh --clean --output /path/to/write/content

### Running directly (development mode)
The script that generates the output files to website is called generate_commands_docs.py
It is best to create and use python virtual environment for it, so you would not install all dependencies globally.
To install the required dependencies run:
```
pip3 install -r requirements.txt
```

This scripts accepts the following options:
- --output_dir "path" : Output directory to which result will be writing "path" (required).
- --local "path": Running with local repository "input file location" (optional)
Note that if you're not running with --local, the script will connect to the remote [redis-doc](https://github.com/dragonflydb/redis-doc), and generate the output by reading directly from there.
The resulting files will be writing to the output_dir that was passed to the script.
Note that this will place each command in a separate subdirectory and the content is writing to index.md file.
For example:
Building the content without using local files:
```
./generate_commands_docs.py  --output_dir /path/to/write/content
```

Building content using existing files from [redis-doc](https://github.com/dragonflydb/redis-doc)
```
./generate_commands_docs.py  --output_dir /path/to/write/content --local /path/to/files/from/redis-doc
```



## Manually Running
In order to run using the docker image, you would need to make sure that you have docker support on your host - [get docker](https://docs.docker.com/get-docker/).
Then you can either manually build
```
docker build -t dragonfly_docs_builder .
```
and 
```
docker run --rm -t -v <you local path>:/tmp/docs/content/commands \
                dragonfly_docs_builder ./generate_docs.sh -o /tmp/docs/content/commands
```
Or using the commands above
