# Tweetable quotes for Python-Markdown

Why this extension? A lot of blog posts have social sharing buttons at the top or bottom of the page. But there is a recent trend to embed shareable quotes right into the post body, and this approach noticeably increases content sharing. Some sites even allow you to select any part of a text and share it (see [medium.com](https://medium.com/life-learning/7-reasons-why-you-will-never-do-anything-amazing-with-your-life-2a1841f1335d) for example). The basic idea is that people prefer to quote a story rather than its headline. And you can have multiple shareable quotes in a single story!

With this extension you will be able to turn the text below

    [tweetable]
    When there is state there can be no freedom,
    but when there is freedom there will be no state.
    -- Vladimir Lenin
    [/tweetable](http://www.brainyquote.com/quotes/authors/v/vladimir_lenin.html)

into the following html markup

    <blockquote class="tweetable">
    <p>When there is state there can be no freedom,
    but when there is freedom there will be no state.
    -- Vladimir Lenin</p>
    <p class="tweetable-buttons">SOCIAL_SHARE_BUTTONS_CODE</p>
    </blockquote>

## Installation

    pip install git+git://github.com/max-arnold/markdown-tweetable.git


## Usage

Default share buttons are rendered using [Font Awesome](http://fontawesome.io). To use it you need to include the following CSS file before your `</head>` tag:

    <link href="//netdna.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">

There are also more advanced ways to use it, go read its [documentation](http://fontawesome.io/get-started/) if you are curious.

If you plan to use Google+ button, you need to include the following JavaScript just before your `</body>` tag:

    <script type="text/javascript">
      (function() {
        var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
        po.src = 'https://apis.google.com/js/client:plusone.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
      })();
    </script>

Also you need oAuth 2.0 client ID, as described in the [documentation](https://developers.google.com/+/web/share/interactive#adding_the_share_button_to_your_page). To inject it, [specify](http://pythonhosted.org/Markdown/reference.html#extensions) `gcid` configuration parameter when initializing class instance:

    MyExtension(configs={'gcid': ''xxxx.apps.googleusercontent.com'})

## Configuration

TODO

List of configuration parameters:

    'networks': [NETWORKS, 'Social networks for sharing.'],
    'snippet': [SNIPPET, 'HTML snippet.'],
    'gcid': ['xxxxx.apps.googleusercontent.com', 'Google Client ID.'],
    'facebook_class': ['fa fa-facebook-square', 'Facebook button CSS class.'],
    'google_class': ['fa fa-google-plus-square', 'Google+ button CSS class.'],
    'twitter_class': ['fa fa-twitter-square', 'Twitter button CSS class.'],
    'vkontakte_class': ['fa fa-vk', 'VKontakte button CSS class.'],

### Button docs:

* https://developers.facebook.com/docs/plugins/share-button/ http://stackoverflow.com/questions/20956229/has-facebook-sharer-php-changed-to-no-longer-accept-detailed-parameters
* https://developers.google.com/+/web/share/interactive
* https://dev.twitter.com/docs/tweet-button
* http://vk.com/dev/share_details

## Dependencies

* [Markdown 2.0+](http://pythonhosted.org/Markdown/)

## Copyright

Copyright 2014 [Max Arnold](http://ar0.me/), all rights reserved.

This software is released under the BSD License.
