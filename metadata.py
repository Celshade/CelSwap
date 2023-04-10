import os
import json
from pprint import pprint
from typing import Any

import requests

# TODO
# Accept a config of traits to update and their new values
#   Use json format (endpoint?)


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
        self.uri: str | None = None  # on_chain uri -> off_chain metadata
        self.metadata: dict[str, Any] | None = None  # off_chain metadata
        self.existing_attributes: list[dict[str, str | int | float]] | None = None
        self.updated_attributes: list[dict[str, str | int | float]] | None = None
  
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
        except AssertionError as e:
            print("Could not find metadata file")
            raise e
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
        except AssertionError as e:
            print("Error requesting metadata")
            raise e
        except Exception as e:
            print(f"Error getting off_chain data: {e}")
            raise e

    def _create_new_off_chain_data(self,
            new_data: dict[str, str | int | float],
            show: bool = False
    ) -> None:
        # TODO FIXME: finish implementing
        # Preserve existing attributes in case not all are updated
        self.updated_metadata = self.metadata.copy()
        # Update attributes
        for attr in new_data:
            if attr in self.existing_attributes:
                self.updated_metadata["attributes"][attr] = new_data[attr]

        # Handle verbose
        if show:
            pprint(self.updated_metadata)
            print(self.updated_metadata == self.metadata)

    def _update_metadata_uri(self):
        # TODO metaboss
        raise NotImplementedError

    # TODO
    # Update existing fields to the provided values
    #   Write new off-chain metadata
    #   Upload new off-chain metadata

    def get_existing_data(self, show: bool = False) -> None:
        """
        Set attributes for the existing metadata.

        Args:
            show: Optional flag to print the metadata on calling the method.
        """
        try:
            self.uri = self._get_metadata_uri(self.token)
            self.metadata = self._get_off_chain_data(self.uri)
            self.existing_attributes = self.metadata.get("attributes")

            # Handle verbose
            if show:
                # pprint(self.metadata)
                print(f"Existing attributes: {self.existing_attributes}")
        except Exception as e:
            print(f"Error loading existing data: {e}")
            raise e

    def create_updated_data(self) -> dict[str, str | int | float]:
        raise NotImplementedError

    # TODO
    # Call METABOSS to update the data field of the on=chain data
    #   Points to the updated off-chain metadata
