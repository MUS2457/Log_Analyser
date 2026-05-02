
class LogAnalyser:
    def __init__(self, entries):
        self.entries = entries

    def count_by_level(self):
        counts = {}
        tl_entries = 0

        if not self.entries :
            return counts
        for entry in self.entries:

            if entry.level not in counts:
                 counts[entry.level] = 0

            counts[entry.level] += 1
            tl_entries += 1

        return counts , tl_entries

    def filter_by_level(self, level):
        results = []

        if not self.entries :
            return results

        for entry in self.entries:
            if entry.level == level:
                results.append(entry)

        return results

    def filter_by_keywords(self, keywords):
        results = []

        if not self.entries :
            return results

        for entry in self.entries:
            if keywords in entry.message:
                results.append(entry)

        return results

    def filter_by_date(self, date):
        results = []

        if not self.entries :
            return results

        for entry in self.entries:
            if entry.date == date:
                results.append(entry)

        return results

    def filter_by_date_range(self, start, end):
        results = []
        if not self.entries :
            return results

        for entry in self.entries:
            if start <= entry.date <= end:
                results.append(entry)

        return results
