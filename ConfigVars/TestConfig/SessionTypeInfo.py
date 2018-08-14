import UtilityPackage.SessionContainer as sc
import UtilityPackage.CustomLogger as cl
import logging

log = cl.customLogger(logging.DEBUG)

container=sc.Build_Session_Container(200)
y=sc.search_session({"type":"REALTIME","theatre":"Luxe: Phoenix Market City",
                     "advance_token":False,'free_seating':True},container)[0].movie

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