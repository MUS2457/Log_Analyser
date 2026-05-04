def most_common_word(counter):
    if counter:
        return max(counter, key=counter.get)

    return None

def sort_words_by_frequency(counter):
    if counter:
        return sorted(counter.items(), key=lambda pair: pair[1], reverse=True)

    return []

def top_n_words(sorted_frequency, limit):
    if sorted_frequency:
        return sorted_frequency[:limit]
    return []

def most_common_message(message_counter):
    return most_common_word(message_counter)

def sort_messages_by_frequency(message_counter):
    return sort_words_by_frequency(message_counter)

def top_n_messages(sorted_messages_frequency, limit):
    return top_n_words(sorted_messages_frequency, limit)

