# Java Practice Website (all categories)

This is a simple static website for your Java code/output screenshots. It includes the question names supplied for all 11 categories in your pasted list, plus the Basic Programming titles you sent earlier. Basic Programming question 70 was missing its question text, so that title is marked as not provided.

## Organize your screenshots

1. Extract this ZIP.
2. Put your category folders together inside one main folder. Folder names can be common variations such as `basic prgraming`, `exception handling`, `oop`, or `single dimention array`.
3. In each category folder, use matching screenshot names such as `q1-1_code.png` and `q1-1_output.png`. The text before `_code` and `_output` must match.
4. Open Command Prompt in this website folder and run:

   `py scripts\organize_screenshots.py "C:\path\to\JavaScreenshots" --output .`

   Replace the example path with the real location of your screenshots folder.
5. Open `index.html` in your browser.

The organizer creates `programs.js`, copies screenshots to `screenshots/`, and writes `pairing-review.csv`. Open the CSV to spot missing code/output pairs. If a category has more screenshot pairs than question titles supplied, the additional ones appear as Question N.

## Notes

- This ZIP cannot include your local screenshots unless you upload them here; run the organizer on your computer to copy them into the website.
- The website displays code first and output second.
- Search and category filters work after the organizer generates `programs.js`.
