# dad-joke-cli

A command-line daily digest: 5 facts, 5 breaking headlines, a tip of the day, and a quote of the day.

Facts, the tip, and the quote are picked deterministically from the date - running it again later today shows the same picks, tomorrow shows a different set. No dependencies beyond the Python standard library, and no state file: the "today" set is derived from the date itself.

Breaking news is fetched live from [BBC News](https://www.bbc.co.uk/news)'s public RSS feed, since real breaking news can't be curated offline - this is the one part of the tool that needs an internet connection. If the network is unavailable, that section prints a short notice and the rest of the digest (facts, tip, quote) still runs normally.

## Usage

```bash
python daily_digest.py
```

That's it - no arguments. Every run prints the full digest.

## Example

```
Daily Digest - Friday, July 31, 2026
====================================

Fun Facts
---------
1. ...
2. ...
...

Breaking News (BBC News)
------------------------
1. ...
...

Tip of the Day
--------------
...

Quote of the Day
----------------
"..."
  - Author
```
