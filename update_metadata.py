"""
Update the off_chain metadata for a given NFT.
This is intended for use by the authority of the NFT being modified.

Author: Celshade
"""
from typing import Union, Optional, Any


# TODO
# Accept a config of traits to update and their new values
#   Use json format (endpoint?)

# TODO 
# Get existing off_chain metadata
    # metaboss decode mint -a <address>  # Gets ON-CHAIN data

def get_off_chain_data(
    on_chain_data: dict[str, Optional[Any]] ) -> dict[str, Optional[Any]]:

# TODO
# Update existing fields to the provided values
#   Write new off-chain metadata
#   Upload new off-chain metadata


def modify_data() -> dict[str, Union[str, int]]:
    pass


# TODO
# Call METABOSS to update the data field of the on=chain data
#   Points to the updated off-chain metadata
