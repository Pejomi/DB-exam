def format_time(duration):
    seconds = int(duration)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d} hours"
    elif minutes > 0:
        return f"{minutes}:{seconds:02d} minutes"
    else:
        return f"{seconds} seconds"
