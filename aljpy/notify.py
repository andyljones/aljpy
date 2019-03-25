import os

def notify(title, text=''):
    os.system(f"""osascript -e 'display notification "{text}" with title "{title}"'""")