#!/bin/bash

#install a set of Visual Studio Code extensions.
extensions=(
  ms-python.python
  esbenp.prettier-vscode
  dbaeumer.vscode-eslint
  ms-python.vscode-pylance
  ms-toolsai.jupyter
)

# Loop through and install each extension
for extension in "${extensions[@]}"; do
  echo "Installing $extension..."
  code --install-extension "$extension" --force
done

echo "All extensions installed."
