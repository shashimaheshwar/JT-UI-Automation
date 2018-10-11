import UtilityPackage.SessionContainer as sc
import UtilityPackage.CustomLogger as cl
import logging,random
from ConfigVars.TestConfig import variables

log = cl.customLogger(logging.DEBUG)

container=sc.Build_Session_Container(200)
try:
    Free_Seating_movie = sc.search_session({"type":"REALTIME","theatre":variables.THEATRE_NAME,
                     "advance_token":False,'free_seating':True},container)
    Qota_session_movie = sc.search_session({"type":"QUOTA","theatre":variables.THEATRE_NAME,
                     "advance_token":False,'free_seating':False},container)
    Advance_Free_seating_movie = sc.search_session({"type":"REALTIME","theatre":variables.THEATRE_NAME,
                     "advance_token":True,'free_seating':True},container)
    Advance_Qota_movie = sc.search_session({"type":"QUOTA","theatre":variables.THEATRE_NAME,
                     "advance_token":True,'free_seating':False},container)
except Exception:
    log.error("Unable to find any session with such query.")


try:
    Free_Seating = Free_Seating_movie[random.randint(0,len(Free_Seating_movie))].movie+","+variables.THEATRE_NAME
    Qota_session = Qota_session_movie[random.randint(0,len(Qota_session_movie))].movie+","+variables.THEATRE_NAME
    Advance_Free_seating = Advance_Free_seating_movie[random.randint(0,len(Advance_Free_seating_movie))].movie+","+variables.THEATRE_NAME
    Advance_Qota = Advance_Qota_movie[random.randint(0,len(Advance_Qota_movie))].movie+","+variables.THEATRE_NAME

except UnboundLocalError:
    print("Session Does not exist")
    log.error(UnboundLocalError+"Session with provided query does not exist")



