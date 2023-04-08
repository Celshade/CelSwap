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
from pprint import pprint

from metadata import MetadataService
from utils import parse_cli_args, TempCel


def main():
    # Parse CLI for NFT data
    data = parse_cli_args()
    if not data:
        print("No data provided. Run with --help for more info.")
        return

    # Get the token addr and `force` flag
    token: str = data.pop("token")
    force: bool = data.pop("force")
    print(f"Token: {token}")  # NOTE: TESTING
    print(f"Attributes: {data}")  # NOTE: TESTING
    print(force)  # NOTE: TESTING
    print(type(force))  # NOTE: TESTING

    # print(os.path.abspath('.'))  # NOTE: TESTING
    if token:
        with TempCel():  # Manage a working dir to avoid user file pollution
            try:
                # TODO add progress bar? On iteration?
                # TODO add shell colors?
                # print("within context manager...")  # NOTE: TESTING
                # print(os.path.abspath('.'))  # NOTE: TESTING
                service = MetadataService(token_address=token, force=force)
                service.get_existing_data(show=True)
                # TODO update data
                # service._create_new_off_chain_data(new_data=data, show=True)
            except Exception as e:
                pass
        # print("left context_manager")  # NOTE: TESTING
        # print(os.path.abspath('.'))  # NOTE: TESTING


if __name__ == "__main__":
    main()
