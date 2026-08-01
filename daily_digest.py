#!/usr/bin/env python3
"""Prints a daily digest: 5 facts, 5 breaking headlines, a tip, and a quote.

Facts, the tip, and the quote are chosen deterministically from the date, so
re-running this on the same day always shows the same picks, and tomorrow
shows a different set - no state file needed. News is live and always
current, since "breaking news" can't meaningfully be curated offline.
"""

import random
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

NEWS_FEED_URL = "http://feeds.bbci.co.uk/news/rss.xml"
NEWS_SOURCE_NAME = "BBC News"
NEWS_HEADLINE_COUNT = 5
NEWS_TIMEOUT_SECONDS = 8

FACTS = {
    "science": [
        "Honey found in ancient Egyptian tombs, thousands of years old, is still perfectly edible - honey never spoils.",
        "Octopuses have three hearts and blue, copper-based blood.",
        "A bolt of lightning can reach temperatures roughly five times hotter than the surface of the sun.",
        "Bananas contain enough potassium-40 to be measurably, though harmlessly, radioactive.",
        "Water expands by about 9% when it freezes, which is why ice floats.",
        "The human body has enough iron in it to make a small nail, about 3 grams on average.",
        "Sound travels about four times faster through water than through air.",
        "A single bolt of lightning carries enough energy to toast roughly 100,000 slices of bread.",
    ],
    "history": [
        "Oxford University is older than the Aztec Empire - Oxford was teaching students by 1096, the Aztec Empire was founded in 1428.",
        "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid of Giza.",
        "The shortest war in recorded history, between Britain and Zanzibar in 1896, lasted around 38 minutes.",
        "Ancient Romans used urine as a mouthwash ingredient because of its ammonia content.",
        "The first known vending machine, dispensing holy water for a coin, was built in ancient Egypt around the 1st century AD.",
        "Napoleon Bonaparte's height was actually about average for his era - the 'short' reputation came from a French-to-English unit mix-up.",
        "The Eiffel Tower can grow more than 6 inches taller in summer as its iron expands in the heat.",
        "The Great Fire of London in 1666 destroyed most of the city but only a handful of deaths were officially recorded.",
    ],
    "space": [
        "A day on Venus is longer than a year on Venus - it takes about 243 Earth days to rotate once but only 225 to orbit the Sun.",
        "There are more stars in the observable universe than grains of sand on every beach on Earth.",
        "Neutron stars are so dense that a teaspoon of their material would weigh about a billion tons.",
        "Footprints left by Apollo astronauts on the Moon could last millions of years since there's no wind or water to erode them.",
        "Saturn's rings are made almost entirely of ice and rock, ranging from dust-sized grains to house-sized chunks.",
        "Light from the Sun takes about 8 minutes and 20 seconds to reach Earth.",
        "Jupiter's Great Red Spot is a storm bigger than Earth that has been raging for at least 350 years.",
        "Space is completely silent because sound needs a medium like air or water to travel, and space is a near-vacuum.",
    ],
    "animals": [
        "A group of flamingos is called a 'flamboyance.'",
        "Sea otters hold hands while sleeping so they don't drift apart from each other.",
        "Elephants are one of the few animals that can recognize themselves in a mirror.",
        "A shrimp's heart is located in its head.",
        "Wombat droppings are cube-shaped, which keeps them from rolling away and helps mark territory.",
        "The mantis shrimp can punch with the acceleration of a bullet, fast enough to briefly boil the water around it.",
        "Cows form close social bonds and can become stressed when separated from their preferred companions.",
        "A tiger's stripe pattern is also on its skin, not just its fur - each one is unique, like a fingerprint.",
    ],
    "geography": [
        "Russia spans 11 time zones, more than any other country in the world.",
        "Point Nemo, in the Pacific Ocean, is the point on Earth farthest from any land - about 1,670 miles from the nearest coast.",
        "More than half the world's population lives within a roughly 3,000-mile radius centered near Southeast Asia.",
        "The Sahara Desert was lush and green, with lakes and rivers, as recently as about 10,000 years ago.",
        "Canada has more lakes than the rest of the world combined - an estimated 2 million or more.",
        "Vatican City is the smallest country in the world by both area and population.",
        "Alaska is both the westernmost and easternmost U.S. state, because the Aleutian Islands cross the 180th meridian.",
        "Africa is home to both the world's shortest river, the Roe River, and one of its longest, the Nile.",
    ],
}

