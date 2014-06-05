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

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

TWEETABLE_RE = r'\[tweetable\](?P<quote>.+)\[/tweetable\]'

NETWORKS = ('google', 'facebook', 'twitter', 'vkontakte',)

SNIPPET = '''<blockquote class="tweetable">
<p>{quote}</p>
<p class="tweetable-buttons">{buttons}</p>
</blockquote>'''

TWITTER = '<a class="" title="Twitter" href="http://twitter.com/home/?status=" target="_blank">'

FACEBOOK = '<a class="" title="Facebook" href="http://www.facebook.com/sharer.php?u=" target="_blank">'

VKONTAKTE = '<a class="" title="Vkontakte" href="http://vk.com/share.php?url=&title=" target="_blank">'

GOOGLE = '''<span class="g-interactivepost"
data-contenturl="https://plus.google.com/pages/"
data-clientid="xxxxx.apps.googleusercontent.com"
data-cookiepolicy="single_host_origin"
data-prefilltext="Engage your users today, create a Google+ page for your business."
data-calltoactionurl="http://plus.google.com/pages/create"
Tell your friends
</span>'''

# <script type="text/javascript">
#   (function() {
#    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
#    po.src = 'https://apis.google.com/js/client:plusone.js';
#    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
#  })();
# </script>

class TweetablePattern(Pattern):
    """InlinePattern for tweetable quotes"""
    def __init__(self, pattern, config, markdown_instance=None):
        super(TweetablePattern, self).__init__(pattern, markdown_instance=markdown_instance)
        self.config = config
        print(config)

    def handleMatch(self, m):
        quote = m.group('quote').strip()
        # TODO: validate length
        snippet = self.config['snippet'].format(quote=quote, buttons='')
        placeholder = self.markdown.htmlStash.store(snippet)
        return placeholder


class TweetableExtension(Extension):
    def __init__(self, configs=()):
        configs = dict(configs) or {}

        # set extension defaults
        self.config = {
            'networks': [NETWORKS, 'Social networks for sharing.'],
            'snippet': [SNIPPET, 'HTML snippet.']
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
        md.inlinePatterns.add('tweetable', tweetable_md_pattern, '_end')
        md.registerExtension(self)


def makeExtension(configs=None):
    return TweetableExtension(configs=configs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=(doctest.NORMALIZE_WHITESPACE +
                                 doctest.REPORT_NDIFF))
