
# Filter, Rewrite, and Scraper Rules
[Home](https://miniflux.app/index.html) > [Documentation](https://miniflux.app/docs/index.html)
- [Feed Filtering Rules](https://miniflux.app/docs/rules.html#feed-filtering-rules)
- [Entry Filtering Rules](https://miniflux.app/docs/rules.html#filtering-rules)
- [Content Rewrite Rules](https://miniflux.app/docs/rules.html#rewrite-rules)
- [URL Rewrite Rules](https://miniflux.app/docs/rules.html#rewriteurl-rules)
- [Scraper Rules](https://miniflux.app/docs/rules.html#scraper-rules)

## Feed Filtering Rules [¶](https://miniflux.app/docs/rules.html#feed-filtering-rules)

Miniflux has a regex\-based filtering system that allows you to ignore or keep articles. For more advanced filtering, you can use the [Entry Filtering Rules](https://miniflux.app/docs/rules.html#filtering-rules) feature.

### Regex\-Based Blocking Filters

Block rules ignore articles with a title, an entry URL, a tag, or an author that matches the regex \([RE2 syntax](https://golang.org/s/re2syntax)\).

For example, the regex `\(?i\)miniflux` will ignore all articles with a title that contains the word Miniflux \(case insensitive\).

Ignored articles won’t be saved into the database.

### Regex\-Based Keep Filters

Keep rules retain only articles that match the regex \([RE2 syntax](https://golang.org/s/re2syntax)\).

For example, the regex `\(?i\)miniflux` will keep only the articles with a title that contains the word Miniflux \(case insensitive\).

## Entry Filtering Rules [¶](https://miniflux.app/docs/rules.html#filtering-rules)

Since Miniflux 2.2.10, filtering rules can be defined for each feed and globally on the Settings page.

There are two types of rules:
- **Block Rules**: Ignore articles that match the regex.
- **Keep Rules**: Retain only articles that match the regex.

### Rules Format and Syntax

Example:

```
FieldName=RegEx
FieldName=RegEx
FieldName=RegEx
```
- Each rule must be on a separate line.
- Duplicate rules are allowed. For example, having multiple `EntryTitle` rules is possible.
- The provided regex should use the [RE2 syntax](https://golang.org/s/re2syntax).
- The order of the rules matters as the processor stops on the first match for both Block and Keep rules.
- Invalid rules are ignored.

Available Fields:
- `EntryTitle`
- `EntryURL`
- `EntryCommentsURL`
- `EntryContent`
- `EntryAuthor`
- `EntryTag`
- `EntryDate`

### Date Patterns

The `EntryDate` field supports the following date patterns:
- `future` \- Match entries with future publication dates.
- `before:YYYY\-MM\-DD` \- Match entries published before a specific date.
- `after:YYYY\-MM\-DD` \- Match entries published after a specific date.
- `between:YYYY\-MM\-DD,YYYY\-MM\-DD` \- Match entries published between two dates.
- `max\-age:duration` \- Match entries that are not older than a specific duration \(e.g., `max\-age:7d` for 7 days\). Valid time units are “ns”, “us” \(or “µs”\), “ms”, “s”, “m”, “h”, “d”.

Date format must be `YYYY\-MM\-DD`, for example: `2024\-01\-01`.

Block rules examples:

```
EntryDate=future                                # Ignore articles with future publication dates
EntryDate=before:2024-01-01                     # Ignore articles published before January 1st, 2024
EntryDate=max-age:30d                           # Ignore articles older than 30 days
EntryTitle=(?i)miniflux                         # Ignore articles with "Miniflux" in the title
EntryTitle=(?i)\b(save|take|get)\s+\$\d{2,5}\b  # Ignore articles with "Save $50", "Get $100…" in the title
EntryTitle=(?i)\$\d{2,5}\s+(off|discount)\b     # Ignore articles with "$50 off"
EntryTitle=(?i)\bbest\s+.*\bdeals?\b            # Ignore articles with "Best Foobar Deals…"
EntryTitle=(?i)\bgift\s+(guide|ideas|list)\b    # Ignore articles that look like listicles
```

Keep rules examples:

```
EntryDate=between:2024-01-01,2024-12-31         # Keep only articles published in 2024
EntryDate=after:2024-03-01                      # Keep only articles published after March 1st, 2024
```

### Global Rules & Feed Rules Ordering

Rules are processed in this order:
1. Global Block Rules
2. Feed Block Rules
3. Global Keep Rules
4. Feed Keep Rules

## Content Rewrite Rules [¶](https://miniflux.app/docs/rules.html#rewrite-rules)

To improve the reading experience, it’s possible to alter the content of feed items.

For example, if you are reading a popular comic website like [XKCD](https://xkcd.com/), it’s nice to have the image title \(the `alt` attribute\) added under the image, especially on mobile devices where there is no `hover` event.
`add\_dynamic\_image`Tries to add the highest quality images from sites that use JavaScript to load images \(e.g., either lazily when scrolling or based on screen size\).`add\_dynamic\_iframe`Tries to add embedded videos from sites that use JavaScript to load iframes \(e.g., either lazily when scrolling or after the rest of the page is loaded\).`add\_image\_title`Adds each image's title as a caption under the image.`add\_youtube\_video`Inserts a YouTube video into the article \(automatic for Youtube.com\).`add\_youtube\_video\_from\_id`Inserts a YouTube video into the article based on the video ID.`add\_invidious\_video`Inserts an Invidious player into the article \(automatic for https://invidio.us\).`add\_youtube\_video\_using\_invidious\_player`Inserts an Invidious player into the article for YouTube feeds.`add\_castopod\_episode`Inserts a Castopod episode player.`add\_mailto\_subject`Inserts mailto links subject into the article.`base64\_decode`Decodes base64 content. It can be used with a selector: `base64\_decode\(".base64"\)`, but can also be used without arguments: `base64\_decode`. In this case, it will try to convert all TextNodes and always fall back to the original text if it cannot decode.`nl2br`Converts new lines `\\n` to `<br>` \(useful for non\-HTML content\).`convert\_text\_links`Converts text links to HTML links \(useful for non\-HTML content\).`fix\_medium\_images`Attempts to fix Medium's images rendered in JavaScript.`use\_noscript\_figure\_images`Uses `<noscript>` content for images rendered with JavaScript.`replace\("search term"\|"replace term"\)`Searches and replaces text.`remove\(".selector, \#another\_selector"\)`Removes DOM elements.`parse\_markdown`Converts Markdown to HTML. **This rule has been removed in version 2.2.4.**`remove\_tables`Removes any tables while keeping the content inside \(useful for email newsletters\).`remove\_clickbait`Removes clickbait titles \(converts uppercase titles\).`replace\_title\("search\-term"\|"replace\-term"\)`Adjusts entry titles.`add\_hn\_links\_using\_hack`Opens HN comments with Hack.`add\_hn\_links\_using\_opener`Opens HN comments with Opener.`fix\_ghost\_cards`Converts [Ghost](https://ghost.org) link cards to regular links.`remove\_img\_blur\_params`Removes blur parameters from image URLs.

Miniflux includes a set of [predefined rules](https://github.com/miniflux/v2/blob/main/internal/reader/rewrite/rules.go) for some websites, but you can define your own rules.

On the feed edit page, enter your custom rules in the field “Rewrite Rules” like this:

```
rule1,rule2
```

Separate each rule with a comma.

## URL Rewrite Rules [¶](https://miniflux.app/docs/rules.html#rewriteurl-rules)

Sometimes it might be required to rewrite a URL in a feed to fetch better\-suited content.

For example, for some users, the URL [https://www.npr.org/sections/money/2021/05/18/997501946/the\-case\-for\-universal\-pre\-k\-just\-got\-stronger](https://www.npr.org/sections/money/2021/05/18/997501946/the-case-for-universal-pre-k-just-got-stronger) displays a cookie consent dialog instead of the actual content, and it would be preferred to fetch the URL [https://text.npr.org/997501946](https://text.npr.org/997501946) instead.

The following rule does this:

```
rewrite("^https:\/\/www\.npr\.org\/\d{4}\/\d{2}\/\d{2}\/(\d+)\/.*$"|"https://text.npr.org/$1")
```

This will rewrite all URLs from the original feed to URLs pointing to *text.npr.org* when the article content is fetched. You may also need to add your own scraper rule because the default rule will try to fetch \#storytext.

Another example is the German page `https://www.heise.de/news/Industrie\-ruestet\-sich\-fuer\-Gasstopp\-Forscher\-vorsichtig\-optimistisch\-7167721.html`, which splits the article into multiple pages. The full text can be read on `https://www.heise.de/news/Industrie\-ruestet\-sich\-fuer\-Gasstopp\-Forscher\-vorsichtig\-optimistisch\-7167721.html?seite=all`.

The URL rewrite rule for that would be:

```
rewrite("(.*?\.html)"|"$1?seite=all")
```

## Scraper Rules [¶](https://miniflux.app/docs/rules.html#scraper-rules)

When an article contains only an extract of the content, you can fetch the original web page and apply a set of rules to get relevant content.

Miniflux uses CSS selectors for custom rules. These custom rules can be saved in the feed properties \(select a feed and click on edit\).

| CSS Selector | Description |
|---|---|
| `div\#articleBody` | Fetch a `div` element with the ID `articleBody`. |
| `div.content` | Fetch all `div` elements with the class `content`. |
| `article, div.article` | Use a comma to define multiple rules. |

Miniflux includes a list of [predefined rules](https://github.com/miniflux/v2/blob/main/internal/reader/scraper/rules.go) for popular websites. You can contribute to the project to keep them up to date.

Under the hood, Miniflux uses the library [Goquery](https://github.com/PuerkitoBio/goquery).
[Edit this page](https://github.com/miniflux/website/edit/main/content/docs/rules.md)
