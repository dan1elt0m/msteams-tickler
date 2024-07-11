# MSTeams-Tickler

MSTeams-Tickler is a command-line interface (CLI) tool that checks the expiration of Microsoft Teams tokens on macOS.

Currently only supports MS Teams classic (old version) on MacOs.


## Installation

To install MSTeams-Tickler, you can use pip:

```bash
pip install msteams-tickler
```

## Usage
Usage
To use MSTeams-Tickler, you can run the main script with Python:

```bash
msteams-tickler
```
By default, MSTeams-Tickler checks the token named "authtoken" in the Teams cookies sqlite file at "~/Library/Application Support/Microsoft/Teams/Cookies". 
If you want to check a different token or use a different cookies file, you can provide them as options:

```bash
msteams-tickler --cookies-path /path/to/cookies --token-name other_tokenh
```

## Contributing
If you want to contribute to MSTeams-Tickler, feel free to open an issue or submit a pull request.  

## License

MSTeams-Tickler is licensed under the MIT License. See LICENSE for more information.
