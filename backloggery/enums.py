from aenum import Enum, MultiValue

def cast[T](enum_type: type[T], val: None | int) -> str:
    if val is None:
        return ""
    else:
        return str(enum_type(val))

class GameEnum(Enum):
    _init_ = 'value full'
    _settings_ = MultiValue

    def __int__(self):
        return self.value

    def __str__(self):
        return self.full

class Status(GameEnum):
    UNPLAYED = 10, 'Unplayed'
    UNFINISHED = 20, 'Unfinished'
    BEATEN = 30, 'Beaten'
    COMPLETED = 40, 'Completed'
    ENDLESS = 60, 'Endless'
    NONE = 80, 'None'

class Priority(GameEnum):
    SHELVED = 10, 'Shelved'
    REPLAY = 20, 'Replay'
    LOW = 30, 'LOW'
    NORMAL = 40, 'Normal'
    HIGH = 50, 'HIGH'
    PAUSED = 60, 'Paused'
    ONGOING = 70, 'Ongoing'
    NOWPLAYING = 80, 'Now Playing'

class Own(GameEnum):
    NONE = 0, ''
    OWN = 1, 'Own'
    FORMERLY = 2, 'Formerly Owned'
    PLAYED = 3, 'Played It'
    OTHER = 4, 'Other'
    HOUSEHOLD = 5, 'Household'
    SUBSCRIPTION = 6, 'Subscription'
    WISHLIST = 7, 'Wishlist'

class PhysDigi(GameEnum):
    NONE = 0, ''
    DIGITAL = 1, 'Digital'
    PHYSICAL = 20, 'Physical'
    PHYSICAL_GAME = 21, 'Physical (Game Only)'
    PHYSICAL_INCOMPLETE = 22, 'Physical (Incomplete)'
    PHYSICAL_COMPLETE = 28, 'Physical (Complete In Box)'
    PHYSICAL_SEALED = 29, 'Physical (Sealed)'
    PHYSICAL_LICENSED = 30, 'Physical (Licensed Repro)'
    PHYSICAL_UNLICENSED = 31, 'Physical (Unlicensed Repro)'

class Region(GameEnum):
    NONE = 0, ''
    FREE = 1, 'Free'
    NA = 2, 'North America'
    JAPAN = 3, 'Japan'
    PAL = 4, 'PAL'
    CHINA = 5, 'China'
    KOREA = 6, 'Korea'
    BRAZIL = 7, 'Brazil'
    ASIA = 8, 'Asia'

class Rating(GameEnum):
    STARS_05 = 1, '0.5 Stars'
    STARS_10 = 2, '1.0 Star'
    STARS_15 = 3, '1.5 Stars'
    STARS_20 = 4, '2.0 Stars'
    STARS_25 = 5, '2.5 Stars'
    STARS_30 = 6, '3.0 Stars'
    STARS_35 = 7, '3.5 Stars'
    STARS_40 = 8, '4.0 Stars'
    STARS_45 = 9, '4.5 Stars'
    STARS_50 = 10, '5.0 Stars'

class Difficulty(GameEnum):
    NONE = 0, ''
    EASY = 10, 'Too Easy'
    RELAXING = 20, 'Relaxing'
    MODERATE = 30, 'Moderate'
    HURTS = 40, 'Hurts'
    HARD = 50, 'Too Hard'
    UNFAIR = 60, 'Unfair'