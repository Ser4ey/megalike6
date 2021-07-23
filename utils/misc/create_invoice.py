from dataclasses import  dataclass
from typing import List
from data import config
from aiogram.types import LabeledPrice


@dataclass
class InvoiceOrder():
    title: str
    description: str
    start_parameter: str
    prices: List[LabeledPrice]
    provider_token: str = config.PROVIDER_TOKEN
    currency: str = 'RUB'
    provider_data: str = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    is_flexible: bool = False

    def generate_invoice(self):
        return self.__dict__