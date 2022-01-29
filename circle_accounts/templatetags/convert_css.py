from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import markdown
from markdown.extensions import Extension

register = template.Library()

@register.filter
def markdown_to_html(text):
    """マークダウンをhtmlに変換する。"""
    html = markdown.markdown(text, extensions=settings.MARKDOWN_EXTENSIONS)
    return mark_safe(html)



class EscapeHtml(Extension):

    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


@register.filter
def markdown_to_html_with_escape(text):
    """マークダウンをhtmlに変換する。
    生のHTMLやCSS、JavaScript等のコードをエスケープした上で、マークダウンをHTMLに変換します。
    公開しているコメント欄等には、こちらを使ってください。
    """
    extensions = settings.MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown.markdown(text, extensions=extensions)
    return mark_safe(html)