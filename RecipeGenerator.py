#!/anaconda/bin/python

import requests, bs4
import random
from consts import *
import smtplib
import text

"""
Hate that feeling when you someone asks you what you want for
dinner some night this week? Well worry no more with this 
Recipe Generator!!

This script is designed to generate a pseudo-random recipe 
from allrecipes.com. When the script is run, the homepage
is obtained using requests and a list of scraped a from the
html code, which can later be used to gather the hrefs from
the list.

Based on this easily readable lxml, all the urls for a genre
of food are accumulated into a list and one is randomly 
selected.

From this genre of food, another collection of urls is 
initialized containing the urls of individual recipes. From
this list of urls, a random recipe url is chosen and 
returned.

Finally, the individual recipe url is opened and the 
necessary information for the recipe (such as the title, 
the time, the servings, the ingredients, and the directions)
is scraped from the website and compiled into a string. 

With this string, at least one of three methods can be
executed: writeRecipe(), sendText(), or sendMail(). Each
option is described in detail in the methods docstring.
"""



def recipeListGenerator():
	"""
	Returns: a list of a tags from the given url

	This function takes the html from the given url, and then
	selects the a tags (which define a hyperlink) and the a
	tags are then accumulated in the returned list.
	"""

	# Retrieves the allrecipes.com website
	res = requests.get('https://www.allrecipes.com')

	# Converts the requested website to lxml BeautifulSoup
	# so that the information is more easily read
	soup = bs4.BeautifulSoup(res.text, "lxml")

	# Select only the a tags that contain the hyperlinks and
	# return the selected list
	return(soup.select('div[id="insideScroll"] > ul > li > a'))


def urlSelector(aList):
	"""
	Returns: a pseudo-randomly selected string containing a url for a type
	of recipe from the allrecipes.com

	Parameter alist: a list of a tags which contain hyperlinks to types of
	recipes.

	From aList, the hyperlinks from each a tag are retrieved and appended
	to a list. From this new list of hyperlinks, a random hyperlink is
	chosen and returned by the function.
	"""

	# Initialize an empty list allRecipeURLs
	allRecipeURLs = []

	# For each a tag in the list aList:
	for a in aList:
		# Extract the hyperlink from href and add to allRecipeURLs list
		allRecipeURLs.append(a.get("href"))

	# Find the number of urls in the list allRecipeURLs
	aruLen = len(allRecipeURLs) - 1

	# Pseudo-Randomly choose a valid index of a url from the list
	urlNum = random.randint(0,aruLen)
	
	# Return the url for the type of recipe at the chosen index
	return(allRecipeURLs[urlNum])


def chooseRecipe(url):
	"""
	Returns: a pseudo-randomly selected string containing a url for a
	specific recipe from the type of recipe found at the url

	Parameter url: a string containing a url for a specific type of
	recipe (i.e. chicken, dessert, etc.)

	Based off of the url, all of the possible recipes for this type of
	recipe are extracted by finding the corresponding a tags. Similar to
	urlSelector(), the hyperlinks for each recipe are then extracted and
	appended to a list, from which one recipe is selected and returned.
	"""

	# Converts the requested url for a type of recipe to lxml 
	# BeautifulSoup so that the information is more easily read
	soup = bs4.BeautifulSoup(requests.get(url).text, "lxml")

	# Initialize an empty list theList
	theList = []

	# Select the specific a tags that contain the hyperlinks for recipes
	# and store all a tags in list rList
	rList = soup.select('section[class="recipe-section"] > \
		article[class="list-recipes"] > ol > \
		li[class="list-recipes__recipe"] > a')
	
	# For each recipe's a tag in rList:
	for r in rList:
		# Extract the hyperlink for the recipe from the a tag and append
		# the hyperlink to theList
		theList.append(r.get("href"))


	# Select the rest of the a tags that contain hyperlinks for recipes
	# and store all a tage in list frc
	frc = soup.select('section[class="recipe-section"] > \
		article[class="fixed-recipe-card"] > \
		div[class="fixed-recipe-card__info"] > a')

	# For each recipe's a tag in frc:
	for r in frc:
		# Extract the hyperlink for the recipe from the a tag and append
		# the hyperlink to theList
		theList.append(r.get("href"))

	# Find the number of urls in the list theList
	tlLen = len(theList)

	# Pseudo-Randomly choose a valid index of a url from the list
	urlNum = random.randint(0, tlLen) - 1

	# Return the url for the specific recipe at the chosen index
	return(theList[urlNum])


