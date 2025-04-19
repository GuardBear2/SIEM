#!/bin/bash

# GuardBear package builder
# Copyright (C) 2015, GuardBear Inc.
#
# This program is a free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.
set -e

build_directories() {
  local build_folder=$1
  local guardbear_dir="$2"
  local future="$3"

  mkdir -p "${build_folder}"
  guardbear_version="$(cat guardbear*/src/VERSION| cut -d 'v' -f 2)"

  if [[ "$future" == "yes" ]]; then
    guardbear_version="$(future_version "$build_folder" "$guardbear_dir" $guardbear_version)"
    source_dir="${build_folder}/guardbear-server-${guardbear_version}"
  else
    package_name="guardbear-server-${guardbear_version}"
    source_dir="${build_folder}/${package_name}"
    cp -R $guardbear_dir "$source_dir"
  fi
  echo "$source_dir"
}

# Function to handle future version
future_version() {
  local build_folder="$1"
  local guardbear_dir="$2"
  local base_version="$3"

  specs_path="$(find $guardbear_dir -name SPECS|grep $SYSTEM)"

  local major=$(echo "$base_version" | cut -dv -f2 | cut -d. -f1)
  local minor=$(echo "$base_version" | cut -d. -f2)
  local version="${major}.30.0"
  local old_name="guardbear-server-${base_version}"
  local new_name=guardbear-server-${version}

  local new_guardbear_dir="${build_folder}/${new_name}"
  cp -R ${guardbear_dir} "$new_guardbear_dir"
  find "$new_guardbear_dir" "${specs_path}" \( -name "*VERSION*" -o -name "*changelog*" \
        -o -name "*.spec" \) -exec sed -i "s/${base_version}/${version}/g" {} \;
  sed -i "s/\$(VERSION)/${major}.${minor}/g" "$new_guardbear_dir/src/Makefile"
  sed -i "s/${base_version}/${version}/g" $new_guardbear_dir/src/init/guardbear-server.sh
  echo "$version"
}

# Function to generate checksum and move files
post_process() {
  local file_path="$1"
  local checksum_flag="$2"
  local source_flag="$3"

  if [[ "$checksum_flag" == "yes" ]]; then
    sha512sum "$file_path" > /var/local/checksum/$(basename "$file_path").sha512
  fi

  if [[ "$source_flag" == "yes" ]]; then
    mv "$file_path" /var/local/guardbear
  fi
}

# Main script body

# Script parameters
export REVISION="$1"
export JOBS="$2"
debug="$3"
checksum="$4"
future="$5"
src="$6"

build_dir="/build_guardbear"

source helper_function.sh

set -x

# Download source code if it is not shared from the local host
if [ ! -d "/guardbear-local-src" ] ; then
    # Use the correct branch and repository
    GUARDBEAR_BRANCH=${GUARDBEAR_BRANCH:-buildbranch3}
    git clone --branch "${GUARDBEAR_BRANCH}" --recurse-submodules https://github.com/GuardBear2/SIEM.git guardbear
    cd guardbear
    git submodule update --init --recursive
    short_commit_hash=$(git rev-parse --short HEAD)
    cd ..
else
    short_commit_hash="$(cd /guardbear-local-src && git config --global --add safe.directory /guardbear-local-src && git rev-parse --short HEAD)"
fi

# Build directories
source_dir=$(build_directories "$build_dir/server" "guardbear*" $future)

guardbear_version="$(cat $source_dir/src/VERSION| cut -d 'v' -f 2)"
# TODO: Improve how we handle package_name
# Changing the "-" to "_" between target and version breaks the convention for RPM or DEB packages.
# For now, I added extra code that fixes it.
package_name="guardbear-server-${guardbear_version}"
specs_path="$(find $source_dir -name SPECS|grep $SYSTEM)"

setup_build "$source_dir" "$specs_path" "$build_dir" "$package_name" "$debug"

set_debug $debug $sources_dir

# Installing build dependencies
cd $sources_dir
build_deps
build_package $package_name $debug "$short_commit_hash" "$guardbear_version"

# Post-processing
get_package_and_checksum $guardbear_version $short_commit_hash $src
