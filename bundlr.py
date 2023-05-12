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
    node = f"https://node{bundlr_node}.bundlr.network"
    # Get the upload price
    command = f"npx bundlr price {fsize} -h {node} -c solana"
    upload_price = int(
        subprocess.check_output(
            command, shell=True
        ).decode("utf-8").strip('\n').split().pop(-4)
    )
    return upload_price


def fund_bundlr_node(lamports: int, wallet: str, bundlr_node: int = 1) -> None:
    """
    Fund the bundlr node.

    NOTE: Funds will be taken from the current keypair designated in the solana
    config.

    Args:
        lamports: The number of lamports to fund the node with.
        wallet: The path to the funding wallet.
        bundlr_node: The bundlr node to use (default=1).  NOTE: use default 95%
    """
    # Config bundlr_network url
    node = f"https://node{bundlr_node}.bundlr.network"
    # Fund the node
    command = f"npx bundlr fund {lamports} -h {node} -w {wallet} -c solana"
    fund_message = int(
        subprocess.check_output(
            command, shell=True
        ).decode("utf-8").strip('\n').split().pop(-4)
    )


def upload_file_to_arweave(file: str, bundlr_node: int = 1) -> str:
    """
    Upload the file to arweave and return the destination url.

    Args:
        file: The file to upload.
        bundlr_node: The bundlr node to use (default=1).  NOTE: use default 95%
    """
    raise NotImplementedError