def openRecipe(url):
	"""
	Returns: a string containing all of the pertinent information to the 
	recipe. This information includes: the name of the recipe, the time
	required for preparation, the number of people served by the recipe,
	the necessary ingredients, the directions, and the url to the
	allrecipes.com website for the recipe so that the user can learn more.

	Parameter url: a string containing the url to a recipe's website.
	"""

	# Retrive the url website and convert to lxml BeautifulSoup
	soup = bs4.BeautifulSoup(requests.get(url).text, "lxml")


	# Find the name of the recipe, which is located in the class attribute
	# "recipe-summary__h1", and retrive the name from the list that the 
	# function find_all() returns.
	name = soup.find_all(attrs={"class": "recipe-summary__h1"})[0].string

	# Find the time required for preparation in the same manner as the 
	# name, which is located in the class attribute "ready-in-time"
	time = soup.find_all(attrs={"class": "ready-in-time"})[0].string

	# Find the number of servings, which is found in the meta tag with the
	# id "metaRecipeServings" and is retrieved from the list returned by
	# select()
	serve = soup.select('meta[id="metaRecipeServings"]')[0].get("content")


	# Initialize an empty string ingredients
	ingredients = ""

	# Find all ingredients (raw html text, not strings), which are under
	# the class attributes named "recipe-ingred_txt added" in the html,
	# and add to list iRaw
	iRaw = soup.find_all(attrs={"class": "recipe-ingred_txt added"})
	
	# For each element in the list iRaw:
	for i in iRaw:
		# Concatenate newline character and string of i to ingredients
		ingredients += '\n' + i.string


	# Initialize an empty list directions
	directions = []

	# Find all directions (raw html text, not strings), which are under 
	# the class attributes named "recipe-directions__list--item" in the
	# html, and add to list dRaw
	dRaw = soup.find_all(attrs={"class": "recipe-directions__list--item"})
	
	# For each element in the list dRaw:
	for d in dRaw:
		# Convert d to a string 
		dir = d.string
		# If the string is not None:
		if(dir != None):
			# If there is a new line character
			if(dir.index('\n') != -1):
				# Append the string up to but not including the newline
				directions.append(dir[:dir.index('\n')])
			# Else if there is not a new line character
			else:
				# Append the whole string with no string slicing
				directions.append(dir)


	# Concatenate the accumulated information with formatting except
	# for the directions
	text = "Recipe Name: " + name + '\n' + \
		"Time: " + time + '\n' + \
		"Serves: " + serve + '\n\n' + \
		"Ingredients: " + ingredients + '\n\n' + \
		"Directions: "


	# Initialize a variable to count through the direction steps
	num = 1

	# For each step in the directions
	for step in directions:
		# Concatenate a newline char, the step num, and the step
		text += '\n' + "    " + str(num) + ". " + step
		# Increase the step number
		num += 1


	# Concatenate three newline chars, a message, and the url
	text += '\n\n\n' + "For more, check out " + url
	
	# Return the formatted information
	return(text)


def writeRecipe(text):
	"""
	Parameter text: a string containing the recipe, starting with the
	recipe name in the format: 
	"Recipe Name: _________ (newline character)
	Time...."

	This method slices the text to extract the recipe name, then
	concatenates the recipe name with the location of the recipe folder
	and the .txt extension. Using this name, a new file with the name is
	opened in the recipes folder, with the text being contained in the
	body of the file.
	"""

	# Extract the name of the recipe for the file name from text
	name = text[text.index(':') + 2:text.index('Time') - 1]

	# Concatenate the location Recipes with the name (no spaces) and .txt
	fName = REC_FOLDER + name.replace(' ', '') + '.txt'

	# Open a file under the file name with the intent of writing
	f = open(fName, 'w')
	
	# Wrie the text to the file
	f.write(text)

	# Close the file for clean finish
	f.close()


def sendMail(text):
	"""
	Parameter text: a string containing the recipe, starting with the
	recipe name in the format: 
	"Recipe Name: _________ (newline character)
	Time...."

	This function is used to send an email to the address in the email
	constant REC_ADDRESS from the other constant EMAIL_ADDRESS. The 
	subject of the message is "Recipe Time" concatenated with the recipe
	name (which is extracted from the text), and the body of the email is
	the recipe from the text parameter.
	"""

	# open an SSL connection for SMTP on Gmail
	smtpObj = smtplib.SMTP_SSL(SMTP, GMAIL_PORT)

	# Identify yourself to an ESMTP server using EHLO
	smtpObj.ehlo()

	# Log in to the Gmail in the EMAIL_ADDRESS constant with password
	smtpObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

	# Extract the name of the recipe for the subject from text
	recipeName = text[text.index(':') + 2:text.index('Time') - 1]

	# Concatenate the beginning of the subject line with the name and '\n'
	subject = 'Subject: Recipe Time! ' + recipeName + '\n'

	# Send the email from the EMAIL_ADDRESS to REC_ADDRESS, with the
	# the contents being the subject and the text
	smtpObj.sendmail(EMAIL_ADDRESS, REC_ADDRESS, (subject + text))

	# Quit out of SMTP to ensure clean closure
	smtpObj.quit()


"""
The following code is the part of the script that runs when called, and 
results in the output that the user witnesses and receives.
"""


# Boolean that ensures that a valid recipe was returned and all functions
# were successfully run
valid = False

# Initialize a variable that the text will be stored in for later
r = ''

# Take in the user's input to choose what is done with the recipe
userIn = input("How would you like to see the recipe?\n" + \
	"d for a text document, t for a text, m for an email: ")

# Convert the input to all lower case to prevent from errors due to case
userIn = userIn.lower()

# While the text is not produced properly to any type of error
while(not valid):
	try:
		# Try to run each method in the proper order to generate a recipe
		r = openRecipe(chooseRecipe(urlSelector(recipeListGenerator())))
	
		# If everything properly runs and there are no errors, valid is
		# changed to True and the while loop is broken out of
		valid = True

	# If any sort of error is raised: 
	except:
		# Do nothing here; valid is still False so run the while loop
		pass


# If the user's input contains a d:
if("d" in userIn):
	# write the recipe to a text document
	writeRecipe(r)

# If the user's input contains a t 
if("t" in userIn):
	# send a text to the constant
	text.sendText(r, TWILIO_NUM, JFP_NUMBER)

# If the user's input contains an m
if("m" in userIn):
	# send an email to the constant email
	sendMail(r)
