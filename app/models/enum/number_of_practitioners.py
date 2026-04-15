from enum import Enum


class NumberOfPractitioners(Enum):
    ONE_TO_FIVE = "1-5 Practitioners"
    SIX_TO_FIFTEEN = "6-15 Practitioners"
    SIXTEEN_TO_FIFTY = "16-50 Practitioners"
    FIFTY_ONE_TO_HUNDRED = "51-100 Practitioners"
    OVER_HUNDRED = "100+ Practitioners"