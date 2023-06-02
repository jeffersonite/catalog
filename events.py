#!/Users/chang/miniconda3/envs/obspy/bin/python

from seismometers import stations
import matplotlib.pyplot as plt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import os
from matplotlib.transforms import blended_transform_factory
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from obspy import Stream
from obspy import Trace
from obspy import read_events
from obspy.geodetics import gps2dist_azimuth
from obspy.clients.fdsn import Client as FDSN_Client
from pathlib import Path

########################################################################
# define parameters
########################################################################
yyyy = 2022
mm = 12
t1 = date(yyyy,mm,1)
t2 = t1 + relativedelta(months=1)


########################################################################
# use HVO AQMS events databasde
########################################################################
# client = FDSN_Client('https://hvo-paqms1.wr.usgs.gov')
# client = FDSN_Client('http://130.118.86.181')


# ########################################################################
# # fetch events from server
# ########################################################################
# events = client.get_events(start=UTCDateTime(t1),
#                            end=UTCDateTime(t2),
#                            minlatitude=18.5, 
#                            maxlatitude=22.5,
#                            minlongitude=-161.0, 
#                            maxlongitude=-154.0,
#                            )


# ########################################################################
# # save monthly events as QuakeML file
# ########################################################################
# # check if the directory exists
# if not os.path.exists(f"{yyyy}/{mm:02d}"):
#     # If it doesn't exist, create it
#     os.makedirs(f"{yyyy}/{mm:02d}")

# events.write(f"{yyyy}/{mm:02d}/events.xml", format="QUAKEML")


########################################################################
# read events in QuakeML file
########################################################################
events = read_events(f"{yyyy}/{mm:02d}/events.xml", format="QUAKEML")


########################################################################
# save individual events as QuakeML file
########################################################################
for event in events:
    # get EVID
    rID = str(event.resource_id)
    evid = "hv" + rID[-8:]
    # check if the directory exists
    if not os.path.exists(f"{yyyy}/{mm:02d}/{evid}"):
        # If it doesn't exist, create it
        os.makedirs(f"{yyyy}/{mm:02d}/{evid}")
    event.write(f"{yyyy}/{mm:02d}/{evid}/event.xml", format="QUAKEML")


########################################################################
# convert ObsPy catalog into Pandas dataframe
########################################################################
eids = []
etypes = []
emodes = []
times = []
lats = []
lons = []
deps = []
mags = []
mtypes = []
mstas = []
mstates = []

for event in events:
    rID = str(event.resource_id)
    evid = "hv" + rID[-8:]
    if len(event.origins) != 0 and len(event.magnitudes) != 0:
        eids.append(evid)
        etypes.append(event.event_type)
        emodes.append(event.origins[0].evaluation_mode)
        times.append(event.origins[0].time.datetime)
        lats.append(event.origins[0].latitude)
        lons.append(event.origins[0].longitude)
        deps.append(event.origins[0].depth / 1000.)
        mags.append(event.magnitudes[0].mag)
        mtypes.append(event.magnitudes[0].magnitude_type)
        mstas.append(event.magnitudes[0].station_count)
        mstates.append(event.magnitudes[0].station_count)
    elif len(event.origins) != 0:
        eids.append(evid)
        etypes.append(event.event_type)
        emodes.append(event.origins[0].evaluation_mode)
        times.append(event.origins[0].time.datetime)
        lats.append(event.origins[0].latitude)
        lons.append(event.origins[0].longitude)
        deps.append(event.origins[0].depth / 1000.)
        mags.append(np.nan)
        mtypes.append('N/A')
        mstas.append(0)
        mstates.append('N/A')

df = pd.DataFrame({'evid':eids,
                   'origintime':times,
                   'latitude':lats,
                   'longitude':lons,
                   'depth':deps,
                   'magnitude':mags,
                   'mtype':mtypes,
                   'mstations':mstas,
                   'state':emodes,
                   'etype':etypes,
                   }, 
                   index = eids)


########################################################################
# create monthly html
########################################################################
html = df.to_html(index=False, render_links=True,
                  formatters={'magnitude': '{:,.1f}'.format,
                              'latitude': '{:,.4f}'.format,
                              'longitude': '{:,.4f}'.format,
                              'depth': '{:,.1f}'.format,
                              'mstations': '{:,.0f}'.format,
                              })
html = html.replace('border="1" class="dataframe"','')
for ids in eids:
    html = html.replace(ids,f'<a href="{ids}/index.html" target="_blank">{ids}</a>')

h = open(f"{yyyy}/{mm:02d}/index.html", "w")
header = """
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <style>
      h3  {
          font-size: 100%;
          }

      p   {
          font-size: 100%;
          }

      img {
          max-width: 100%;
          height: auto;
          border-radius: 8px;
          display: block;
          margin-left: auto;
          margin-right: auto;
          }
      table {
          border-collapse: collapse;
          width: 100%;
          }
      th, td {
          padding: 3px;
          text-align: center;
          border-bottom: thin solid #ddd;
          font-size: 100%;
          font-family: Trebuchet MS, sans-serif;
          }
      tr:nth-child(even){background-color: #ebebeb}
      tr:hover {background-color: #f8c8d0;}
      th {
          background-color: #343434;
          color: white;
        }
      body {
        margin-bottom: 60px;
        }
      .footer {
          position: fixed;
          bottom: 0;
          left: 0;
          right: 0;
          background: #111;
          height: auto;
          width: 100%;
          padding-top: 0px;
          color: #fff;
          text-align: center;
          font-family: Trebuchet MS, sans-serif;
          font-size: 75%
            }
    </style>
  </head>
  <body>
"""

footer = f"""
    <div class="footer">
      <p>Last updated on {datetime.now().strftime("%Y-%m-%d %H:%M")} HST</p>
    </div>
  </body>
</html>
"""

h.write(header)
h.write(html)
h.write(footer)
h.close()


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
