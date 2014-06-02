Tweetable quotes for Python-Markdown
====================================

Why this extension? A lot of blog posts have social sharing buttons at the top or bottom of the page. But there is a recent trend to embed shareable quotes right into the post body, and this approach noticeably increases content sharing. Some sites even allow you to select any part of a text and share it (see [medium.com](https://medium.com/life-learning/7-reasons-why-you-will-never-do-anything-amazing-with-your-life-2a1841f1335d) for example). The basic idea is that people prefer to quote a story rather than its headline. And you can have multiple shareable quotes in a single story!

With this extension you will be able to turn the text below

    [tweetable]
    When there is state there can be no freedom,
    but when there is freedom there will be no state.
    -- Vladimir Lenin
    [/tweetable]

into the following html markup

    <blockquote class="tweetable">
    <p>When there is state there can be no freedom,
    but when there is freedom there will be no state.
    -- Vladimir Lenin</p>
    <footer>[Social share buttons code]</footer>
    </blockquote>


Installation
------------

    pip install git+git://github.com/max-arnold/markdown-tweetable.git

Usage
-----

Dependencies
------------

* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)

Copyright
---------

- 2014 [Max Arnold](http://ar0.me/)

All rights reserved.

This software is released under the BSD License.
