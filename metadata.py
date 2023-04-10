import os
import json
from pprint import pprint
from typing import Any

import requests


class MetadataService():
    """
    Update existing attribute data on an NFT.

    Args:
        force: Flag to bypass confirmation prompts.
        token_address: The NFT token address.
    """
    def __init__(
            self,
            force: bool,
            token_address: str
    ) -> None:
        self.force = force
        self.token = token_address
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
            assert os.path.exists(f"{token_address}.json")
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
        Update attributes to their new values.

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

    def _update_off_chain_data(self):
        raise NotImplementedError

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

    def create_updated_data(self) -> dict[str, str | int | float]:
        raise NotImplementedError

    # TODO
    # Call METABOSS to update the data field of the on=chain data
    #   Points to the updated off-chain metadata
