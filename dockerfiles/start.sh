#!/bin/bash
set -e

# if a some command has been passed to container, executes it and exit,
# otherwise runs bash
if [[ $@ ]]; then 
    eval $@
else 
    /bin/bash
fi
