#!/bin/bash
commit=$1
if [[ "$commit" = "" ]]; then
  echo "missing argument: commit sha1" 1>&2
  exit 1
fi
git show -q $commit || exit 1
echo $commit > .unstable-release
echo include .unstable-release >> MANIFEST.in
python setup.py sdist upload
git checkout MANIFEST.in
rm .unstable-release
