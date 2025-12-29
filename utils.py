def map_score(score, mapping):
    if score is None:
        return "-"
    try:
        score = int(score)
    except ValueError:
        return "-"
    for r, desc in mapping.items():
        if score in r:
            return desc
    return str(score)
