#!/bin/bash

# Install packages using pip
pip install matplotlib Tk requests bs4

# Check if installation was successful
if [ $? -eq 0 ]; then
  echo "Installation successful"
else
  echo "Installation failed"
fi
