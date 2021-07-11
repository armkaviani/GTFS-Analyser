ECHO off

time /t
ECHO Import start.

python gtfs_app_download_unzip.py http://data.pid.cz/PID_GTFS.zip cz_pid

python gtfs_0101_createdb.py cz_pid
python gtfs_0111_import_agency.py cz_pid
python gtfs_0112_import_routes.py cz_pid
python gtfs_0113_import_trips.py cz_pid
python gtfs_0114_import_stoptimes.py cz_pid
python gtfs_0115_import_stops.py cz_pid
python gtfs_0116_import_calendar.py cz_pid
python gtfs_0117_import_calendardates.py cz_pid

time /t
ECHO Import finished, start processing.

python gtfs_0212_query_create_table_end-stop-names.py cz_pid

python gtfs_0251_create_1_applikation_table_praha_hln.py cz_pid
python gtfs_0252_create_2_applikation_table_praha_hln.py cz_pid

time /t
ECHO Processing finished.

PAUSE