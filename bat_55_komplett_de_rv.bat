ECHO off

time /t
ECHO Import Start.

python gtfs_app_download_unzip.py https://download.gtfs.de/germany/rv_free/latest.zip de_rv

python gtfs_0101_createdb.py de_rv
python gtfs_0111_import_agency.py de_rv
python gtfs_0112_import_routes.py de_rv
python gtfs_0113_import_trips.py de_rv
python gtfs_0114_import_stoptimes.py de_rv
python gtfs_0115_import_stops.py de_rv
python gtfs_0116_import_calendar.py de_rv
python gtfs_0117_import_calendardates.py de_rv

TIME /t
ECHO Import Finished, start Processing.

python gtfs_0212_query_create_table_end-stop-names.py de_rv

python gtfs_0221_create_1_applikation_table_berlin_hbf.py de_rv
python gtfs_0222_create_2_applikation_table_berlin_hbf.py de_rv

TIME /t
ECHO Processing Finished.

PAUSE