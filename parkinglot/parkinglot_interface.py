from .db import PostDB
from .ocr_validator import OcrValidator


class ParkingLot:
    user: str
    password: str
    database: str
    table: str

    def __init__(
        self,
        user="postgres",
        password="password",
        database="parkinglot",
        table="entrances",
    ) -> None:
        db = PostDB(user=user, password=password)
        db.create_database(database=database)
        db.switch_connection(user=user, password=password, database=database)
        db.create_table(table=table)

    @staticmethod
    def check(img: str) -> str:
        license_ = OcrValidator.ocr(img)
        return OcrValidator.license_validator(license_)
