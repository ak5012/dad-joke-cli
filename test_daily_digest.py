#!/usr/bin/env python3
"""Tests for daily_digest. Stdlib only, no network: python -m unittest"""
import contextlib
import io
import unittest
import urllib.error
import xml.etree.ElementTree as ET
from datetime import date
from unittest import mock

import daily_digest

SAMPLE_RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
  <title>Sample feed</title>
  <item><title>  First headline  </title></item>
  <item><title>Second headline</title></item>
  <item><title>Third headline</title></item>
  <item><title>Fourth headline</title></item>
  <item><title>Fifth headline</title></item>
  <item><title>Sixth headline</title></item>
</channel></rss>"""


def frozen_date(year, month, day):
    """Patch daily_digest's `date` so today() is fixed."""
    stub = mock.MagicMock()
    stub.today.return_value = date(year, month, day)
    return mock.patch.object(daily_digest, "date", stub)


def fake_urlopen(payload):
    """Patch urlopen to return `payload` from a context manager."""
    response = mock.MagicMock()
    response.read.return_value = payload
    response.__enter__.return_value = response
    return mock.patch("urllib.request.urlopen", return_value=response)


def run_main():
    """Run main() with output captured, returning what it printed."""
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink):
        daily_digest.main()
    return sink.getvalue()


class TestJokes(unittest.TestCase):
    def test_every_category_has_jokes(self):
        for name, jokes in daily_digest.JOKES.items():
            self.assertTrue(jokes, f"{name} is empty")

    def test_no_duplicate_jokes(self):
        pool = [joke for jokes in daily_digest.JOKES.values() for joke in jokes]
        self.assertEqual(len(pool), len(set(pool)))

    def test_daily_joke_comes_from_the_pool(self):
        pool = [joke for jokes in daily_digest.JOKES.values() for joke in jokes]
        with frozen_date(2026, 8, 10):
            self.assertIn(daily_digest.daily_joke(), pool)

    def test_same_day_gives_the_same_joke(self):
        with frozen_date(2026, 8, 10):
            first = daily_digest.daily_joke()
            second = daily_digest.daily_joke()
        self.assertEqual(first, second)

    def test_the_joke_changes_across_the_year(self):
        seen = set()
        for day in range(1, 29):
            with frozen_date(2026, 2, day):
                seen.add(daily_digest.daily_joke())
        self.assertGreater(len(seen), 1, "joke never changes from day to day")


class TestDeterminism(unittest.TestCase):
    def test_facts_are_stable_within_a_day(self):
        with frozen_date(2026, 8, 10):
            self.assertEqual(daily_digest.daily_facts(), daily_digest.daily_facts())

    def test_facts_are_not_repeated_within_one_day(self):
        with frozen_date(2026, 8, 10):
            facts = daily_digest.daily_facts(5)
        self.assertEqual(len(facts), 5)
        self.assertEqual(len(facts), len(set(facts)))

    def test_tip_and_quote_are_stable_within_a_day(self):
        with frozen_date(2026, 8, 10):
            self.assertEqual(daily_digest.daily_tip(), daily_digest.daily_tip())
            self.assertEqual(daily_digest.daily_quote(), daily_digest.daily_quote())

    def test_sections_are_seeded_independently(self):
        # Same day, different sections should not draw the same index.
        with frozen_date(2026, 8, 10):
            joke_rng = daily_digest._daily_rng("joke").random()
            tip_rng = daily_digest._daily_rng("tip").random()
        self.assertNotEqual(joke_rng, tip_rng)

    def test_quote_is_a_text_author_pair(self):
        with frozen_date(2026, 8, 10):
            quote, author = daily_digest.daily_quote()
        self.assertTrue(quote and author)


class TestNews(unittest.TestCase):
    def test_parses_headlines_from_the_feed(self):
        with fake_urlopen(SAMPLE_RSS):
            headlines = daily_digest.fetch_breaking_news(3)
        self.assertEqual(headlines, ["First headline", "Second headline", "Third headline"])

    def test_stops_at_the_requested_count(self):
        with fake_urlopen(SAMPLE_RSS):
            self.assertEqual(len(daily_digest.fetch_breaking_news(5)), 5)

    def test_network_failure_propagates(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            with self.assertRaises(urllib.error.URLError):
                daily_digest.fetch_breaking_news()

    def test_malformed_feed_raises_parse_error(self):
        with fake_urlopen(b"not xml at all"):
            with self.assertRaises(ET.ParseError):
                daily_digest.fetch_breaking_news()


class TestMain(unittest.TestCase):
    def test_prints_every_section(self):
        with frozen_date(2026, 8, 10), fake_urlopen(SAMPLE_RSS):
            output = run_main()
        for heading in ("Fun Facts", "Breaking News", "Joke of the Day",
                        "Tip of the Day", "Quote of the Day"):
            self.assertIn(heading, output)

    def test_digest_survives_a_news_outage(self):
        outage = mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("down"))
        with frozen_date(2026, 8, 10), outage:
            output = run_main()
        self.assertIn("Couldn't fetch news right now", output)
        # The offline sections must still print.
        for heading in ("Fun Facts", "Joke of the Day", "Tip of the Day", "Quote of the Day"):
            self.assertIn(heading, output)

    def test_joke_section_prints_the_days_joke(self):
        with frozen_date(2026, 8, 10), fake_urlopen(SAMPLE_RSS):
            joke = daily_digest.daily_joke()
            output = run_main()
        self.assertIn(joke, output)


if __name__ == "__main__":
    unittest.main()
