# -*- coding: utf-8 -*-
#
# Copyright © 2014 Max Arnold.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function, unicode_literals
from urllib import quote_plus

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

TWEETABLE_RE = r'\[tweetable\](?P<quote>[^\[]+)\[/tweetable\](?:\((?P<url>[^\)]+)\))?'

NETWORKS = ('google', 'facebook', 'twitter', 'vkontakte',)

SNIPPET = '''<blockquote class="tweetable">
<p>{quote}</p>
<p class="tweetable-buttons">{buttons}</p>
</blockquote>'''

# TODO: find a way to get current page url if not specified
# TODO: button classes
# TODO: button text localization

GOOGLE = ('<a href="javascript:void(0)" '
          'title="Click to share on Google+" '
          'class="tweetable-button g-interactivepost" '
          'data-clientid="{gcid}" '
          'data-cookiepolicy="single_host_origin" '
          'data-contenturl="{url}" '
          'data-calltoactionurl="{url}" '
          'data-prefilltext="{headline}">'
          '<span class="{google_class}"></span></a>')

def create_google_button(url, headline, config):
    return GOOGLE.format(url=url,
                         headline=headline,
                         gcid=config['gcid'],
                         google_class=config['google_class'])


FACEBOOK = ('<a class="tweetable-button" '
            'title="Copy the text, then click to share on Facebook" '
            'href="https://www.facebook.com/sharer/sharer.php?u={url}" '
            'target="_blank">'
            '<span class="{facebook_class}"></span></a>')

def create_facebook_button(url, headline, config):
    return FACEBOOK.format(url=quote_plus(url),
                           headline=quote_plus(headline.encode('utf-8')),
                           facebook_class=config['facebook_class'])


# TODO: optional via
TWITTER = ('<a class="tweetable-button" '
           'title="Click to share on Twitter" '
           'href="https://twitter.com/share?text={headline}&url={url}" '
           'target="_blank">'
           '<span class="{twitter_class}"></span></a>')

def create_twitter_button(url, headline, config):
    # TODO: validate length
    # short_url_length_https: 23, short_url_length: 22, total_length: 140
    return TWITTER.format(url=quote_plus(url),
                          headline=quote_plus(headline.encode('utf-8')),
                          twitter_class=config['twitter_class'])


VKONTAKTE = ('<a class="tweetable-button" '
             'title="Click to share on VKontakte" '
             'href="https://vk.com/share.php?url={url}&title={headline}" '
             'target="_blank">'
             '<span class="{vkontakte_class}"></span></a>')

def create_vkontakte_button(url, headline, config):
    return VKONTAKTE.format(url=quote_plus(url),
                            headline=quote_plus(headline.encode('utf-8')),
                            vkontakte_class=config['vkontakte_class'])


BUTTONS = {
    'google': create_google_button,
    'facebook': create_facebook_button,
    'twitter': create_twitter_button,
    'vkontakte': create_vkontakte_button,
}

def create_buttons(url, headline, config):
    buttons = [BUTTONS[n](url, headline, config) for n in config['networks']]
    return '\n'.join(buttons)


class TweetablePattern(Pattern):
    """InlinePattern for tweetable quotes"""
    def __init__(self, pattern, config, markdown_instance=None):
        super(TweetablePattern, self).__init__(pattern, markdown_instance=markdown_instance)
        self.config = config

    def handleMatch(self, m):
        quote = m.group('quote').strip()
        url = m.group('url')
        url = '' if url is None else url.strip()
        buttons = create_buttons(url, quote, self.config)
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
            'twitter_class': ['fa fa-twitter-square', 'Twitter button CSS class.'],
            'vkontakte_class': ['fa fa-vk', 'VKontakte button CSS class.'],
        }

        # Validate network list
        networks = tuple(filter(None, configs.pop('networks', '').split(';')))
        diff = set(networks).difference(set(NETWORKS))
        if diff:
            raise ValueError('Unsupported social network(s): {}'.format(', '.join(list(diff))))

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
