# CelSwap
[![GNU LGPLv3 license](https://img.shields.io/badge/license-LGPLv3-blue.svg)](https://github.com/Celshade/CelSwap/blob/master/LICENSE.LESSER)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-green.svg)](https://www.python.org/)

_A simple way to update SPL-token metadata_


<gif>

***

## System Requirements:
_This program was created on WSL2 and is intended for use with Linux/Unix compatible systems._
_Windows OS functionality has not yet been tested_

1. **Python [3.11+]**:
    * See docs and install instructions -> [here](https://www.python.org/)
1. **Solana CLI**:
    * See docs and install instructions -> [here](https://docs.solana.com/cli/install-solana-cli-tools)
1. **Bundlr CLI**: (requires NodeJS LTS or greater)
    * See docs and install instructions -> [here](https://docs.bundlr.network/developer-docs/sdk/installing-the-sdk)
    * **Make note of where bundlr is installed on your machine (see _Configuration_ section below)**
1. **Metaboss**:
    * See docs and install instructions -> [here](https://metaboss.rs/installation.html)
    * [source_code](https://github.com/samuelvanderwaal/metaboss)

## Python Requirements:
1. **requests**: Installable via `pip install requests` [->PYPI docs<-](https://pypi.org/project/requests/)

***

## Program Configuration
Once the above requirements are installed, you'll need to update the \
`config.json` file (found in the CelSwap root directory) with the correct \
directory that contains your `bundlr` installation.

i.e.

Your config.json file should look something like this:

```
{
    "bundlr_dir": "/home/your_user_name/bundlr"
}
```

**DON'T FORGET YOUR SOLANA CONFIGRATION**

This program assumes you already have the wallet authority set in your solana \
config for any tokens that you plan on updating. Naturally, your RPC url should \
also be set appropriately to match where your token lives (mainnet | devnet). \
See the solana CLI docs for more information, but here are the basic commands \
to work with:

`solana config get` (shows current solana config) \
`solana config set --url` (sets RPC url) \
`solana config set --keypair` (sets wallet auth - use the ABSOLUTE path, not relative)
***

## Running CelSwap
All you need is the **token_address** for the SPL-token you wish to update \
and the desired attributes/values.

**CelSwap will NOT update attributes that do not already exist on the token** \
(Planned to be included in a future release)

To call the program, simply navigate to the CelSwap root directory, and call \
the program with a json string of `{token:address, attribute1:value, attribute2:value, ...}` \

i.e.

`python src/celswap.py -d '{"token": "iu7DGFv6LsdGb9THFGtdF3cSmpt8CwJjY527vnLzBcw", "base": "green", "glow": "magenta"}'`

The `-d` flag stands for the `DATA` being passed to the program. \
Run `python src/celswap.py -h` to see available command flags.

***

## Potential Hickups (aka bundlr)
Bundlr can cause some minor annoyances, depending on how it gets installed.

Bundlr dependencies may not be installed upon initial installation, and this \
program assumes that bundlr is not added to your $PATH by default (which is why \
we set up our `config.json` file).

It's important to make sure you're able to call bundlr before trying to run \
the program, so you'll first want to test this with a simple `--version` call. \
Navigate to your bundlr directory and run `npx bundlr --version` to confirm this.

If this doesn not work and you're getting dependency errors, make sure you're \
still inside the bundlr installation directory and run `npm install` to \
download the bundlr package requirements. From there, repeat the previous step.
