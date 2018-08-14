import requests
import json

class Session():
    def __init__(self,movie,movie_id,theatre,theatre_id,screen,session_id,date,type,advance_token,free_seating):
        self.movie=movie
        self.movie_id=movie_id
        self.theatre=theatre
        self.theatre_id=theatre_id
        self.screen=screen
        self.session_id=session_id
        self.date=date
        self.type=type
        self.advance_token=advance_token
        self.free_seating=free_seating

# Build an Array of Session Objects.
# First_N_Movies --> Collect Session
# information about first N movies in the datapacks. Add more number can hinder performance


def Build_Session_Container(first_N_Movies):
    Session_container=[]
    citesPack=requests.get('https://d1n1a8bo7yrjlf.cloudfront.net/datapax/JUSTICKETS.chennai.v1.json')
    if citesPack.status_code==200:
        citesPack=json.loads(citesPack.content)
    else:
        return None
    counter=1
    for movie_object in citesPack['movies']:
        if counter>=first_N_Movies:
            break
        cityMoviePack=requests.get('https://d1n1a8bo7yrjlf.cloudfront.net/datapax/JUSTICKETS.chennai.'+movie_object['url']+'.v1.json')
        if cityMoviePack.status_code==200:
            cityMoviePack=json.loads(cityMoviePack.content)
            for items in cityMoviePack['sessions']:
                l_movie= movie_object['name']
                l_movie_id=movie_object['id']
                l_theatre=items['screen']['theatre']['name']
                l_theatreid=items['screen']['theatre']['id']
                l_screen=items['screen']['name']
                l_sessionid=items['id']
                l_date=items['date']
                l_type=items['type']
                l_advance_token=items['advance_token']
                l_free_seating=items['free_seating']
                session= Session(movie=l_movie,movie_id=l_movie_id,theatre=l_theatre,theatre_id=l_theatreid,
                    screen=l_screen,session_id=l_sessionid,date=l_date,type=l_type,advance_token=l_advance_token,free_seating=l_free_seating)
                Session_container.append(session)
                session=None
        counter=counter+1

    return Session_container


def search_session(Query, sessionContainter):
    result=[]
    for sessions in sessionContainter:
        match=True
        for items in Query:
            if eval('sessions.'+items)==Query[items]:
                pass
            else:
                match=False
        if match is True:
            if sessions not in result:
                result.append(sessions)
    return result
