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

GOOGLE = ('<a href="javascript:void(0)" '
          'title="Click to share on Google+" '
          'class="tweetable-button g-interactivepost" '
          'data-clientid="{gcid}" '
          'data-cookiepolicy="single_host_origin" '
          'data-contenturl="{url}" '
          'data-calltoactionurl="{url}" '
          'data-prefilltext="{quote}{hashtags}">'
          '<span class="{google_class}"></span></a>')

def create_google_button(url, quote, hashtags, config):
    return GOOGLE.format(url=url,
                         quote=quote,
                         hashtags=format_hashtags(hashtags),
                         gcid=config['gcid'],
                         google_class=config['google_class'])


FACEBOOK = ('<a class="tweetable-button" '
            'title="Copy the text, then click to share on Facebook" '
            'href="https://www.facebook.com/sharer/sharer.php?u={url}" '
            'target="_blank">'
            '<span class="{facebook_class}"></span></a>')

def create_facebook_button(url, quote, hashtags, config):
    return FACEBOOK.format(url=quote_plus(url),
                           quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
                           facebook_class=config['facebook_class'])


LINKEDIN = ('<a class="tweetable-button" '
            'title="Click to share on LinkedIn" '
            'href="http://www.linkedin.com/shareArticle?mini=true&url={url}&title={quote}" '
            'target="_blank">'
            '<span class="{linkedin_class}"></span></a>')

def create_linkedin_button(url, quote, hashtags, config):
    return LINKEDIN.format(url=quote_plus(url),
                           quote=quote_plus(quote.encode('utf-8')),
                           linkedin_class=config['linkedin_class'])


# TODO: optional via
TWITTER = ('<a class="tweetable-button" '
           'title="Click to share on Twitter" '
           'href="https://twitter.com/share?text={quote}&url={url}" '
           'target="_blank">'
           '<span class="{twitter_class}"></span></a>')

def create_twitter_button(url, quote, hashtags, config):
    # TODO: validate length
    # short_url_length_https: 23, short_url_length: 22, total_length: 140
    return TWITTER.format(url=quote_plus(url),
                          quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
                          twitter_class=config['twitter_class'])


# TODO: optional source
VKONTAKTE = ('<a class="tweetable-button" '
             'title="Click to share on VKontakte" '
             'href="https://vk.com/share.php?url={url}&title={quote}" '
             'target="_blank">'
             '<span class="{vkontakte_class}"></span></a>')

def create_vkontakte_button(url, quote, hashtags, config):
    return VKONTAKTE.format(url=quote_plus(url),
                            quote=quote_plus((quote + format_hashtags(hashtags)).encode('utf-8')),
                            vkontakte_class=config['vkontakte_class'])


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
            'gcid': ['xxxxx.apps.googleusercontent.com', 'Google Client ID.'],
            'facebook_class': ['fa fa-facebook-square', 'Facebook button CSS class.'],
            'google_class': ['fa fa-google-plus-square', 'Google+ button CSS class.'],
            'linkedin_class': ['fa fa-linkedin-square', 'LinkedIn button CSS class.'],
            'twitter_class': ['fa fa-twitter-square', 'Twitter button CSS class.'],
            'vkontakte_class': ['fa fa-vk', 'VKontakte button CSS class.'],
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
