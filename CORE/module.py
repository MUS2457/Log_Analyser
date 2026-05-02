
class LogEntry:
    def __init__(self, timestamp, level, message, raw):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.raw = raw

    def __str__(self):   # print object as readable data, not memory position
        return f"[{self.timestamp}] {self.level}: {self.message}"

    @classmethod
    def from_dict(cls, log_info):
        return cls(
            log_info['timestamp'],
            log_info['level'],
            log_info['message'],
            log_info['raw']
        )





