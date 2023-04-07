"""
Update the metadata for a given NFT.
This is intended for use by the authority of the NFT being modified.

Assumptions:
    Solana config::keypair is set to the update authority of the target NFT

Author: Celshade

Python Requirements:
    requests
System Requirements:
    solana CLI
    metaboss
    bundlr
"""
import os
from pprint import pprint

from metadata import MetadataService
from utils import TempCel


def main():
    token = "iu7DGFv6LsdGb9THFGtdF3cSmpt8CwJjY527vnLzBcw"  # NOTE: devnet CKEY

    # print(os.path.abspath('.'))  # NOTE: TESTING
    with TempCel():  # Manage a working dir to avoid user file pollution
        try:
            # TODO add progress bar? On iteration?
            # TODO add shell colors?
            # print("within context manager...")  # NOTE: TESTING
            # print(os.path.abspath('.'))  # NOTE: TESTING
            # pass
            service = MetadataService(token_address=token)
            service.get_existing_data(show=True)
        except Exception as e:
            pass
    # print("left context_manager")  # NOTE: TESTING
    # print(os.path.abspath('.'))  # NOTE: TESTING


if __name__ == "__main__":
    main()
