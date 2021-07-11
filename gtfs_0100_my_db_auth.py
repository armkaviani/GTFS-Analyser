'''
Username and password for MariaDB
Usage in python sourcecode:

    import gtfs_0100_my_db_auth
    db_username = gtfs_0100_my_db_auth.db_username
    db_password = gtfs_0100_my_db_auth.db_password
    
Version: 2021-06-02 ... Version 001
'''

db_username = "root"      # "yourusername"
db_password = "secretpw"  # "yourpassword"
db_name = "gtfs01"  # Test with this databasename == feedpath