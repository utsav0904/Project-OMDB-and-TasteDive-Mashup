
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
import requests_with_caching
import json
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_related_titles(["Black Panther", "Captain Marvel"])
# get_related_titles([])

def get_movies_from_tastedive(artist):
    parameters={"q":artist,"type":"movies","limit":5}
    page=requests_with_caching.get("https://tastedive.com/api/similar",params=parameters)
    py_data=json.loads(page.text)
    return py_data
   
def extract_movie_titles(data):
    titles=[]
    for movie in data['Similar']['Results']:
        titles.append(movie['Name'])
    return titles    
def get_related_titles(movietitles):
    relatedmovie=[]
    for titles in movietitles:
        print(titles)
        a=get_movies_from_tastedive(titles)
        b=extract_movie_titles(a)
        for movie in b:
            if movie not in relatedmovie:
                relatedmovie.append(movie)
    return relatedmovie            

def get_movie_data(title):
    mdata={}
    parameters={"t":title,"r":"json"}
    page=requests_with_caching.get("http://www.omdbapi.com/",params=parameters)
    mdata=json.loads(page.text)
    return mdata
def get_movie_rating(data):
    rotten_rating=0
    if len(data['Ratings']) > 1:
        if data['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            rotten_rating = data['Ratings'][1]['Value'][:2]
            rotten_rating = int(rotten_rating)
    else:
        rotten_rating = 0

    return rotten_rating

def getkey(item):
    return item[1]


def get_sorted_recommendations(movieslist):
    related_movies = get_related_titles(movieslist)
    ratings = []
    sorted_list = []
    for movie in related_movies:
        a = get_movie_data(movie)
        ratings.append(get_movie_rating(a))

    temp_tuple1 = zip(related_movies, ratings)
    temp_tuple2 = sorted(temp_tuple1, key=getkey, reverse=True)
    print(temp_tuple2)
    for i in range(len(temp_tuple2) - 1):
        if temp_tuple2[i][0] not in sorted_list:
            if temp_tuple2[i][1] == temp_tuple2[i + 1][1]:
                if temp_tuple2[i][0] < temp_tuple2[i + 1][0]:
                    sorted_list.append(temp_tuple2[i + 1][0])
                    sorted_list.append(temp_tuple2[i][0])
            else:
                sorted_list.append(temp_tuple2[i][0])

    print(sorted_list)

    return sorted_list