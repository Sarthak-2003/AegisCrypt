from datetime import datetime

def log_event(action):
    with open("security_log.txt", "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} -> {action}\n")
