# Tweetable quotes for Python-Markdown

Why this extension? A lot of blog posts have social sharing buttons at the top or bottom of a page. But there is a recent trend to embed shareable quotes right into the post body, which noticeably increases content sharing. Some sites even allow you to select any part of text and share it (see [medium.com](https://medium.com/life-learning/7-reasons-why-you-will-never-do-anything-amazing-with-your-life-2a1841f1335d) for example). The basic idea is that people prefer to quote a story rather than its headline. And you can have multiple shareable quotes in a single story!

With this extension you will be able to turn the text below:

    [tweetable url="http://www.brainyquote.com/quotes/authors/v/vladimir_lenin.html"]
    When there is state there can be no freedom,
    but when there is freedom there will be no state.
    -- Vladimir Lenin
    [/tweetable]

into the following nice styled quote:

![Screenshot of the quote](/screenshot.png)

## Installation

    pip install markdown-tweetable

or:

    pip install git+git://github.com/max-arnold/markdown-tweetable.git


## Usage

Full syntax:

    [tweetable alt="When there is state there can be no freedom,
                    but when there is freedom there will be no state"
               url="http://en.wikipedia.org/wiki/Vladimir_Lenin"
               hashtags="#lenin"]
    When there is state there can be no freedom, but when there is freedom there will be no state.
    -- Vladimir Lenin
    [/tweetable]

And you definitely want to add some style. Below is an example:

    blockquote.tweetable {
        border-top: 1px solid #CCC;
        border-bottom: 1px solid #CCC;
        border-left: none;
        border-right: none;
        position: relative;
    }

    blockquote.tweetable::before {
        content: '“';
        position: absolute;
        top: 0;
        left: 0;
        font-size: 4em;
        font-family: "inherit";
        font-weight: bold;
        color: #888;
    }

    blockquote.tweetable p {
        margin: 0 0 0.5em 1.5em;
        font-style: italic;
    }

    .tweetable-svg-icon {
        /* fill: #db3535; */
        width: 1em;
    }

## List of configuration parameters

### Social buttons

List of social networks for sharing. By default contains all supported networks:

    networks=('twitter', 'facebook', 'linkedin', 'vkontakte',)

You can also specify it as a string (useful if you configured this markdown extension using module path with parameters):

    networks='twitter;facebook;linkedin;vkontakte'

### HTML snippet

By default it looks like this:

    snippet='''<blockquote class="tweetable">
        <p>{quote}</p>
        <p class="tweetable-buttons">{buttons}</p>
    </blockquote>'''

### Social button snippets

    snippet_facebook='''<a class="tweetable-button"
        title="Copy the text, then click to share on Facebook"
        href="https://www.facebook.com/sharer/sharer.php?u={urlq}"
        target="_blank">
        {icon_facebook}</a>'''

    snippet_linkedin='''<a class="tweetable-button"
        title="Click to share on LinkedIn"
        href="http://www.linkedin.com/shareArticle?mini=true&url={urlq}&title={quote}"
        target="_blank">
        {icon_linkedin}</a>'''

    snippet_twitter='''<a class="tweetable-button"
        title="Click to share on Twitter"
        href="https://twitter.com/intent/tweet?text={quote}&url={urlq}&hashtags={hashtags}"
        target="_blank">
        {icon_twitter}</a>'''

    snippet_vkontakte='''<a class="tweetable-button"
        title="Click to share on VKontakte"
        href="https://vk.com/share.php?url={urlq}&title={quote}"
        target="_blank">
        {icon_vkontakte}</a>'''

### Social icons

    icon_facebook='''
        <svg role="img" class="tweetable-svg-icon" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
        <rect fill="#3b5998" height="512" rx="15%" width="512"/>
        <path d="m287 456v-299c0-21 6-35 35-35h38v-63c-7-1-29-3-55-3-54 0-91 33-91 94v306m143-254h-205v72h196" fill="#fff"/>
        </svg>'''

    icon_linkedin='''
        ...
    '''

    icon_twitter='''
        ...
    '''

    icon_vkontakte='''
        ...
    '''


Given all these configuration options, the resulting HTML markup would look like this:

    <blockquote class="tweetable">
      <p>When there is state there can be no freedom,
         but when there is freedom there will be no state.
         -- Vladimir Lenin
      </p>

      <p class="tweetable-buttons">
        <a class="tweetable-button"
           title="Click to share on Twitter"
           href="https://twitter.com/intent/tweet?text=When+there+is+state+there+can+be+no+freedom%2C%0Abut+when+there+is+freedom+there+will+be+no+state.%0A--+Vladimir+Lenin&amp;url=http%3A%2F%2Fwww.brainyquote.com%2Fquotes%2Fauthors%2Fv%2Fvladimir_lenin.html&amp;hashtags="
           target="_blank">
          <svg>Twitter icon here...</svg>
        </a>

        <a class="tweetable-button"
            title="Copy the text, then click to share on Facebook"
            href="https://www.facebook.com/sharer/sharer.php?u=http%3A%2F%2Fwww.brainyquote.com%2Fquotes%2Fauthors%2Fv%2Fvladimir_lenin.html"
            target="_blank">
          <svg>Facebook icon here...</svg>
        </a>

        <a class="tweetable-button"
            title="Click to share on LinkedIn"
            href="href="http://www.linkedin.com/shareArticle?mini=true&url={http%3A%2F%2Fwww.brainyquote.com%2Fquotes%2Fauthors%2Fv%2Fvladimir_lenin.html}&title={When+there+is+state+there+can+be+no+freedom%2C%0Abut+when+there+is+freedom+there+will+be+no+state.%0A--+Vladimir+Lenin}"
            target="_blank">
          <svg>LinkedIn icon here...</svg>
        </a>

        <a class="tweetable-button"
           title="Click to share on VKontakte"
           href="https://vk.com/share.php?url=http%3A%2F%2Fwww.brainyquote.com%2Fquotes%2Fauthors%2Fv%2Fvladimir_lenin.html&amp;title=When+there+is+state+there+can+be+no+freedom%2C%0Abut+when+there+is+freedom+there+will+be+no+state.%0A--+Vladimir+Lenin"
           target="_blank">
          <svg>VKontakte icon here...</svg>
        </a>
      </p>
    </blockquote>


### Button docs:

* https://developers.facebook.com/docs/plugins/share-button/
* http://developer.linkedin.com/documents/share-linkedin
* https://dev.twitter.com/docs/tweet-button
* http://vk.com/dev/share_details

NOTES:

* Facebook button sucks, because it [does not support](http://stackoverflow.com/questions/20956229/has-facebook-sharer-php-changed-to-no-longer-accept-detailed-parameters) prefilled text.
* LinkedIn [does not support](http://help.linkedin.com/app/answers/detail/a_id/5028/~/linkedin-signal---no-longer-supported) hashtags.

### SVG Icons

Default share buttons are rendered using [Super Tiny Icons](https://github.com/edent/SuperTinyIcons).

## Dependencies

* [Markdown 2.6+](http://pythonhosted.org/Markdown/)

## Copyright

Copyright 2014-2017 [Max Arnold](http://ar0.me/blog/en/), all rights reserved.

This software is released under the MIT License.
