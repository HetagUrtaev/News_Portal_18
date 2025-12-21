from django import template
import re

register = template.Library()

bad_words = [
    'плохие слова'
]

@register.filter
def censor(value):
    if not isinstance(value, str):
        return value

    def replace_word(match):
        word = match.group(0)
        if len(word) == 0:
            return word
        return word[0] + '*' * (len(word) - 1)

    pattern = r'\b(' + '|'.join(re.escape(word) for word in bad_words) + r')\b'
    result = re.sub(pattern, replace_word, value) #flags=re.IGNORECASE - слова, которые нужно цензурировать, начинаются с верхнего или нижнего регистра.
    return result