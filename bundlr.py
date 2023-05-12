import os
import json
import shutil
import subprocess


def get_bundlr_dir() -> str | None:
    """
    Return the directory for bundlr calls.

    Reads from a simple `config.json` file in the program root dir.

    `See project README for config file information`
    """
    try:
        with open("../config.json", 'r') as f:
            bundlr_dir = json.load(f).get("bundlr_dir")
            if bundlr_dir:
                return bundlr_dir
            else:
                raise ValueError("No bundlr directory found in config")

    except FileNotFoundError as fe:
        print(f"Error finding config file - check naming: {fe}")
    except Exception as e:
        print(f"Error reading bundlr config file: {e}")
        raise e


def get_bundlr_price(file: str, bundlr_node: int = 1) -> int:
    """
    Get the price [in lamports] to upload the given file to arweave.

    Args:
        file: The file to price-check.
        bundlr_node: The bundlr node to use (default=1).  NOTE: use default 95%
    """
    # Get filesize
    fsize = os.path.getsize(file)
    # Config bundlr_network url
    bundlr_node = f"https://node{bundlr_node}.bundlr.network"
    # Get the upload price
    price_command = f"npx bundlr price {fsize} -h {bundlr_node} -c solana"
    upload_price = int(
        subprocess.check_output(
            price_command, shell=True
        ).decode("utf-8").strip('\n').split().pop(-4)
    )
    return upload_price


def upload_file_to_arweave(file: str, bundlr_dir: str, bundlr_node: int = 1) -> None:
    raise NotImplementedError
