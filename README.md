# discourse-nolt-import
What it says on the tin! A simple and noodley Python script to mass import Nolt feedback in CSV format as topics and posts in Discourse.

## Installations
python 3 and pip: [tutorial for Mac here](https://docs.python-guide.org/starting/install3/osx/)

requests: [tutorial here](https://www.geeksforgeeks.org/how-to-install-requests-in-python-for-windows-linux-mac/)

dotenv: [tutorial here](https://www.python-engineer.com/posts/dotenv-python/)

## How to download
Green "Code" button on the top right > Download as .zip > Extract to a convenient location

## Project setup
1. Copy the .env.sample file and rename the copy's filename to .env
2. Go to [Google Sheets](sheets.google.com) and type `=IMPORTDATA("https://opal.nolt.io/api/csv?apikey=be0d8bd6-b8de-424f-98df-4165f7b65c72&comments=true&votes=true")` into the first cell - it will automatically import
3. Export everything as a .csv and rename the file to something with no spaces like nolt_feedback.csv, and move the file from your Downloads into the same folder as everything else in this project
4. Add this filename to the .env like so: `CSV_FILENAME="nolt_feedback.csv"`
5. Go to your Discourse community > Settings > API > New API Key
6. Select "single" for user level and "global" for scope
7. Copy the secret key and add it to .env like so: `API_KEY="YOUR_KEY_HERE"`
8. Add the Discourse username you're logged into (ideally an admin) to the .env file as well, like so: `API_USER="USERNAME_HERE"` (respect the caps in your username)
9. Add the API endpoint you need to the .env file, which will likely be `API_ENDPOINT="https://[Discourse URL Here]/posts.json"`
10. Save your .env file ;D
11. Last thing: if you want to post everything to a specific category, make sure the category ID number is correct in line 24 of the nolt-import.py script, change as you need! Sorry for leaving it hard-coded

## Running the script
1. Open your terminal
2. Navigate to the project folder using the [cd command](https://www.geeksforgeeks.org/cd-command-in-linux-with-examples/)
3. Run command: `python3 nolt-import.py`

## Gotchas
Discourse will probably rate-limit you so follow [this tutorial](https://meta.discourse.org/t/global-rate-limits-and-throttling-in-discourse/78612) to make sure that doesn't happen!
