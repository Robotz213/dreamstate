# Dreamstate Package Manager

This project is intended to be a "project creator," capable of integrating with uv and other package managers.

Currently, it only creates Flask projects, but in the future, I plan to create projects for Celery, FastAPI, and so on.

## Usage

Add it using any installer (pip, pipx, etc)

```zsh
# Pip example
pip install dreamstate

ds version # or ds about

# Returns
DreamState Package Manager
Version: 1.0.0
Author: RobotzDev
License: MIT

# Creating a flask project
ds create-app flask@default

```
