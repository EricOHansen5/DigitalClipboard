from enum import Enum

class LogTypeString(Enum):
    GEN = "-- GENERAL  --"
    WAR = "-- WARNING  --"
    ERR = "-- ERROR    --"
    CRIT ="-- CRITICAL --"