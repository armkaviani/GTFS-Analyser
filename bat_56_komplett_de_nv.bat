ECHO off

TIME /t
ECHO Import start.

python gtfs_app_download_unzip.py https://download.gtfs.de/germany/nv_free/latest.zip de_nv

python gtfs_0101_createdb.py de_nv
python gtfs_0111_import_agency.py de_nv
python gtfs_0112_import_routes.py de_nv
python gtfs_0113_import_trips.py de_nv
python gtfs_0114_import_stoptimes.py de_nv
python gtfs_0115_import_stops.py de_nv
python gtfs_0116_import_calendar.py de_nv
python gtfs_0117_import_calendardates.py de_nv

TIME /t
ECHO Import finished, start processing.

python gtfs_0212_query_create_table_end-stop-names.py de_nv

python gtfs_0231_create_1_applikation_table_leipzig_hbf.py de_nv
python gtfs_0232_create_2_applikation_table_leipzig_hbf.py de_nv

TIME /t
ECHO Processing finished.

PAUSE