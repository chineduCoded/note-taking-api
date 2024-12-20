from enum import Enum


class LanguageCode(str, Enum):
    AUTO = "auto"
    EN_US = "en-US"
    EN_GB = "en-GB"
    FR_FR = "fr-FR"
    ES_ES = "es-ES"
    DE_DE = "de-DE"
    ES = "es"
    FR = "fr"
    DE = "de"