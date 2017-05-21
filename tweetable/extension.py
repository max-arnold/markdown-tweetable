# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import re

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

TWEETABLE_RE = r'''
\[tweetable
  (?:\s+
    (?:
        alt=["'](?P<alt>[^"']+)["']
      |
        url=["'](?P<url>[^"']+)["']
      |
        hashtags=["'](?P<hashtags>[^"']+)["']
    )
  \s*)*
\]
  (?P<quote>[^\[]+)
\[/tweetable\]
'''

HASHTAGS_RE = re.compile(r'^(?:(#\w+)(?:\s+(#\w+))*)?', re.UNICODE)

# TODO: email
NETWORKS = ('twitter', 'google', 'facebook', 'linkedin', 'vkontakte',)

SNIPPET = '''<blockquote class="tweetable">
<p>{quote}</p>
<p class="tweetable-buttons">{buttons}</p>
</blockquote>'''

# TODO: find a way to get current page url if not specified
# TODO: button text localization

ICON_GOOGLE = (
    '<svg role="img" class="tweetable-svg-icon" viewBox="0 0 512 512" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<rect fill="#dd4f43" height="512" rx="15%" width="512"/>'
    '<path d="m56 257a126 126 0 0 1 212-96l-33 33c-21-13-49-24-75-14a80 '
    '80 0 1 0 54 151c21-8 35-28 41-48l-72-1v-44h122c1 36-3 74-27 102a127 '
    '127 0 0 1 -222-83zm327-56h36l1 37h36v37h-36l-1 36h-36v-36h-37v-37h37z" '
    'fill="#fff"/>'
    '</svg>'
)

SNIPPET_GOOGLE = (
    '<a href="javascript:void(0)" '
    'title="Click to share on Google+" '
    'class="tweetable-button g-interactivepost" '
    'data-clientid="{gcid}" '
    'data-cookiepolicy="single_host_origin" '
    'data-contenturl="{url}" '
    'data-calltoactionurl="{url}" '
    'data-prefilltext="{quote}{hashtags}">'
    '{icon_google}</a>'
)

def create_google_button(url, quote, hashtags, config):
    return config['snippet_google'].format(
        url=url,
        urlq=quote_plus(url),
        quote=quote,
        hashtags=format_hashtags(hashtags),
        gcid=config['gcid'],
        icon_google=config['icon_google']
)

ICON_FACEBOOK = (
    '<svg role="img" class="tweetable-svg-icon" viewBox="0 0 512 512" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<rect fill="#3b5998" height="512" rx="15%" width="512"/>'
    '<path d="m287 456v-299c0-21 6-35 35-35h38v-63c-7-1-29-3-55-3-54 '
    '0-91 33-91 94v306m143-254h-205v72h196" fill="#fff"/>'
    '</svg>'
)

SNIPPET_FACEBOOK = (
    '<a class="tweetable-button" '
    'title="Copy the text, then click to share on Facebook" '
    'href="https://www.facebook.com/sharer/sharer.php?u={urlq}" '
    'target="_blank">'
    '{icon_facebook}</a>'
)

def create_facebook_button(url, quote, hashtags, config):
    return config['snippet_facebook'].format(
        url=url,
        urlq=quote_plus(url),
        quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
        icon_facebook=config['icon_facebook']
    )


ICON_LINKEDIN = (
    '<svg role="img" class="tweetable-svg-icon" viewBox="0 0 512 512" '
    'xmlns="http://www.w3.org/2000/svg" fill="#fff">'
    '<rect width="512" height="512" rx="15%" fill="#0077b5"/>'
    '<circle cx="104" cy="104" r="48"/>'
    '<path d="m237 178v259m-133-259v259" stroke="#fff" stroke-width="86"/>'
    '<path d="m279 293c0-26 18-53 48-53 31 0 43 24 43 '
    '59v138h86v-148c0-80-42-116-99-116-45 0-67 25-78 42"/>'
    '</svg>'
)

SNIPPET_LINKEDIN = (
    '<a class="tweetable-button" '
    'title="Click to share on LinkedIn" '
    'href="http://www.linkedin.com/shareArticle?mini=true&url={urlq}&title={quote}" '
    'target="_blank">'
    '{icon_linkedin}</a>'
)

def create_linkedin_button(url, quote, hashtags, config):
    return config['snippet_linkedin'].format(
        url=url,
        urlq=quote_plus(url),
        quote=quote_plus(quote.encode('utf-8')),
        icon_linkedin=config['icon_linkedin']
    )


ICON_TWITTER = (
    '<svg role="img" class="tweetable-svg-icon" viewBox="0 0 512 512" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<rect fill="#1da1f3" height="512" rx="15%" width="512"/>'
    '<path d="m456 133c-14 7-31 11-47 13 17-10 30-27 37-46-15 10-34 '
    '16-52 20-61-62-157-7-141 75-68-3-129-35-169-85-22 37-11 86 26 '
    '109-13 0-26-4-37-9 0 39 28 72 65 80-12 3-25 4-37 2 10 33 41 57 '
    '77 57-42 30-77 38-122 34 170 111 378-32 359-208 16-11 30-25 41-42z" '
    'fill="#fff"/>'
    '</svg>'
)

# TODO: optional via
SNIPPET_TWITTER = (
    '<a class="tweetable-button" '
    'title="Click to share on Twitter" '
    'href="https://twitter.com/intent/tweet?text={quote}&url={urlq}&hashtags={hashtags}" '
    'target="_blank">'
    '{icon_twitter}</a>'
)

