def most_common(counter):
    if counter:
        return max(counter, key=counter.get)

    return None

def sort_by_frequency(counter):
    if counter:
        return sorted(counter.items(), key=lambda pair: pair[1], reverse=True)

    return []

def top_n_words(sorted_frequency, limit):
    if sorted_frequency:
        return sorted_frequency[:limit]
    return []