TIPS = [
    "Write tomorrow's top 3 priorities before you stop working today - decisions are easier with a fresh mind, not first thing in the morning.",
    "Batch small tasks like emails and quick replies into one block instead of letting them interrupt deep work all day.",
    "Keep a glass of water nearby - mild dehydration is a common, invisible cause of afternoon fatigue.",
    "Give yourself a real stopping time each day. Work expands to fill the time available for it.",
    "When you feel stuck, change your environment for ten minutes - a different room, a walk, some fresh air.",
    "Say no to new commitments by default; you can always say yes later once you know the real cost.",
    "Keep your to-do list to what you can realistically finish today, not everything you'd like to finish someday.",
    "A five-minute task done now often takes fifteen minutes of dread if you put it off instead.",
    "Turn off notifications during your most focused hour of the day - protect it like a meeting you can't miss.",
    "Write things down the moment you think of them; trying to remember is a constant, quiet drain on attention.",
    "Do the hardest task of the day first, while your willpower is freshest.",
    "Take a short walk after meals - it aids digestion and resets your mind before the next task.",
    "Keep your workspace slightly cleaner than feels necessary; clutter adds small, constant friction.",
    "Read one page of a book before checking your phone in the morning - it sets the tone for the day.",
    "Ask 'what would make this easy?' before assuming a task has to be hard.",
    "Schedule breaks like you schedule meetings - they're just as easy to skip if you don't.",
    "Reply to messages in batches at set times rather than the instant they arrive.",
    "Keep a running list of small wins - it's easy to forget progress when you're focused on what's left.",
    "Sleep is the cheapest performance upgrade available; protect the last hour before bed.",
    "When overwhelmed, write down everything on your mind, then pick just one thing to do next.",
    "Set a timer for 10 minutes on a task you're avoiding - momentum is often the hardest part.",
    "Keep your goals visible somewhere you'll actually see them daily, not buried in a document.",
    "Learn one keyboard shortcut a week for the tools you use most - small efficiencies compound.",
    "End the day by writing down one thing that went well - it's easy to only remember what didn't.",
]

QUOTES = [
    ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Whether you think you can or you think you can't, you're right.", "Henry Ford"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("Do what you can, with what you have, where you are.", "Theodore Roosevelt"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
    ("Hardships often prepare ordinary people for an extraordinary destiny.", "C.S. Lewis"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("What you get by achieving your goals is not as important as what you become by achieving them.", "Zig Ziglar"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("Your time is limited, so don't waste it living someone else's life.", "Steve Jobs"),
    ("The only limit to our realization of tomorrow will be our doubts of today.", "Franklin D. Roosevelt"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("Perfection is not attainable, but if we chase perfection we can catch excellence.", "Vince Lombardi"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("Opportunities don't happen. You create them.", "Chris Grosser"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
]


def _daily_rng(section: str) -> random.Random:
    """A random.Random seeded by (today's date, section name).

    Deterministic per day so repeated runs match, and namespaced per section
    so facts/tip/quote don't all shift together off one shared seed.
    """
    return random.Random(f"{date.today().isoformat()}:{section}")


def daily_facts(count: int = 5) -> list[str]:
    pool = [fact for facts in FACTS.values() for fact in facts]
    return _daily_rng("facts").sample(pool, min(count, len(pool)))


def daily_tip() -> str:
    return _daily_rng("tip").choice(TIPS)


def daily_quote() -> tuple[str, str]:
    return _daily_rng("quote").choice(QUOTES)


def fetch_breaking_news(count: int = NEWS_HEADLINE_COUNT) -> list[str]:
    """Latest headlines from a live RSS feed. Raises on any network/parse failure."""
    request = urllib.request.Request(
        NEWS_FEED_URL, headers={"User-Agent": "daily-digest-cli/1.0"}
    )
    with urllib.request.urlopen(request, timeout=NEWS_TIMEOUT_SECONDS) as response:
        root = ET.fromstring(response.read())

    headlines = []
    for item in root.iter("item"):
        title = item.findtext("title")
        if title:
            headlines.append(title.strip())
        if len(headlines) >= count:
            break
    return headlines


def print_section(title: str, lines: list[str]) -> None:
    print(title)
    print("-" * len(title))
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")
    print()


def main() -> None:
    today = date.today().strftime("%A, %B %d, %Y")
    print(f"Daily Digest - {today}")
    print("=" * (15 + len(today)))
    print()

    print_section("Fun Facts", daily_facts())

    try:
        headlines = fetch_breaking_news()
        print_section(f"Breaking News ({NEWS_SOURCE_NAME})", headlines)
    except (urllib.error.URLError, ET.ParseError, TimeoutError) as exc:
        print(f"Breaking News ({NEWS_SOURCE_NAME})")
        print("-" * (16 + len(NEWS_SOURCE_NAME)))
        print(f"Couldn't fetch news right now ({exc}). Check your internet connection.")
        print()

    print("Tip of the Day")
    print("-" * 14)
    print(daily_tip())
    print()

    print("Quote of the Day")
    print("-" * 16)
    quote, author = daily_quote()
    print(f'"{quote}"')
    print(f"  - {author}")


if __name__ == "__main__":
    main()
