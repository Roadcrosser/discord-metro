def fancify(message):
    border = "█" * 10
    msg_split = message.split("\n")
    rejoined = "\n".join([(" " * 3) + m for m in msg_split])

    return f"{border}\n{rejoined}\n{border}"