def create_twitter_button(url, quote, hashtags, config):
    # TODO: validate length
    # short_url_length_https: 23, short_url_length: 22, total_length: 140
    return config['snippet_twitter'].format(
        url=url,
        urlq=quote_plus(url),
        quote=quote_plus(quote.encode('utf-8')),
        hashtags=format_hashtags(hashtags, separator=',', strip_hash=True),
        icon_twitter=config['icon_twitter']
    )


ICON_VKONTAKTE = (
    '<svg role="img" class="tweetable-svg-icon" viewBox="0 0 512 512" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<rect width="512" height="512" rx="15%" fill="#4c75a3"/>'
    '<path d="m275 369c6-1 15-3 15-15 0 0-1-32 14-37 15-4 34 31 54 45 '
    '15 10 26 8 26 8l54-1s28-2 15-24c-1-2-9-16-41-45-33-31-28-26 12-80 '
    '24-33 35-53 31-61-4-7-21-6-21-6h-60c-6 0-10 1-13 7 0 0-9 26-22 '
    '47-27 46-37 48-42 45-10-6-8-26-8-40 0-47 7-64-14-68-6-1-11-2-27-2-21 '
    '0-40 0-50 5-7 4-12 11-9 12 4 1 13 2 18 8 6 9 6 27 6 27s4 52-8 59c-8 '
    '4-19-5-43-46-12-21-22-45-22-45-3-7-6-8-13-10h-58c-7 0-16 1-12 14 0 '
    '0 45 105 96 158 46 48 99 45 99 45z" fill="#fff"/>'
    '</svg>'
)

# TODO: optional source
SNIPPET_VKONTAKTE = (
    '<a class="tweetable-button" '
    'title="Click to share on VKontakte" '
    'href="https://vk.com/share.php?url={urlq}&title={quote}" '
    'target="_blank">'
    '{icon_vkontakte}</a>'
)

def create_vkontakte_button(url, quote, hashtags, config):
    return config['snippet_vkontakte'].format(
        url=url,
        urlq=quote_plus(url),
        quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
        icon_vkontakte=config['icon_vkontakte']
    )


BUTTONS = {
    'google': create_google_button,
    'facebook': create_facebook_button,
    'linkedin': create_linkedin_button,
    'twitter': create_twitter_button,
    'vkontakte': create_vkontakte_button,
}

def create_buttons(url, quote, hashtags, config):
    buttons = [BUTTONS[n](url, quote, hashtags, config) for n in config['networks']]
    return '\n'.join(buttons)


def format_hashtags(hashtags, separator=' ', strip_hash=False):
    return separator.join(hashtags).replace('#' if strip_hash else '', '')


class TweetablePattern(Pattern):
    """InlinePattern for tweetable quotes"""
    def __init__(self, pattern, config, markdown_instance=None):
        self.pattern = pattern
        self.compiled_re = re.compile("^(.*?)%s(.*?)$" % pattern, re.DOTALL | re.UNICODE | re.VERBOSE)

        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False
        if markdown_instance:
            self.markdown = markdown_instance

        self.config = config

    def handleMatch(self, m):
        quote, alt, url, hashtags = ['' if m.group(a) is None else m.group(a).strip() for a in ('quote', 'alt', 'url', 'hashtags')]
        alt_quote = alt or quote
        hashtags = [h for h in re.match(HASHTAGS_RE, hashtags).groups() if h is not None]
        if not url.startswith('http'):
            raise ValueError('Please specify url for tweetable quote.')
        buttons = create_buttons(url, alt_quote, hashtags, self.config)
        snippet = self.config['snippet'].format(quote=quote, buttons=buttons)
        placeholder = self.markdown.htmlStash.store(snippet)
        return placeholder


class TweetableExtension(Extension):
    def __init__(self, *args, **kwargs):
        # set extension defaults
        self.config = {
            'networks': [NETWORKS, 'Social networks for sharing.'],
            'snippet': [SNIPPET, 'HTML snippet.'],

            'snippet_facebook': [SNIPPET_FACEBOOK, 'Facebook HTML snippet.'],
            'icon_facebook': [ICON_FACEBOOK, 'Facebook SVG icon.'],

            'snippet_google': [SNIPPET_GOOGLE, 'Google+ HTML snippet.'],
            'icon_google': [ICON_GOOGLE, 'Google+ SVG icon.'],
            'gcid': ['xxxxx.apps.googleusercontent.com', 'Google Client ID.'],

            'snippet_linkedin': [SNIPPET_LINKEDIN, 'LinkedIn HTML snippet.'],
            'icon_linkedin': [ICON_LINKEDIN, 'LinkedIn SVG icon.'],

            'snippet_twitter': [SNIPPET_TWITTER, 'Twitter HTML snippet.'],
            'icon_twitter': [ICON_TWITTER, 'Twitter SVG icon.'],

            'snippet_vkontakte': [SNIPPET_VKONTAKTE, 'VKontakte HTML snippet.'],
            'icon_vkontakte': [ICON_VKONTAKTE, 'VKontakte SVG icon.'],
        }

        # Accept not only list/tuple but also a string, with values separated by semicolon
        networks = kwargs.pop('networks', '')
        if not isinstance(networks, (list, tuple)):
            networks = tuple(filter(None, networks.split(';')))

        # Validate network list
        diff = set(networks).difference(set(NETWORKS))
        if diff:
            raise ValueError('Unsupported social network(s): {}'.format(', '.join(list(diff))))

        # TODO: validate gcid if google is enabled

        networks = networks or NETWORKS
        self.setConfig('networks', networks)

        self.setConfigs(kwargs)

    def extendMarkdown(self, md, md_globals):
        tweetable_md_pattern = TweetablePattern(TWEETABLE_RE, self.getConfigs(), markdown_instance=md)
        md.inlinePatterns.add('tweetable', tweetable_md_pattern, '<link')
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    return TweetableExtension(*args, **kwargs)
