def edit_text(text):
    if len(text) < 2000:
        return text
    else:
        return f'{text[:1997]}...'