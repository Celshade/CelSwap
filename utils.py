import argparse
import json
import os
import shutil


# FIXME: Fix this context manager and ensure cleanup
class TempCel():
    """
    Manage a temporary working environment so user dirs are not polluted.

    This is a context manager. Any temporary files should be removed upon
    exit.
    >>> `with TempCel():`
    """
    def __init__(self) -> None:
        self.WORKING_DIR = "_CELSWAP_TEMP"

    def __enter__(self) -> None:
        """
        Enter the temp working environment.
        """
        try:
            # Check for existing temp dir, else create
            if not os.path.exists(f"{self.WORKING_DIR}"):
                os.mkdir(self.WORKING_DIR)
                # print("WORKING ENV CREATED")  # NOTE: TESTING

            # Move into the temp dir
            os.chdir(self.WORKING_DIR)
            # print("IN THE WORKING ENV")  # NOTE: TESTING
        except Exception as e:
            print("Error during setup")
            raise e

    def __exit__(self, *args, **kwargs) -> None:
        """
        Leave the temp working environment and cleanup.
        """
        try:
            # Exit the working dir before cleanup
            if os.path.abspath('.').endswith(self.WORKING_DIR):
                os.chdir("..")
            # Delete the working dir
            shutil.rmtree(self.WORKING_DIR)
            # print("WORKING DIR REMOVED")  # NOTE: TESTING
        except Exception as e:
            print("Error during clean up")
            raise e


def parse_cli_args() -> dict[str, str | int | float] | None:
    """
    Parse JSON CLI config and return it as a dict.
    """
    try:
        # init parser
        parser =  argparse.ArgumentParser()
        # Configure args: add as needed
        parser.add_argument(  # token data (JSON)
            "-d", "--data", type=str,
            help="Token address and desired attribute data in JSON format"
        )
        parser.add_argument(  # bool flag to control program prompts
            "-s", "--safe", action="store_true", default=True,
            help="Forces the program to run with confirmation prompts"
        )
        # Parse data
        args = parser.parse_args()
        if not args.data:
            return None
        config = json.loads(args.data)
        config["force"] = args.safe  # set `force` flag in the config dict

        # Validate config data
        assert isinstance(config, dict)
        assert "token" in config  # token_address

        return config
    except AssertionError as ae:
        print(f"Invalid json config: {ae}")
        raise ae
    except Exception as e:
        print(f"Error parsing data from the CLI: {e}")
        raise e

# NOTE: simple progress bar
# import sys
# import time

# def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.6+
#     count = len(it)
#     def show(j):
#         x = int(size*j/count)
#         print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count}", end='\r', file=out, flush=True)
#     show(0)
#     for i, item in enumerate(it):
#         yield item
#         show(i+1)
#     print("\n", flush=True, file=out)


# for i in progressbar(range(15), "Computing: ", 40):
#     time.sleep(0.1) # any code you need
