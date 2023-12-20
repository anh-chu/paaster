#!/bin/sh
ROOT_DIR=./

# Replace env vars in JavaScript and HTML files served by NGINX
find "$ROOT_DIR" -path ./proc/tty/driver -prune -type f \( -name "*.js" -o -name "*.html" \) -exec sed -i 's|VITE_NAME_PLACEHOLDER|'"$VITE_NAME"'|g' {} +
find "$ROOT_DIR" -path ./proc/tty/driver -prune -type f \( -name "*.js" -o -name "*.html" \) -exec sed -i 's|VITE_API_URL_PLACEHOLDER|'"$VITE_API_URL"'|g' {} +
