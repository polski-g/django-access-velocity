django-access-velocity

access_velocity package


Keeps track of logged in users's most recent and current IP. If they change
then it computes the distance (geoip) between the two locations and then the 
velocity based on the time difference. If a threshold is exceeded, block the 
user for a time.
