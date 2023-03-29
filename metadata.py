import os
import json
from typing import Union, Optional, Any

import requests

# NOTE: Test token: CHYNQyNUxXkD97xgtHuJJFsHmjGVi8aakqFoXjGxySEB

# TODO
# Accept a config of traits to update and their new values
#   Use json format (endpoint?)


class MetadataService():
    def __init__(self, token_address: str) -> None:
        self.token = token_address
        self.uri: Optional[str] = None  # on_chain uri pointing to off_chain metadata
        self.metadata: dict[str, str] = {}  # off_chain metadata (traits)

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
            # Ensure the metada file exists
            assert os.path.exists(f"{token_address}.json")
            # Parse the uri
            with open(f"{token_address}.json", 'r') as f:
                metadata = json.loads(f.read())
                uri = metadata["data"]["uri"].strip("\x00")  # strip strays
            return uri
        except AssertionError as e:
            print("Could not find metadata file")
            raise e
        except Exception as e:
            print("Error parsing on_chain data")
            raise e

    def _get_off_chain_data(self, uri: str) -> dict[str, str]:
        """
        Return the off-chain metadata for the given uri.

        Args:
            uri: The on_chain uri pointing to the off_chain metadata.
        """
        try:
            # Get off_chain metadata
            res = requests.get(uri)
            assert res.status_code == 200
            # Parse the metadata and return
            return json.loads(res.text)
        except AssertionError as e:
            print("Error requesting metadata")
            raise e
        except Exception as e:
            print("Error getting off_chain data")
            raise e

    def _upload_off_chain_data(self):
        # TODO: bundlr
        raise NotImplementedError

    def _update_metadata_uri(self):
        # TODO metaboss
        raise NotImplementedError

    # TODO
    # Update existing fields to the provided values
    #   Write new off-chain metadata
    #   Upload new off-chain metadata

    def get_existing_data(self) -> None:
        """
        Establish the existing metadata.
        """
        try:
            self.uri = self._get_metadata_uri(self.token)
            self.metadata = self._get_off_chain_data(self.uri)
        except Exception as e:
            print("Error loading existing data")
            raise e

    def create_updated_data(
        self,
        off_chain_data: dict[str, Optional[Any]],
        new_data: str  # NOTE: JSON
    ) -> dict[str, Union[str, int]]:
        """
        Return the updated on-chain and off-chain metadata.

        The format of the new data must be in json format.

        Args:
            off_chain_data: The existing off-chain metadata.
            new_data: The off-chain metadata we want to make use of.
        """
        raise NotImplementedError

    # TODO
    # Call METABOSS to update the data field of the on=chain data
    #   Points to the updated off-chain metadata
