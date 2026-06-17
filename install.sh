#!/bin/bash

# AirTransit CLI Installer for macOS and Linux

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
CYAN="\033[36m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}Installing AirTransit CLI...${RESET}"

# Determine installation directory
INSTALL_DIR="/usr/local/bin"
USE_SUDO=false

if [ ! -w "$INSTALL_DIR" ]; then
    # If /usr/local/bin is not writable by current user, use sudo
    echo -e "${YELLOW}Notice: Writing to $INSTALL_DIR requires administrator privileges (sudo).${RESET}"
    USE_SUDO=true
fi

# Target file path
TARGET="$INSTALL_DIR/transfer"

# Copy file
echo -e "Copying executable to $TARGET..."
if [ "$USE_SUDO" = true ]; then
    sudo cp transfer.py "$TARGET"
else
    cp transfer.py "$TARGET"
fi

# Make executable
echo -e "Setting permissions..."
if [ "$USE_SUDO" = true ]; then
    sudo chmod +x "$TARGET"
else
    chmod +x "$TARGET"
fi

echo -e "\n${BOLD}${GREEN}✓ Installation Completed successfully!${RESET}"
echo -e "You can now use the ${BOLD}transfer${RESET} command from any directory."
echo -e "\n${BOLD}Usage:${RESET}"
echo -e "  transfer send <filepath>"
echo -e "  transfer receive <code>"
