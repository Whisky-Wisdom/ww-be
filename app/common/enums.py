from enum import Enum



class WhiskyCategory(str, Enum):
    BOURBON = "bourbon"
    SINGLE_MALT = "single_malt"
    BLENDED = "blended"