import os
import json
from pprint import pprint
from typing import Any

import requests

from bundlr import get_bundlr_dir, get_bundlr_price


class MetadataService():
    """
    Update existing attribute data on an NFT.

    Args:
        token_address: The NFT token address.
        auth_keypair: The wallet auth for the NFT.
        force: Flag to bypass confirmation prompts.
    """
    def __init__(
            self,
            token_address: str,
            auth_keypair: str,
            force: bool,
    ) -> None:
        self.token = token_address
        self.auth_keypair = auth_keypair
        self.force = force
        # Non-init attrs
        self.uri: str = None  # on_chain uri -> off_chain metadata
        self.metadata: dict[str, Any] = None  # off_chain metadata
        self.existing_attrs: list[dict[str, str | int | float]] = None
        self.updated_attrs: list[dict[str, str | int | float]] = None

    def _get_metadata_uri(self, token_address: str) -> str:
        """
        Parse the on_chain metadata and return the uri for the off_chain
        metadata.

        Args:
            token_address: The token address.
        """
        # NOTE: metaboss decode mint can take a list with -l?
        try:
            # Get on_chain metadata
            os.system(f"metaboss decode mint -a {token_address}")
            assert os.path.exists(f"{token_address}.json")  # sanity check
            print("metadata decoded")  # NOTE: TESTING

            # Parse the uri
            with open(f"{token_address}.json", 'r') as f:
                metadata = json.loads(f.read())
                uri = metadata["uri"]
            return uri
        except Exception as e:
            print(f"Error parsing on_chain data: {e}")
            raise e

    def _get_off_chain_data(self, uri: str) -> dict[str, Any]:
        """
        Return the off-chain metadata for the given uri.

        Args:
            uri: The on_chain uri pointing to the off_chain metadata.
        """
        try:
            # Get off_chain metadata
            res = requests.get(uri)
            assert res.status_code == 200
            return json.loads(res.text)
        # except AssertionError as e:
        #     print("Something went wrong requesting metadata")
        #     raise e
        except Exception as e:
            print(f"Error getting off_chain data: {e}")
            raise e

    def _update_attrs(
        self,
        new_data: dict[str, str | int | float],
        show: bool = False
    ) -> None:
        """
        Update attributes to their new values and write the new metadata file.

        NOTE: This method will NOT upload to the new data to arweave.

        Args:
            new_data: The desired attributes and their values.
            show: Flag to output testing info (default=False).
        """
        # Preserve existing attributes in case not all are updated
        self.updated_attrs = self.existing_attrs.copy()

        # Update attributes
        for attr in self.updated_attrs:
            trait = attr["trait_type"]

            if attr["trait_type"] in new_data:
                new_value = new_data[trait]

                # Handle verbose
                if show:
                    print(f"Updated {trait}: {attr['value']} -> {new_value}")
                # Update the attribute
                attr["value"] = new_value

        # Update metadata
        self.metadata["attributes"] = self.updated_attrs

        # Write the updated metadata to file
        filename = "updated_metadata.json"
        with open(filename, 'w') as f:
            f.write(json.dumps(self.metadata))

        # Confirm existance of metadata file and set filepath
        assert os.path.exists(filename)
        self.metadata_path = os.path.abspath(filename)

    def _upload_off_chain_data(self) -> None:
        """
        Upload the updated metadata to arweave.

        NOTE: This requires a small amount of available lamports to fund the
        upload to arweave.
        """
        try:
            # Get pwd and bundlr dir
            curdir = os.path.abspath('.')
            bundlr_dir = get_bundlr_dir()
            print(f"\nbundlr_dir: {bundlr_dir}")  # NOTE: TESTING
            os.chdir(bundlr_dir)  # Nav to bundlr dir

            # Fund bundlr_node
            upload_price = get_bundlr_price(file=self.metadata_path)
            print(f"upload_price: {upload_price}")
            # TODO upload to arweave
            # TODO check for successful upload
            # TODO preserve uri
            # uri = None

            # Return to previous location
            os.chdir(curdir)
            # print(os.path.abspath('.'))  # NOTE: TESTING
        except FileNotFoundError as de:
            print(f"Error switching directories: {de}")
            raise de
        except Exception as e:
            print(f"Error updating off-chain metadata: {e}")
            raise e

    def _update_metadata_uri(self):
        raise NotImplementedError

    # TODO
    # Update existing fields to the provided values
    #   Upload new off-chain metadata

    def get_existing_data(self, show: bool = False) -> None:
        """
        Set attributes for the existing metadata.

        Args:
            show: Flag to output testing info (default=False).
        """
        try:
            self.uri = self._get_metadata_uri(self.token)
            self.metadata = self._get_off_chain_data(self.uri)
            self.existing_attrs = self.metadata.get("attributes")

            # Handle verbose
            if show:
                # pprint(self.metadata)
                print("Existing attributes:")
                pprint(self.existing_attrs)
        except Exception as e:
            print(f"Error loading existing data: {e}")
            raise e
