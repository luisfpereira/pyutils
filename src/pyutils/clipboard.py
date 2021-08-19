import pyperclip


def copy_to_clipboard(text):
    pyperclip.copy(text)


def paste_clipboard():
    return pyperclip.paste()
