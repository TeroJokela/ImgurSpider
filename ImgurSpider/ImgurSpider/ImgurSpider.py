import os
import requests
from urllib import request
from bs4 import BeautifulSoup

howManyPicturesDownloaded = 0
strTags = '' # Tags

class Image():
    # Get the direct link for a picture and download it
    def DownloadImage(TargetImage):
        # Get the TargetImage site's source and look for specific elements
        sourceCode = requests.get(TargetImage)
        sourceCodeText = sourceCode.text
        soupDownload = BeautifulSoup(sourceCodeText, "html.parser")
        for i in soupDownload.findAll('link', {'rel': 'image_src'}):
            href = i.get('href')
            
            # We make the filename the image ID
            filename = ''
            for j in range(5, 12):
                filename += href[-j]
            filename = filename[::-1]
            # We make sure there isn't any '/' characters that could mess up our program
            finalFilename = ''
            for x in filename:
                if x == '/':
                    finalFilename += 'X'
                else:
                    finalFilename += x

            # We choose the file extension by checking if it's a GIF or not
            if Image.isGif(soupDownload):
                finalFilename += '.gif'
            else:
                finalFilename += '.jpg'

            # We download and save the picture to the 'strTags' folder with the name of the image ID
            global strTags
            request.urlretrieve(href, Image.Directory(strTags) +  finalFilename)
            global howManyPicturesDownloaded
            howManyPicturesDownloaded += 1
            print("Downloaded", href[:27], '(' + finalFilename + ')')

    # We check if the image is a GIF or not by checking if there's a "video-elements" class in 
    def isGif(soup):
        for i in soup.findAll('div', {'class': 'video-elements'}):
            return True
        return False

    # Make a new folder for the wanted path if one doesn't already exist
    def Directory(folderName):
        completePath = folderName + '/'
        if not os.path.exists(completePath):
            os.makedirs(completePath)
            return completePath
        else:
            return completePath

# We get links to all the images we get from the crawl URL and crawl those links to get the image URL and download it
def Spider(url):
    try:
        sourceCode = requests.get(url)
        sourceCodeText = sourceCode.text
        soup = BeautifulSoup(sourceCodeText, "html.parser")
        for i in soup.findAll('a', {'class': 'image-list-link'}):
            href = i.get('href')
            if href != None:
                finishURL = 'https://imgur.com' + href
                Image.DownloadImage(finishURL)
    except requests.exceptions.ConnectionError:
        print("No internet connection")
    except:
        print("Unknown error, please find out what's the problem")
        
# Create an Imgur link using the tags we were given
def createLink():
    global strTags
    strTags = input("> ")
    fin = ''
    for i in strTags:
        if i == ' ':
            fin += '+'
        else:
            fin += i
    return 'https://imgur.com/search/time?q=' + fin

# Our main starting point for our program
def main():
    print("What kind of pictures do you want?")
    crawl_url = createLink()
    print("Downloading pictures from [", crawl_url, "]\nPlease wait . . .")
    Spider(crawl_url)
    print("Finished")
    if howManyPicturesDownloaded > 0:
        print("I downloaded", howManyPicturesDownloaded, "pictures!")
    else:
        print("I found nothing")
    input("Press enter to quit . . . ")

# Run the main function unless this is used as a library
if __name__ == "__main__":
    main()
