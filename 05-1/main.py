import os
import re
from pprint import pprint


def check_update(update, later_pages):
    seen_pages = set()
    for page in update:
        # A page that has no rules is automatically valid.
        if page not in later_pages:
            seen_pages.add(page)
            continue

        # If a page that should appear later has already been seen, this update is invalid.
        for later_page in later_pages[page]:
            if later_page in seen_pages:
                print(f"  Oops! Page {page} must come before already-seen page {later_page}")
                return False
        seen_pages.add(page)

    return True


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

later_pages = {}
updates = []
processing_rules = True
for line in lines:
    stripped_line = line.strip()

    # The first empty line switches to processing updates.
    if stripped_line == '':
        processing_rules = False
        continue

    if processing_rules:
        match = re.match(r"(\d+)\|(\d+)", stripped_line)
        before = match.groups()[0]
        after = match.groups()[1]
        if before not in later_pages:
            later_pages[before] = {after}
        else:
            later_pages[before].add(after)
    else:
        updates.append(stripped_line.split(','))

middle_page_sum = 0
for update in updates:
    print(f"Checking update: [{', '.join(update)}]")
    result = check_update(update, later_pages)
    print("  Valid" if result else "  Invalid")

    if result:
        middle_page_number = int(update[(len(update) // 2)])
        print(f"  Middle page is {middle_page_number}")
        middle_page_sum += middle_page_number

print(middle_page_sum)
