import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify


#       TODO TAKE USERS INPUT AND REPLACE ALL WHITESPACES WITH - [FOR ROTTEN TOMATOES]

print('-----------------IMDB RATINGS-------------------')
IMDBrequest = requests.get('https://www.imdb.com/find?q=' + 'social network')
print(IMDBrequest)

soup = BeautifulSoup(IMDBrequest.text, 'html.parser')
tbody = soup.find(class_='findSection')




ids=[]
photos=[]
for links in tbody.find_all('td',{'class':'primary_photo'}):
    ids.append(links.find('a').get('href'))
    photos.append(links.find('img').get('src'))
correctIds = []
for x in ids:
    correctIds.append(x[7:-1])

infos=[[correctIds],[photos]]
print(infos)

#       COLLECTING ALL IDS FROM  SEARCH

print(correctIds)



selecredMovie = correctIds[0]

print('----------------')

#REQUESTING INFOS ABOUT SELECTED MOVIE/SHOW

detailsReq = requests.get('https://www.imdb.com/title/'+selecredMovie)


detailSoup = BeautifulSoup(detailsReq.text, 'html.parser')

titleBlock = detailSoup.find(class_='title_block')
movieTitle = titleBlock.find('h1', {'class':''}).getText()
print('this is that part'+ movieTitle)
movieRating = titleBlock.find('strong').get('title')
print(movieRating)
print()

#       HANDLING ROTTEN TOMATOES REQUESTS AND RATINGS

print('-----------------ROTTEN TOMATOES-------------------')
RTrequest = requests.get('https://www.rottentomatoes.com/m/'+'the-social-network')

print(RTrequest)
rottenSoup = BeautifulSoup(RTrequest.text, 'html.parser')



movieNameRT = rottenSoup.find('h1', {'class': 'mop-ratings-wrap__title mop-ratings-wrap__title--top'}).getText()
print(movieNameRT)

tomatometer = rottenSoup.find('span',{'class': 'mop-ratings-wrap__percentage'}).getText().replace(' ','').replace('\n','')
tomatometerCount =rottenSoup.find('small',{'class':'mop-ratings-wrap__text--small'}).getText().replace(' ','').replace('\n','')
audienceScore = rottenSoup.find('span', {'class':'mop-ratings-wrap__percentage'}).getText().replace(' ','').replace('\n','')
audienceCount = rottenSoup.find('div',{'class':'mop-ratings-wrap__review-totals mop-ratings-wrap__review-totals--not-released'}).getText().replace(' ','').replace('\n','')

rottenTomatoesInfo = {'movieName':movieNameRT, 'tomatoraiting':{'tomatometer':tomatometer,'count':tomatometerCount},
                      'audienceRating':{'audienceScore':audienceScore, 'audineceCount':audienceCount}}
print(rottenTomatoesInfo)


app = Flask(__name__)

@app.route('/')
def hw():
    return 'helloWorld'


@app.route('/<movie>')
def do_dhis(movie):
    IMDBrequest = requests.get('https://www.imdb.com/find?q=' + movie)
    soup = BeautifulSoup(IMDBrequest.text, 'html.parser')
    tbody = soup.find(class_='findSection')

    ids = []
    photos = []
    for links in tbody.find_all('td', {'class': 'primary_photo'}):
        ids.append(links.find('a').get('href'))
        photo = links.find('img').get('src')
        info={'photo':photo}
        photos.append(info)
    titles=[]
    for links in tbody.find_all('td', {'class': 'result_text'}):

        name = links.find('a').getText()
       # year =links.getText() ,'year':year
        infos={'title':name}
        titles.append(infos)


    correctIds = []
    for x in ids:
        correctIds.append(x[7:-1])

    infos ={'ids': correctIds,'photos': photos,'titles': titles},
    result=[infos,movie]
    return jsonify(searchResult=infos,
                   searchedMovie=movie)


@app.route('/id/<movieID>')
def movieInfo(movieID):
    detailsReq = requests.get('https://www.imdb.com/title/' + movieID)
    detailSoup = BeautifulSoup(detailsReq.text, 'html.parser')

    titleBlock = detailSoup.find(class_='title_block')
    movieTitle = titleBlock.find('h1', {'class': ''}).getText()
    movieRating = titleBlock.find('strong').get('title')
    movieInfo={'movieTitle': movieTitle, 'movieRating': movieRating}
    return jsonify(result=movieInfo)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
