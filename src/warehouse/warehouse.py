from json import dumps, loads, JSONDecodeError
import logging
import pathlib


WAREHOUSE_DIR = pathlib.Path(__file__).parent.resolve()
lgr = logging.getLogger(__name__)

class Warehouse:

    def __init__(self, *, config_file_name="warehouse_config.json") -> None:
        self.config_file_name: bool = config_file_name    # this will change on which database it will be operating
        self.config: dict[str, bool | str | float | dict] = {}

    def load_config(self):
        file_path = f"{WAREHOUSE_DIR}\\..\\config\\{self.config_file_name}"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.config = loads(f.read())
        except OSError:
            lgr.error("Failed to open file")
        except JSONDecodeError as e:
            lgr.error("Failed to load config")
        except:
            lgr.critical("Unknown error")


    def load_data(self):
        pass

    def save_data(self):
        pass

    def listen_and_serve(self):
        """
        Listen for http
        """

try:
    #raise ValueError
    raise OSError
except ValueError:
    print("ValueError")
except IndexError:
    print("IndexError")
except:
    print("else")

