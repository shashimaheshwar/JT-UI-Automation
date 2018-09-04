import UtilityPackage.SessionContainer as sc
import UtilityPackage.CustomLogger as cl
import logging,random

log = cl.customLogger(logging.DEBUG)

container=sc.Build_Session_Container(200)

Free_Seating_movie = sc.search_session({"type":"REALTIME","theatre":"Luxe: Phoenix Market City",
                     "advance_token":False,'free_seating':True},container)
Qota_session_movie = sc.search_session({"type":"QUOTA","theatre":"Luxe: Phoenix Market City",
                     "advance_token":False,'free_seating':False},container)
Advance_Free_seating_movie = sc.search_session({"type":"REALTIME","theatre":"Luxe: Phoenix Market City",
                     "advance_token":True,'free_seating':True},container)
Advance_Qota_movie = sc.search_session({"type":"QUOTA","theatre":"Luxe: Phoenix Market City",
                     "advance_token":True,'free_seating':False},container)

try:
    Free_Seating = Free_Seating_movie[0].movie+",Luxe: Phoenix Market"
    Qota_session = Qota_session_movie[0].movie+",Luxe: Phoenix Market"
    Advance_Free_seating = Advance_Free_seating_movie[0].movie+",Luxe: Phoenix Market"
    Advance_Qota = Advance_Qota_movie[0].movie+",Luxe: Phoenix Market"

except UnboundLocalError:
    print("Session Does not exist")
    log.error(UnboundLocalError+"Session with provided query does not exist")

print(Free_Seating_movie[random.randint(0,len(Qota_session_movie))].movie)
for element in Free_Seating_movie:
    print(element.movie, element.theatre, element.session_id)

'''
Free_Seating_movie_dic = {}
list_of_ob = sc.search_session({"type": "REALTIME", "theatre": "Luxe: Phoenix Market City",
                             "advance_token": False, 'free_seating': True}, container)
for element in list_of_ob:
    if element.movie in Free_Seating_movie_dic.keys():
        Free_Seating_movie_dic[element.movie] = Free_Seating_movie_dic[element.movie] + "," + element.session_id
    else:
        Free_Seating_movie_dic[element.movie] = element.session_id

Qota_session_movie_dic = {}
list_of_ob = sc.search_session({"type":"QUOTA","theatre":"Luxe: Phoenix Market City",
                     "advance_token":False,'free_seating':False}, container)
for element in list_of_ob:
    if element.movie in Qota_session_movie_dic.keys():
        Qota_session_movie_dic[element.movie] = Qota_session_movie_dic[element.movie] + "," + element.session_id
    else:
        Free_Seating_movie_dic[element.movie] = element.session_id

Advance_Free_seating_dic = {}
list_of_ob = sc.search_session({"type":"REALTIME","theatre":"Luxe: Phoenix Market City",
                     "advance_token":True,'free_seating':True}, container)
for element in list_of_ob:
    if element.movie in Advance_Free_seating_dic.keys():
        Advance_Free_seating_dic[element.movie] = Advance_Free_seating_dic[element.movie] + "," + element.session_id
    else:
        Advance_Free_seating_dic[element.movie] = element.session_id

Advance_Qota_movie_dic = {}
list_of_ob = sc.search_session({"type":"QUOTA","theatre":"Luxe: Phoenix Market City",
                     "advance_token":True,'free_seating':False}, container)
for element in list_of_ob:
    if element.movie in Advance_Qota_movie_dic.keys():
        Advance_Qota_movie_dic[element.movie] = Advance_Qota_movie_dic[element.movie] + "," + element.session_id
    else:
        Advance_Qota_movie_dic[element.movie] = element.session_id
        '''

