import ocrspace
import regex as re

from config import api_key
from db import db_insert
from utils import logger


class OcrValidator():
    @staticmethod
    def ocr(file: str) -> str:
        """
        :params: file as a path string
        :return: str (License plate number)
        """
        api = ocrspace.API(
            endpoint='https://api.ocr.space/parse/image', api_key=api_key)
        try:
            filename = file

            result = api.ocr_file(open(filename, 'rb')).splitlines()

            return result[0] if result != [] else ''

        except Exception as e:
            logger.warning(e, exc_info=True)
            raise Exception(
                "There is something wrong with the api please check log for farther understanding")

    @staticmethod
    def license_validator(license: str) -> str:
        """:return: ALLOWED/NOT_ALLOWED/NOT_VALID to enter the parking lot"""

        logger.info(f'Function is_allowed is running with {license = }')

        enum = ['ALLOWED', 'NOT_ALLOWED', 'NOT_VALID']
        state = enum[0]

        try:
            # Check if there is any (non-digit || non-letter) in license charecters
            if re.sub(r'[a-zA-Z0-9]', '', license):
                state = enum[2]
                return state

            # Check if last charecter in license is 6 or G
            if license[-1] in ('6', 'G'):
                state = enum[1]
                db_insert(license, state)
                return state

            # Check rather there is ('L' || 'M') in license charecters
            if 'L' in license or 'M' in license:
                state = enum[1]
                db_insert(license, state)
                return state

            # Check if license charecters are all digits
            if False not in [*map(str.isdigit, license)]:
                state = enum[1]
                db_insert(license, state)
                return state

        except Exception as err:
            logger.warning(
                f'License is an empty string! \n{str(err)}', exc_info=True)
            state = enum[2]
            return state

        finally:
            logger.info(
                f'Function is_allowed done checking {license = } with status: {state}')

        db_insert(license, state)
        return state
