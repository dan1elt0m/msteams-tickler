# MSTeams-Tickler

MSTeams-Tickler is a command-line interface (CLI) tool that checks the expiration of Microsoft Teams tokens on macOS.


## Installation

To install MSTeams-Tickler, you can use pip:

```bash
pip install msteams-tickler
```

## Usage
Usage

To use MSTeams-Tickler, run:

```bash
mstc check
```

or for MSTeams classic 
```bash
mstc classic check
```

MSTeams uses a binarycookies file to store the tokens.  MSTeams-Tickler looks for the binarycookies file at the default location.
If you have the binarycookies file at a different location, you can specify the path to the binarycookies file using the `--cookies-path` option:

```bash
mstc check --cookies-path /path/to/cookies.binarycookies --token-name other_token
```
! MSTeams classic looks for a sqlite file at the default cookies location.  If you have the sqlite file at a different location,
you can specify the path to the sqlite file using the `--cookies-path` option:

## Contributing
If you want to contribute to MSTeams-Tickler, feel free to open an issue or submit a pull request.  

## License

MSTeams-Tickler is licensed under the MIT License. See LICENSE for more information.
