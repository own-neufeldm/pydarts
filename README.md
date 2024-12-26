# pydarts

This is a Python app for tracking the score of a Darts game.

## Archive Notice

This project was abandoned in favor of [own.neufeldm/darts-tracker](https://github.com/own-neufeldm/darts-tracker).

## Requirements

This application requires Python v3.11 (or higher) to be installed. It was developed on and for
Windows (x64), though other common operating systems are probably supported too (not tested).

## Setup

Assuming your environment meets the requirements stated above, install like so on Windows:

1. clone this repository and `cd` into it
2. create a virtual environment (venv): `python -m venv .\.venv`
3. activate the virtual environment: `.\.venv\Scripts\Activate.ps1`
4. install pydarts in the virtual environment: `pip install -e .`
5. create an executable: `pyinstaller .\pydarts.spec`

You now have a portable executable at `.\dist\pydarts.exe` which you can move and run.

## Attributions

The following resources have been authored by other people:

| Resource                            | Attribution                                          |
| ----------------------------------- | ---------------------------------------------------- |
| [App icon](pydarts/icons/darts.ico) | [Icon by Smashicons](https://www.freepik.com/search) |

Thank you.

## Contributions

If you find a bug or want to contribute, feel free to open an issue or a pull request.
