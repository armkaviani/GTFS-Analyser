ECHO off

time /t
ECHO Import start.

python gtfs_app_download_unzip.py https://gtfs.irail.be/nmbs/gtfs/latest.zip be_nmbs

python gtfs_0101_createdb.py be_nmbs
python gtfs_0111_import_agency.py be_nmbs
python gtfs_0112_import_routes.py be_nmbs
python gtfs_0113_import_trips.py be_nmbs
python gtfs_0114_import_stoptimes.py be_nmbs
python gtfs_0115_import_stops.py be_nmbs
python gtfs_0116_import_calendar.py be_nmbs
python gtfs_0117_import_calendardates.py be_nmbs

time /t
ECHO Import finished, start processing.

python gtfs_0212_query_create_table_end-stop-names.py be_nmbs

python gtfs_0241_create_1_applikation_table_bruxelles_midi.py be_nmbs
python gtfs_0242_create_2_applikation_table_bruxelles_midi.py be_nmbs

time /t
ECHO Processing finished.

PAUSE