
import math
from datetime import datetime, time


def log_round(number):
    if number != 0:
      magnitude = math.floor(math.log10(abs(number))) + 1
    else:
      return 0
    if magnitude > 3:
      return round(number, 0)
    return round(number, -magnitude + 3)

def argmax(iterable):
  return max(enumerate(iterable), key=lambda x: x[1])[0]



def today_ts():
    midnight = datetime.combine(datetime.now().date(), time.min)
    timestamp_midnight = int(midnight.timestamp())
    return timestamp_midnight
  
  
  