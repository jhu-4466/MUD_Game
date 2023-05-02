#!/bin/bash

# Define function to show help message
function handbook {
    echo ""
    echo "Usage: $0 [-b target]"
    echo ""
    echo "Options:"
    echo "  -b, --build TARGET   Specify the target to build (client/server)."
    echo "  -h, --help           Show this help message and exit."
}

# Define variables
BUILD=""
PROTO_PATH=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -b|--build)
            BUILD="$2"
            shift
            shift
            ;;
        -c)
            shift
            ;;
        -h|--help)
            handbook
            exit 0
            ;;
        *)
            echo "Error: Unknown option: $1"
            handbook
            exit 1
            ;;
    esac
done

# Check if the build target is specified
if [ -z "$BUILD" ]; then
    echo "Error: Build target not specified."
    handbook
    exit 1
fi

# Check if the build target is valid
if [[ "$BUILD" != "client" && "$BUILD" != "server" ]]; then
    echo "Error: Invalid build target: $BUILD"
    handbook
    exit 1
fi

# Set proto path based on build target
if [[ "$BUILD" == "client" ]]; then
    PROTO_PATH="../../Client/src/utils/proto"
elif [[ "$BUILD" == "server" ]]; then
    PROTO_PATH="../../Server/src/utils/proto"
fi
# Create proto path if it does not exist
if [[ ! -d "$PROTO_PATH" ]]; then
    mkdir -p "$PROTO_PATH"
    echo "Created $PROTO_PATH"
fi

# Output the build target
cd ./proto/
protoc --python_out="$PROTO_PATH" se_world.proto