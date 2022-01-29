from django import template

register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムフィルタとして登録する
@register.filter
def limit(contents):
    if len(contents)>50:
        contents=contents[:50]
    return contents
