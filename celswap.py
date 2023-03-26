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
"""
from metadata import MetadataService
from utils import TempCel


def main():
    with TempCel():  # Manage a working dir to avoid user file pollution
        try:
            # TODO add progress bar? On iteration?
            # TODO add shell colors?
            pass
        except Exception as e:
            pass
