import requests
from bs4 import BeautifulSoup


def parse_recipe(recipe_url):
    try:  # because if url is invalid then it supposed to give error which will be return from Exception
        source = requests.get(recipe_url)
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
        print(
            f"{cooktime_Numberof_people_catagory[i].text} : {cooktime_Numberof_people_numerical[i].text}")
    print(" ")
    print("Here is list of all ingredients needed with it's quantity:\n")

    for i in range(len(listofallitem)):
        print(i, ":", listofallitem[i])

    print(" ")
    print("Let's look at steps for recipe:")
    print(" ")
    requiredforstep = soup.find(
        'ol', class_="comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup")
    stephtml = requiredforstep.find_all('li')
    steps = []
    for i in range(len(stephtml)):
        steps.append([f"Step Number {i+1}: {stephtml[i].text.strip()}"])
    for i in steps:
        for j in i:
            print(j)
            print(" ")
    print("You can refer same recipe via youtube based on video link below,which is best recommendation of YouTube:")


if __name__ == "__main__":
    recipe_url = input("Enter the recipe url: ")
    recipe(recipe_url)