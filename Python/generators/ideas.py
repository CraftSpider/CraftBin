
import random


DEMOGRAPHICS = ("Dogs", "Cats", "Fish", "Boomers", "Millenials", "The Elderly", "Kids", "Babies", "Teens", "Adults",
                "LGBTQ+", "Straights", "Gen X", "Gen Z")

ACTIVITIES = ("Amazon", "Uber Eats", "Google", "YouTube", "Reddit", "Twitter", "GMail", "Dropbox", "Radare2", "An IDE",
              "A Laptop", "A POS", "Insurance", "A Calendar", "Twitch", "Webcomics", "ERD Software")

while True:
    print(f"{random.choice(ACTIVITIES)} for {random.choice(DEMOGRAPHICS)}")
    input()
