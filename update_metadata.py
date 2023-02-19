"""
Update the off_chain metadata for a given NFT.
This is intended for use by the authority of the NFT being modified.

Author: Celshade
Current Requirements:
    solana CLI
    metaboss
    bundlr
"""
import json
from typing import Union, Optional, Any

from solana.rpc.async_api import AsyncClient


# TODO
# Accept a config of traits to update and their new values
#   Use json format (endpoint?)


def get_on_chain_data(address: str) -> dict[str, Optional[Any]]:
    """
    Return the on-chain metadata for the given token address.

    Args:
        address: The token address to get on-chain data for.
    """
    # metaboss decode mint -a <address>  # Gets ON-CHAIN data
    # TODO json convert to dict
    raise NotImplementedError


def get_off_chain_data(
    on_chain_data: dict[str, Optional[Any]]
) -> dict[str, Optional[Any]]:
    """
    Return the off-chain metadata for the given on-chain NFT metadata.

    Args:
        on_chain_data: The existing on-chain metadata.
    """
    raise NotImplementedError


# TODO
# Update existing fields to the provided values
#   Write new off-chain metadata
#   Upload new off-chain metadata


def create_updated_data(
    on_chain_data: dict[str, Optional[Any]],
    off_chain_data: dict[str, Optional[Any]],
    new_data: dict[str, Optional[Any]]
) -> dict[str, Union[str, int]]:
    """
    Return the updated on-chain and off-chain metadata.
    
    Args:
        on_chain_data: The existing on-chain metadata.
        off_chain_data: The existing off-chain metadata.
        new_data: The off-chain metadata we want to make use of.
    """
    raise NotImplementedError


def upload_off_chain():
    raise NotImplementedError


def upload_on_chain():
    raise NotImplementedError


# TODO
# Call METABOSS to update the data field of the on=chain data
#   Points to the updated off-chain metadata
