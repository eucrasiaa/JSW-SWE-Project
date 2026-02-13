#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "if failure, run as root!"
fi

show_help() {
    echo "Usage: ./dockTool.sh [option]"
    echo "Options:"
    echo "  -s    Start/Restart the project (Detached)"
    echo "  -b    Build/Rebuild images"
    echo "  -k    Kill/Stop and remove containers"
    echo "  -l    View real-time logs"
    echo "  -conn Connect (shell) to the web container"
    echo "  -h    Display this help message"
}

case "$1" in
    -s)
        echo "Starting project..."
        # -d for detached mode, so it runs in the background
        docker-compose up -d
        echo "Running at http://localhost:4413"
        ;;
    -b)
        echo "Building/Refreshing images..."
        docker-compose build --no-cache
        ;;
    -rb)
        echo "Full teardown and rebuild..."
        docker-compose down
        docker-compose up -d --build
        ;;
    -k)
        echo "Stopping and removing containers..."
        docker-compose down
        ;;
    -l)
        echo "Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    -conn)
        echo "Connecting to the web container..."
        # Uses the service name defined in docker-compose.yml
        docker-compose exec web /bin/bash
        ;;
    -h|--help)
        show_help
        ;;
    *)
        echo "Invalid option."
        show_help
        exit 1
        ;;
esac
