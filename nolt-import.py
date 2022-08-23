import csv
import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

# configuring environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# getting env variables
csv_filename = os.environ.get("CSV_FILENAME")
api_key = os.environ.get("API_KEY")
api_user = os.environ.get("API_USER")
api_endpoint = os.environ.get("API_ENDPOINT")

# a little function to ensure f strings will get re-evaluated after defining the variables
def fstr(template):
    return eval(f'f"""{template}"""')

# ----------- initiating variables -----------

category_id = 9
fb_status = ""
post_author = ""
post_excerpt = ""
post_url = ""
post_tag = ""
post_title = ""
num_votes = ""

# templates for the raw content to be uploaded
req_content_topic = "Feature Requested By: {post_author}\nNumber of Votes: {num_votes}\nView Original Post: {post_url}\n\n{post_excerpt}"
req_content_post = "Comment By: {post_author}\n\n{post_excerpt}"
req_title = "[{fb_status}] {post_title}"
cur_topic = 297

# ----------- setting up api request -----------

# headers for requests
headers = {'Content-Type': 'application/json',
           'Api-Key': api_key,
           'Api-Username': api_user}

# ----------- reading csv and cleaning data -----------

# opening csv export and cleaning it
with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")

    next(csv_reader)

    for line in csv_reader:
        post_url = line[1]
        post_title = line[2]
        num_votes = line[5]
        fb_status = line[14]
        post_tag = line[23]
        post_excerpt = line[25]
        post_author = line[28]
        fb_tag = line[31]

        if fb_status != 'Archived':
            # this means this line is a comment, not a top-level post
            if line[0] == '':
                # this indicates this is a real comment, not an admin change
                if line[24] == "BASIC":
                    # creating payload for POST request
                    post_data = {"raw": fstr(req_content_post),
                            "topic_id": cur_topic,
                            "category": category_id,
                            "tags[]": post_tag}

                    # sending post request and saving response as response object
                    response = requests.post(url = api_endpoint, json = post_data, headers = headers)

                    res = response.content
                    res = res.decode('UTF-8')

                    print(res)
                    print("Current Topic ID: ", cur_topic)
            # this means this is a top-level post
            else:
                final_title = fstr(req_title)
                if fb_status == "Completed":
                    final_title = "🥳 " + final_title
                elif int(num_votes) >= 30 or fb_status == "High Demand":
                    final_title = "🔥 " + final_title

                topic_data = {"title": final_title,
                        "raw": fstr(req_content_topic),
                        "category": category_id,
                        "tags": [fb_tag]}

                if post_tag != "":
                    # creating payload for POST request
                    topic_data["tags"] = [post_tag, fb_tag]

                # sending post request and saving response as response object
                response = requests.post(url = api_endpoint, json = topic_data, headers = headers)

                print("This is the post tag: ", post_tag)
                res = response.content
                res = res.decode('UTF-8')
                return_data = json.loads(res)
                print(res)
                cur_topic = return_data['topic_id']
                print("Current Topic ID: ", cur_topic)
