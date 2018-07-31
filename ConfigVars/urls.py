from ConfigVars import variables

HOME_PAGE='https://www.blacktickets.in/chennai'
PAYMENTS_PAGE='https://www.blacktickets.in/orders/{0}'
MOVIEPASS_URL='https://staging.moviepass.io/'
GET_SESSION_IDS_API= "GET,https://d1n1a8bo7yrjlf.cloudfront.net/datapax/JUSTICKETS."+variables.CITY+"."+variables.MOVIE_NAME+".v1.json"
GET_SEAT_AVALIABLITY="GET,https://staging-pm.justickets.co/availability?session_id={0}&channel=JUSTICKETS-WEB&platform=WEB"
