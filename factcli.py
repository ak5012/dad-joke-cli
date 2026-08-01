#!/usr/bin/env python3
import argparse
import random

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


def get_fact(category: str | None = None) -> str:
    pool = FACTS[category] if category else [f for facts in FACTS.values() for f in facts]
    return random.choice(pool)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print random fun facts.")
    parser.add_argument("count", nargs="?", type=int, default=1, help="how many facts to print (default: 1)")
    parser.add_argument(
        "-c", "--category", choices=sorted(FACTS), help="limit facts to one category"
    )
    parser.add_argument(
        "-l", "--list-categories", action="store_true", help="list available categories and exit"
    )
    args = parser.parse_args()

    if args.list_categories:
        for name in sorted(FACTS):
            print(name)
        return

    for _ in range(max(1, args.count)):
        print(get_fact(args.category))


if __name__ == "__main__":
    main()
