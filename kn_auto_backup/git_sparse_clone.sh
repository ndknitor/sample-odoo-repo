#!/bin/bash

function git_sparse_clone() (
  rurl="$1" localdir="$2" branch="$3" && shift 3
  mkdir -p "$localdir"
  cd "$localdir"

  git init
  git remote add -f origin "$rurl"

  git config core.sparseCheckout true

  # Loops over remaining args
  for i; do
    echo "$i" >> .git/info/sparse-checkout
  done

  git pull origin "$branch"
pwd
  for i; do
    mv $i/* ./
    rm -rf $i
  done
)

git_sparse_clone "$@"