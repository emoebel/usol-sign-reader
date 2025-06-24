from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional, List
import enum
import re

def to_camel(string: str) -> str:
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), string)

class CamelModel(BaseModel):
    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True
    }

# Enums
class TafelOutputFormatEnum(enum.Enum):
    SVGEmbedFonts = 0

class TafelOutputUnitEnum(enum.Enum):
    Millimeter = 0
    Pixel = 0 # added by eml

class TafelTypeEnum(enum.Enum):
    ZielwegweiserMitZielUndZeitAngabe = 2

class LvArtsEnum(enum.Enum):
    Wandern = 1

class SkinTypeEnum(enum.Enum):
    VssNorm = 1

class SeiteTypeEnum(enum.Enum):
    OneSide = 1

class TextScalingModeEnum(enum.Enum):
    Scaled75 = 1

class AusrichtungBeschriftungTypeEnum(enum.Enum):
    Right = 1
    Left = 2

class SymbolsEnum(enum.Enum):
    None_ = 0
    Bahnhof = 1
    Bushof = 2
    Aussichtspunkt = 30
    Restaurant = 47

class TafelSpitzeTypeEnum(enum.Enum):
    Wanderweg = 1

# Models
class BaseDto(CamelModel):
    id: Optional[UUID] = None

class StandortfeldDto(BaseDto):
    ort_zeile1: str
    ort_zeile2: str
    text_scaling_mode: TextScalingModeEnum
    hoehe: int

class TafelEintragBaseModelDto(BaseDto):
    name: Optional[str] = None
    name_zusatz: Optional[str] = None
    zeile: Optional[int] = None
    distance: Optional[int] = None

class GelbTafelEintragDto(TafelEintragBaseModelDto):
    text_scaling_mode: Optional[TextScalingModeEnum] = None
    zeit_scaling_mode: Optional[int] = None
    zeit: Optional[int] = None
    symbol1: Optional[SymbolsEnum] = None
    symbol2: Optional[SymbolsEnum] = None
    symbol3: Optional[SymbolsEnum] = None
    spitze_type: TafelSpitzeTypeEnum
    special_hinweis: Optional[str] = None
    has_special_hinweis: Optional[bool] = False
    has_separator: Optional[bool] = False
    schwierigkeitsgrad: Optional[str] = None

class TafelTeilBaseModelDto(BaseDto):
    system_winkel: int
    montage_winkel: int
    ausrichtung_beschriftung: AusrichtungBeschriftungTypeEnum
    order: int

class GelbTafelTeilDto(TafelTeilBaseModelDto):
    routen_feld1: Optional[str] = None
    routen_feld2: Optional[str] = None
    routen_feld3: Optional[str] = None
    spitze_type: TafelSpitzeTypeEnum
    anzahl_zeilen: Optional[int] = None
    entries: List[GelbTafelEintragDto]
    zubringer_symbol1: Optional[SymbolsEnum] = None
    zubringer_symbol2: Optional[SymbolsEnum] = None
    zubringer_text: Optional[str] = None
    zubringer_text_scaling_mode: Optional[str] = None

class TafelBaseModelDto(BaseDto):
    nummer: int
    old_nummer: Optional[str] = None
    has_standort_feld: bool
    standort_feld: Optional[StandortfeldDto] = None
    tafel_type: TafelTypeEnum
    lv_arts: LvArtsEnum
    skin: Optional[SkinTypeEnum] = None
    seite: SeiteTypeEnum
    display_placeholder: Optional[bool] = None

class GelbTafelDto(TafelBaseModelDto):
    is_doppelwegweiser: bool
    tafel_teile: List[GelbTafelTeilDto]

class TafelMetaInformationDto(BaseDto):
    output_format: Optional[TafelOutputFormatEnum] = None
    output_unit: Optional[TafelOutputUnitEnum] = None
    fixed_width: Optional[float] = None
    fixed_height: Optional[float] = None
    scaling_factor: Optional[float] = None
    dpi: Optional[float] = None
    mounting_area_visible: Optional[bool] = None
    info_or_warning_symbol_visible: Optional[bool] = None
    ignore_seite_property: Optional[bool] = None
    mounting_holes_visible: Optional[bool] = None
    mounting_separation_line_visible: Optional[bool] = None
    tafel_border_visible: Optional[bool] = None
    tafel_color_visible: Optional[bool] = None
    tafel_spitze_visible: Optional[bool] = None
    standort_nummer_visible: Optional[bool] = None
    doppel_spitz_center_vertically: Optional[bool] = None
    symbols_type: Optional[str] = None
    time_format: Optional[str] = None
    mandant_id: Optional[UUID] = None
    mandant_name: Optional[str] = None
    standort_nummer: Optional[str] = None
    standort_nummer_vertical: Optional[bool] = None
    config_type: Optional[int] = None
    custom_color: Optional[str] = None
    disable_time_rounding: Optional[bool] = None
    disable_distance_rounding: Optional[bool] = None
    gelb_tafel_list: Optional[List[GelbTafelDto]] = None
    rot_tafel_list: Optional[List] = None