#!/bin/bash
# Script to fix Wazuh server build issues
# Issues addressed:
# 1. SOURCE_DATE_EPOCH environment variable
# 2. engine_precompiled_store.tar.gz extraction

set -e

echo "Fixing Wazuh build issues..."

# First, fix the SOURCE_DATE_EPOCH issue by adding it to the build environment
# Create a wrapper script that will be used when building in Docker
cat > packages/debs/utils/fix_date_epoch.sh << 'EOF'
#!/bin/bash
# Reset the SOURCE_DATE_EPOCH to current time
export SOURCE_DATE_EPOCH=$(date +%s)
echo "Set SOURCE_DATE_EPOCH to $SOURCE_DATE_EPOCH (current time)"

# Execute the original command
exec "$@"
EOF

chmod +x packages/debs/utils/fix_date_epoch.sh

# Modify the Docker run command in generate_package.sh to use our wrapper
sed -i 's|${CONTAINER_NAME}:${DOCKER_TAG} \\|${CONTAINER_NAME}:${DOCKER_TAG} /usr/local/bin/fix_date_epoch.sh \\|' packages/generate_package.sh

# Now, create a valid placeholder for the engine precompiled store
echo "Creating valid engine_precompiled_store placeholder..."

# Create directory structure
mkdir -p temp/engine/store/schema/engine-schema
mkdir -p temp/engine/store/schema/wazuh-logpar-overrides
mkdir -p temp/engine/kvdb

# Create placeholder files
echo "{}" > temp/engine/store/schema/engine-schema/0
echo "{}" > temp/engine/store/schema/wazuh-logpar-overrides/0
touch temp/engine/store/.placeholder
touch temp/engine/kvdb/.placeholder

# Create archive (format depends on platform)
if command -v tar &> /dev/null && command -v gzip &> /dev/null; then
    # Create tar.gz file
    cd temp
    tar -czf engine_precompiled_store.tar.gz engine
    cd ..
    mkdir -p src/engine
    cp temp/engine_precompiled_store.tar.gz src/engine/
    echo "Created tar.gz archive for engine store"
elif command -v 7z &> /dev/null; then
    # Use 7zip to create archive on Windows
    mkdir -p src/engine
    cd temp
    7z a -tgzip ../src/engine/engine_precompiled_store.tar.gz engine
    cd ..
    echo "Created tar.gz archive using 7z for engine store"
else
    echo "WARNING: Couldn't create tar.gz archive. Make sure tar and gzip or 7z are installed."
    # Copy directory structure as fallback
    mkdir -p src/engine
    cp -r temp/engine src/engine/store
    echo "Copied directory structure instead"
fi

echo "Fix script completed."
echo "Now you can run the build process again with these fixes in place." 