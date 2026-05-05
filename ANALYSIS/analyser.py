import re
import analyser_helper

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

    def peak_log_hour(self):
        counter = {}

        if not self.entries :
            return counter

        for entry in self.entries:   # .hour I used it cause it s an object
            hour = entry.timestamp.hour             # this can be used too (t) if timestamp was not an object
            counter[hour] = counter.get(hour,0) + 1 # t = int(entry.timestamp.split(" ")[1].split(":")[0])
                                                    # split(x)  x is the point of cut
        return max(counter, key=counter.get)

    def summary_report(self, top_n=5):
        
        word_freq = self.word_frequency()
        sorted_words = analyser_helper.sort_words_by_frequency(word_freq)
        top_words = analyser_helper.top_n_words(sorted_words, top_n)
        most_common_w = analyser_helper.most_common_word(word_freq)
        msg_counter = self.count_by_message()
        sorted_messages = analyser_helper.sort_messages_by_frequency(msg_counter)
        top_msgs = analyser_helper.top_n_messages(sorted_messages, top_n)
        most_common_msg = analyser_helper.most_common_message(msg_counter)
        common_words = self.common_words_across_logs()
        common_words = list(common_words) if common_words else []
        grouped = self.group_by_date()
        logs_per_date = {str(date): len(entries) for date, entries in grouped.items()}

        return {
            # basic stats
            "total_entries": self.total_entries(),
            "count_by_level": self.count_by_level(),
            "peak_log_hour": self.peak_log_hour(),

            # word analysis
            "word_frequency": word_freq,
            "sorted_word_frequency": sorted_words,
            "top_words": top_words,
            "most_common_word": most_common_w,

            # message analysis
            "count_by_message": msg_counter,
            "sorted_messages_by_frequency": sorted_messages,
            "top_messages": top_msgs,
            "most_common_message": most_common_msg,

            # common words
            "common_words_across_logs": common_words,

            # date analysis
            "logs_per_date": logs_per_date,
            "group_by_date": {str(date): [e.message for e in entries] for date, entries in grouped.items()}
        }










