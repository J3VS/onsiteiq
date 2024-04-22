from datetime import datetime

import pytz

utc = pytz.UTC


def to_utc(dt: datetime) -> datetime:
    return utc.localize(dt)


def now():
    return to_utc(datetime.now())
