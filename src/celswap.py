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
from utils import TempCel, parse_cli_args, get_wallet_path


def main():
    # Parse CLI for NFT data
    data = parse_cli_args()
    if not data:
        print("No args provided. Run with --help for more info.")
        return

    # Get the token addr and `force` flag
    token: str = data.pop("token")
    force: bool = data.pop("force")
    image: str = data.pop("image")
    print(f"Token: {token}")  # NOTE: TESTING
    # print(f"Attributes: {data}")  # NOTE: TESTING
    # print(type(data))  # NOTE: TESTING
    # print(f"Force flag: {force}")  # NOTE: TESTING
    # print(type(force))  # NOTE: TESTING
    print(image)  # NOTE: TESTING

    # print(os.path.abspath('.'))  # NOTE: TESTING
    if token:
        # Init vars and service(s)
        wallet = get_wallet_path()
        # print(f"wallet: {wallet}\n")  # NOTE: TESTING
        # if image:  # TODO implement image handling
        service = MetadataService(
            token_address=token,
            auth_keypair=wallet,
            force=force
        )

        with TempCel():  # Manage a working dir to avoid user file pollution
            try:
                # TODO add progress bar? On iteration?
                # TODO add shell colors?
                # print("within context manager...")  # NOTE: TESTING
                # print(os.path.abspath('.'))  # NOTE: TESTING

                # Get existing data
                service.get_existing_data(show=True)
                # Create updated metadata
                service._update_attrs(new_data=data, show=True)
                service._upload_off_chain_data()
                # Update the metadata URI
                service.update_metadata()

            except Exception as e:
                pass
        # print("left context_manager")  # NOTE: TESTING
        # print(os.path.abspath('.'))  # NOTE: TESTING


if __name__ == "__main__":
    main()
