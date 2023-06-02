#!/Users/chang/miniconda3/envs/obspy/bin/python

from seismometers import stations
import matplotlib.pyplot as plt
import os
from matplotlib.transforms import blended_transform_factory
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from obspy import Stream
from obspy import Trace
from obspy import read
from obspy.geodetics import gps2dist_azimuth
from obspy.clients.fdsn import Client as FDSN_Client
from pathlib import Path

########################################################################
# define parameters
########################################################################
start_time = UTCDateTime(2022,12,1)
end_time = UTCDateTime(2023,1,1)


########################################################################
# use HVO AQMS events databasde
########################################################################
client = FDSN_Client('http://hvo-aqms.wr.usgs.gov')


########################################################################
# fetch events from server
########################################################################
events = client.get_events(start=start_time,
                           end=end_time,
                           minlatitude=18.5, 
                           maxlatitude=22.5,
                           minlongitude=-161.0, 
                           maxlongitude=-154.0,
                           )


########################################################################
# save events as QuakeML file
########################################################################
for event in events:
    # get EVID
    rID = str(event.resource_id)
    evid = "hv" + rID[-8:]
    # check if the directory exists
    if not os.path.exists(f"catalogs/{evid}"):
        # If it doesn't exist, create it
        os.makedirs(f"catalogs/{evid}")
    event.write(f"catalogs/{evid}/{evid}.xml", format="QUAKEML")


########################################################################
# plot events
########################################################################
#events.plot(projection='local',
#            resolution='f',
#            color='depth',
#            )
#
#plt.close()
########################################################################
