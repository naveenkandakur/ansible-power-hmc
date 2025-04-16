#!/bin/bash

echo "======== $0 ========"
set -x
set -o errexit
set -o pipefail
set -o errtrace

# shellcheck disable=SC2317
err_report() {
    echo "Error running '$1' [rc=$2] line $3 "
}

trap 'err_report "$BASH_COMMAND" $? $LINENO' ERR

DIR="$(pwd)"
MODULE_DIR="$DIR/plugins/modules"
INV_PLUGIN_DIR="$DIR/plugins/inventory"
ROLE_DIR="$DIR/roles"
ROLE_LIST=`ls -1 $ROLE_DIR`
DOC_SRC_DIR="$DIR/docs/source"
DOC_BLD_DIR="$DIR/docs/build"

#ansible-doc-extractor --template $DOC_TEMPLATE $DOC_SRC_DIR $MODULE_DIR/*.py
[[ ! -d "$DOC_SRC_DIR"/modules ]] && mkdir -p "$DOC_SRC_DIR"/modules && mkdir -p "$DOC_SRC_DIR"/plugins
[[ ! -d "$DOC_SRC_DIR"/roles ]] && mkdir -p "$DOC_SRC_DIR"/roles
[[ ! -d "$DOC_BLD_DIR" ]] && mkdir -p "$DOC_BLD_DIR"

# generate the updated role documentations
for role in $ROLE_LIST
do
        cp $ROLE_DIR/$role/README.rst $DOC_SRC_DIR/roles/$role.rst
done
ansible-doc-extractor "$DOC_SRC_DIR"/modules "$MODULE_DIR"/*.py
ansible-doc-extractor "$DOC_SRC_DIR"/plugins "$INV_PLUGIN_DIR"/*.py


# create the html files
sphinx-build -b html $DOC_SRC_DIR $DOC_BLD_DIR

ls "$DOC_BLD_DIR"
touch "$DOC_BLD_DIR"/.nojekyll

rc=$?
exit "$rc"
