import logging
import os
import boto3
from botocore.exceptions import ClientError
import json


def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get(
                                 'S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4', s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def recipe_parser(url):
    """Return a recipe for the given URL"""
    import requests
    from bs4 import BeautifulSoup

    jdict = {}

    jdict['link'] = url
    # -----------------------------------------------------------------------------------------------------------------
    neededwebsite = url

    try:  # because if url is invalid then it supposed to give error which will be return from Exception
        source = requests.get(neededwebsite)
        # print(type(source))
        source.raise_for_status()
        # Type of variable soup is BeautifulSoup # It's text of html text of given website.
        soup = BeautifulSoup(source.text, 'html.parser')

        # We wrote it beause of "table class="wikitable" style="width=100%"
        required = soup.find('ul', class_="mntl-structured-ingredients__list")
        # find will find perticular x ....... /x that x from whole html text
        # print(table) # table is for this table in
        # print(type(source))
    except Exception as e:
        print(e)
    htmlofitems = required.find_all('p')

    spanhtml = []
    for i in range(0, len(htmlofitems)):
        spanhtml1 = htmlofitems[i].find_all('span')
        spanhtml.append(spanhtml1)
    listofallitem = []

    # FOR jdict library
    # jdict=dict()
    jdict1 = dict()
    jlist = []
    for i in range(len(spanhtml)):
        singleitem = []
        singledict = dict()
        for j in range(0, len(spanhtml[i])):
            if spanhtml[i][j].text:
                # print(spanhtml[i][j].text)
                if spanhtml[i][j].get("data-ingredient-quantity") == 'true':
                    singledict["qty"] = spanhtml[i][j].text
                elif spanhtml[i][j].get("data-ingredient-unit") == 'true':
                    singledict["unit"] = spanhtml[i][j].text
                elif spanhtml[i][j].get("data-ingredient-name") == 'true':
                    singledict["name"] = spanhtml[i][j].text
    # print(singledict)
        jlist.append(singledict)
    jdict['ingredients'] = jlist
    # print(jdict)
    # now give value to jdict key & val as this dict

    for i in range(len(spanhtml)):
        singleitem = []
        for j in range(0, len(spanhtml[i])):
            if spanhtml[i][j].text:
                singleitem.append(spanhtml[i][j].text)
        listofallitem.append(singleitem)

    cooktime_Numberof_people_numerical = soup.find_all(
        'div', class_="mntl-recipe-details__value")
    cooktime_Numberof_people_catagory = soup.find_all(
        'div', class_="mntl-recipe-details__label")
    print(" ")
    print("Details for this recipe:")
    print(" ")
    for i in range(len(cooktime_Numberof_people_catagory)):
        key = cooktime_Numberof_people_catagory[i].text.lower()
        # Transform key
        key = key.replace(" ", "_")
        value = cooktime_Numberof_people_numerical[i].text
        jdict[key] = value
    id_ing = 1
    for i in listofallitem:
        print(f'{id_ing}":"{i}')
        id_ing = id_ing+1
    print(singleitem)
    print(" ")
    print("Let's look at steps for recipe:")
    print(" ")
    requiredforstep = soup.find(
        'ol', class_="comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup")
    stephtml = requiredforstep.find_all('li')
    steps = []
    for i in range(len(stephtml)):
        steps.append([f"Step Number {i+1}: {stephtml[i].text.strip()}"])

    # jdict for steps
    # jdict=dict()
    jlist = []
    for i in range(len(stephtml)):
        jdict1 = dict()
        jdict1['step'] = i
        jdict1['text'] = stephtml[i].text.strip()
        # print(jdict1)
        jlist.append(jdict1)
    jdict['steps'] = jlist
    # jdict
    # now add this to final code
    return jdict


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    print(recipe_parser(
        "https://www.allrecipes.com/recipe/8511288/washington-apple-cocktail/"))
