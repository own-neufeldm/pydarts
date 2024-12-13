# pydarts

This is a Desktop app for tracking the score of a Darts game.

## Requirements

The following dependencies must already be installed on your system:

| Dependency                                  | Version |
| ------------------------------------------- | ------- |
| [python](https://www.python.org/downloads/) | ^3.12   |
| [pipx](https://pipx.pypa.io/stable/)        | ^1.6    |

This app was written on and for Windows 10 (x64). It may work on other operating systems but it is
not officially supported.

## Setup

Install the app using `pipx`, e.g. directly from GitHub using SSH:

```
$ pipx install git+ssh://git@github.com/own-neufeldm/pydarts.git

  installed package pydarts 2.0.0, installed using Python 3.12.5
  These apps are now globally available
    - pydarts.exe
done! ✨ 🌟 ✨
```

You can now run the app using `pydarts`.

Additionally, you can configure a shortcut to run the app from your Start Menu without opening a
Terminal first. To do so, create a shortcut named `PyDarts` in the
`C:\ProgramData\Microsoft\Windows\Start Menu\Programs` directory. Point it to the following target:
`pwsh.exe -w hidden -c pydarts`. You can use [this asset](./pydarts/assets/icon.ico) as icon.

> [!NOTE]
> If you do not have PowerShell 7 (`pwsh`) installed, use `powershell.exe` instead.

You can now run the app from your Start Menu using `PyDarts`.

## Attributions

The following resources have been authored by other people:

| Resource                            | Attribution                                          |
| ----------------------------------- | ---------------------------------------------------- |
| [App icon](pydarts/assets/icon.ico) | [Icon by Smashicons](https://www.freepik.com/search) |

Thank you.

## Contributions

If you find a bug or want to contribute, feel free to open an issue or a pull request.
