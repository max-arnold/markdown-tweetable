# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from urllib import quote_plus
import re

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

SNIPPET_GOOGLE = ('<a href="javascript:void(0)" '
                  'title="Click to share on Google+" '
                  'class="tweetable-button g-interactivepost" '
                  'data-clientid="{gcid}" '
                  'data-cookiepolicy="single_host_origin" '
                  'data-contenturl="{url}" '
                  'data-calltoactionurl="{url}" '
                  'data-prefilltext="{quote}{hashtags}">'
                  '<span class="{css_google}"></span></a>')

def create_google_button(url, quote, hashtags, config):
    return config['snippet_google'].format(url=url,
                                    urlq=quote_plus(url),
                                    quote=quote,
                                    hashtags=format_hashtags(hashtags),
                                    gcid=config['gcid'],
                                    css_google=config['css_google'])


SNIPPET_FACEBOOK = ('<a class="tweetable-button" '
                    'title="Copy the text, then click to share on Facebook" '
                    'href="https://www.facebook.com/sharer/sharer.php?u={urlq}" '
                    'target="_blank">'
                    '<span class="{css_facebook}"></span></a>')

def create_facebook_button(url, quote, hashtags, config):
    return config['snippet_facebook'].format(url=url,
                                      urlq=quote_plus(url),
                                      quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
                                      css_facebook=config['css_facebook'])


SNIPPET_LINKEDIN = ('<a class="tweetable-button" '
                    'title="Click to share on LinkedIn" '
                    'href="http://www.linkedin.com/shareArticle?mini=true&url={urlq}&title={quote}" '
                    'target="_blank">'
                    '<span class="{css_linkedin}"></span></a>')

def create_linkedin_button(url, quote, hashtags, config):
    return config['snippet_linkedin'].format(url=url,
                                      urlq=quote_plus(url),
                                      quote=quote_plus(quote.encode('utf-8')),
                                      css_linkedin=config['css_linkedin'])


# TODO: optional via
SNIPPET_TWITTER = ('<a class="tweetable-button" '
                   'title="Click to share on Twitter" '
                   'href="https://twitter.com/share?text={quote}&url={urlq}" '
                   'target="_blank">'
                   '<span class="{css_twitter}"></span></a>')

def create_twitter_button(url, quote, hashtags, config):
    # TODO: validate length
    # short_url_length_https: 23, short_url_length: 22, total_length: 140
    return config['snippet_twitter'].format(url=url,
                                     urlq=quote_plus(url),
                                     quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
                                     css_twitter=config['css_twitter'])


# TODO: optional source
SNIPPET_VKONTAKTE = ('<a class="tweetable-button" '
                     'title="Click to share on VKontakte" '
                     'href="https://vk.com/share.php?url={urlq}&title={quote}" '
                     'target="_blank">'
                     '<span class="{css_vkontakte}"></span></a>')

def create_vkontakte_button(url, quote, hashtags, config):
    return config['snippet_vkontakte'].format(url=url,
                                       urlq=quote_plus(url),
                                       quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
                                       css_vkontakte=config['css_vkontakte'])


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


def format_hashtags(hashtags, space=True):
    return (' ' if space and hashtags else '') + ' '.join(hashtags)


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
    def __init__(self, configs=()):
        configs = dict(configs) or {}

        # set extension defaults
        self.config = {
            'networks': [NETWORKS, 'Social networks for sharing.'],
            'snippet': [SNIPPET, 'HTML snippet.'],

            'snippet_facebook': [SNIPPET_FACEBOOK, 'Facebook HTML snippet.'],
            'css_facebook': ['fa fa-facebook-square', 'Facebook button CSS class.'],

            'snippet_google': [SNIPPET_GOOGLE, 'Google+ HTML snippet.'],
            'css_google': ['fa fa-google-plus-square', 'Google+ button CSS class.'],
            'gcid': ['xxxxx.apps.googleusercontent.com', 'Google Client ID.'],

            'snippet_linkedin': [SNIPPET_LINKEDIN, 'LinkedIn HTML snippet.'],
            'css_linkedin': ['fa fa-linkedin-square', 'LinkedIn button CSS class.'],

            'snippet_twitter': [SNIPPET_TWITTER, 'Twitter HTML snippet.'],
            'css_twitter': ['fa fa-twitter-square', 'Twitter button CSS class.'],

            'snippet_vkontakte': [SNIPPET_VKONTAKTE, 'VKontakte HTML snippet.'],
            'css_vkontakte': ['fa fa-vk', 'VKontakte button CSS class.'],
        }

        # Accept not only list/tuple but also a string, with values separated by semicolon
        networks = configs.pop('networks', '')
        if not isinstance(networks, (list, tuple)):
            networks = tuple(filter(None, networks.split(';')))

        # Validate network list
        diff = set(networks).difference(set(NETWORKS))
        if diff:
            raise ValueError('Unsupported social network(s): {}'.format(', '.join(list(diff))))

        # TODO: validate gcid if google is enabled

        networks = networks or NETWORKS
        self.setConfig('networks', networks)

        # Override defaults with user settings
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        tweetable_md_pattern = TweetablePattern(TWEETABLE_RE, self.getConfigs(), markdown_instance=md)
        md.inlinePatterns.add('tweetable', tweetable_md_pattern, '<link')
        md.registerExtension(self)


def makeExtension(configs=None):
    return TweetableExtension(configs=configs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=(doctest.NORMALIZE_WHITESPACE +
                                 doctest.REPORT_NDIFF))
