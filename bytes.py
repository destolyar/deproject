def to_bytes(message):
    if isinstance(message, str):
        msg = message.encode()
        return msg
    else:
        return message
