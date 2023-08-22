import re
from enum import Enum, auto

import ocrspace

from .config import api_key
from .db import PostDB
from .utils import logger


class ApiError(Exception):
    """Error API"""


# Instance of PostDB for insertion of data
db_insert = PostDB.insert_data


class IsAllowedState(Enum):
    ALLOWED = auto()
    NOT_ALLOWED = auto()
    NOT_VALID = auto()


class OcrValidator:
    @staticmethod
    def ocr(file: str) -> str:
        """
        :params: file as a path string
        :return: str (License plate number)
        """
        api = ocrspace.API(
            endpoint="https://api.ocr.space/parse/image", api_key=api_key
        )
        try:
            filename = file

            # A fixed list of strings without any whitespaces charecters
            result = api.ocr_file(open(filename, "rb")).splitlines()

            # Return the first the first element or an empty string if list is empty
            return result[0] if result != [] else ""

        except Exception as e:
            logger.warning(e, exc_info=True)
            raise ApiError(
                "There is something wrong with the api please check log for farther understanding"
            ) from e

    @staticmethod
    def license_validator(license_: str) -> str:
        """:return: ALLOWED/NOT_ALLOWED/NOT_VALID to enter the parking lot"""

        logger.info("Function is_allowed is running with %s", license_)

        state = IsAllowedState.ALLOWED.name

        try:
            # Check if there is any (non-digit || non-letter) in license_ charecters
            if re.sub(r"[a-zA-Z0-9]", "", license_):
                state = IsAllowedState.NOT_VALID.name
                return state

            # Check if last charecter in license_ is 6 or G
            if license_[-1] in ("6", "G"):
                state = IsAllowedState.NOT_ALLOWED.name
                db_insert(license_, state)
                return state

            # Check rather there is ('L' || 'M') in license_ charecters
            if "L" in license_ or "M" in license_:
                state = IsAllowedState.NOT_ALLOWED.name
                db_insert(license_, state)
                return state

            # Check if license_ charecters are all digits
            if False not in map(str.isdigit, license_):
                state = IsAllowedState.NOT_ALLOWED.name
                db_insert(license_, state)
                return state

        except Exception as err:
            logger.warning("License is an empty string! \n%s", str(err), exc_info=True)
            state = IsAllowedState.NOT_VALID.name
            return state

        finally:
            logger.info(
                "Function is_allowed done checking %s with status: %s", license_, state
            )

        db_insert(license_, state)
        return state
