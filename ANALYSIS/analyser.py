import re


class LogAnalyser:
    def __init__(self, entries):
        self.entries = entries

    def count_by_level(self):
        counts = {}

        if not self.entries :
            return counts
        for entry in self.entries:

            if entry.level not in counts:
                 counts[entry.level] = 0

            counts[entry.level] += 1

        return counts

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

    def group_by_date(self):
        group_date = {}

        if not self.entries :
            return group_date

        for entry in self.entries:
            if entry.date not in group_date :
                group_date[entry.date] = []

            group_date[entry.date].append(entry)

        return group_date

    def common_words_across_logs(self):
        results = []

        if not self.entries:
            return results

        for entry in self.entries:
            results.append(entry.message)

        if results:

            words_set = [set(message.lower().split()) for message in results]
            # convert each message into a set of unique words
            common_words = set.intersection(*words_set)
            # * unpacks the list so intersection receives each set separately
            #  intersection() returns words that appear in every message

            return common_words

        return None

    def word_frequency(self):
        counter = {}

        if not self.entries:
            return []

        for entry in self.entries:
            words = entry.message.lower().split()
            for word in words:
                counter[word] = counter.get(word, 0) + 1

        return  counter

    def total_entries(self):
        if not self.entries :
            return 0
        return len(self.entries)

    def count_by_message(self):
        counter = {}
        if not self.entries:
            return counter

        for entry in self.entries:
            message = entry.message.lower()
            counter[message] = counter.get(message, 0) + 1

        return counter

    def unique_messages(self):
        if not self.entries :
            return set()

        return  set([entry.message.lower() for entry in self.entries])

    def messages_containing(self, keywords):
        results = []
        if not self.entries :
            return results

        for entry in self.entries:
            if keywords.lower() in entry.message.lower():
                results.append(entry)

        return results

    def messages_matching(self, pattern):
        results = []
        if not self.entries:
            return results

        regex = re.compile(pattern, re.IGNORECASE) # compile manually for fast search
                                                   # re.ignore means do not care if upper, lower... all possibilities
        for entry in self.entries:
            if regex.search(entry.message):  # if I did not compile manually python will do it every time while searching
                results.append(entry)

        return results









