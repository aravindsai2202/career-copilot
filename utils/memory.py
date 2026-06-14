def add_message(
    history,
    role,
    content
):
    history.append(
        {
            "role": role,
            "content": content
        }
    )