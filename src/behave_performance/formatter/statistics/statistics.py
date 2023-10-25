
SEP = '_'

class StatDataType():
    COUNT = 'COUNT'
    OTHER = 'OTHER'
    NANOS = 'NANOS'
    MILLIS = 'MILLIS'
    SECONDS = 'SECONDS'

class StatType:
    def __init__(self, key, fullname, shortname, abbrivation, data_type, is_floating_point):
        self.key = key
        self.fullname = fullname
        self.shortname = shortname
        self.abbrivation = abbrivation
        self.data_type = data_type
        self.is_floating_point = is_floating_point
    
    def get_default_value(self):
        if self.is_floating_point:
            return 0.0
        else:
            return 0



class StatTypes():
    AVERAGE = StatType('avg', 'Average', 'Avg', 'avg', StatDataType.SECONDS, True)
    MINIMUM = StatType('min', 'Minimum', 'Min', 'min', StatDataType.SECONDS, True)
    MAXIMUM = StatType('max', 'Maximum', 'Max', 'max', StatDataType.SECONDS, True)
    MEDIAN = StatType('med', 'Median', 'Med', 'med', StatDataType.SECONDS, True)
    COUNT = StatType('cnt', 'Count', 'Count', 'cnt', StatDataType.COUNT, False)
    PASSED = StatType('pass', 'Passed', 'Pass', 'pass', StatDataType.COUNT, False)
    FAILED = StatType('fail', 'Failed', 'Fail', 'fail', StatDataType.COUNT, False)
    ERRORED = StatType('error', 'Errored', 'Error', 'error', StatDataType.COUNT, False)
    PERCENTILE = StatType('prctl', 'Percentile', 'Prctl', 'prctl', StatDataType.SECONDS, True)
    PERCENTAGE = StatType('%', 'Percentage', 'Percent', '%', StatDataType.OTHER, True)
    STD_DEVIATION = StatType('stdev', 'Standard Deviation', 'StdDev', 'stdev', StatDataType.OTHER, True)
    CONCURRENCY = StatType('cncrnt', 'Concurrency', 'Concurrency', 'cncrnt', StatDataType.OTHER, True)



def get_default_stats(is_strict):
    stats = {
        StatTypes.COUNT.key: 0
    }
    if not is_strict:
        stats[StatTypes.PASSED.key] = 0
        stats[StatTypes.FAILED.key] = 0
    stats[StatTypes.AVERAGE.key] = 0
    stats[StatTypes.MAXIMUM.key] = None
    stats[StatTypes.MINIMUM.key] = None
    stats[StatTypes.CONCURRENCY.key] = 0
    return stats

def get_default_stat_types(is_strict):
    stat_types = {
        StatTypes.COUNT.key: StatTypes.COUNT
    }
    if not is_strict:
        stat_types[StatTypes.PASSED.key] = StatTypes.PASSED
        stat_types[StatTypes.FAILED.key] = StatTypes.FAILED
    stat_types[StatTypes.AVERAGE.key] = StatTypes.AVERAGE
    stat_types[StatTypes.MINIMUM.key] = StatTypes.MINIMUM
    stat_types[StatTypes.MAXIMUM.key] = StatTypes.MAXIMUM
    stat_types[StatTypes.CONCURRENCY.key] = StatTypes.CONCURRENCY
    return stat_types

def create_stat_type(key, fullname, shortname, abbrivation, data_type):
    return StatType(key, fullname, shortname, abbrivation, data_type, True)

def create_stat_type_with_prefix(prefix, stat):
    return StatType(
        f"{prefix}{SEP}{stat.key}",
        f"{prefix}{SEP}{stat.fullname}",
        f"{prefix}{SEP}{stat.shortname}",
        f"{prefix}{SEP}{stat.abbrivation}",
        stat.data_type,
        stat.is_floating_point
    )

def create_stat_type_with_postfix(stat, postfix):
    return StatType(
        f"{stat.key}{SEP}{postfix}",
        f"{stat.fullname}{SEP}{postfix}",
        f"{stat.shortname}{SEP}{postfix}",
        f"{stat.abbrivation}{SEP}{postfix}",
        stat.data_type,
        stat.is_floating_point
    )