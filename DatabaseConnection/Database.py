from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
# from CustomLogger.logger import Logger

# logging = Logger('logFiles/test.log')


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('app_log_files.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Connector:
    def __init__(self):
        """
        :DESC: Creates connection with Database when backend thread runs.
        """
        logger.info('INFO', 'Obj created')
        self.Client_id = 'hOYNoTvQQUtrRXJaYmdRWAQi'
        self.Client_secret = 'dE9cD8r92xpFXU5S.yT_2iDk+m44xNP.2MT8x4nGDj5yrjDWWvFDB0i+-b,m1t.z-rjpXOUg4Wxg60BpZkMAcpa5Nqk--9knajc-T2FecdjBZNS1ySPnae+U4XFgkEps'
        cloud_config = {'secure_connect_bundle': 'secure-connect-flightdatabase.zip'}
        auth_provider = PlainTextAuthProvider(self.Client_id, self.Client_secret)
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = cluster.connect()

    def master(self):
        """
        :DESC: Creates table if not existed into database
        :return:
        """
        self.session.execute("use flighpricedata")
        self.session.execute("select release_version from system.local")
        self.session.execute("CREATE TABLE Data(id uuid PRIMARY KEY,Airline text,Source text,Destination text,Total_Stops text,Total_Duration int,Journey_month int,Journey_day int);")

    def addData(self, result):
        """
        :param result: Gets data from user and puts it into database
        :return:
        """
        logger.info('INFO', "Inside addData")
        logger.info('INFO', "Inside addData")

        column = "id, Airline, Source,Destination, Total_Stops, Total_Duration, Journey_month, Journey_day"
        value = "{0},'{1}','{2}','{3}','{4}',{5},{6},{7}".format('uuid()', result['Airline'], result['Source'],
                                                                 result['Destination'], result['Total_Stops'],
                                                                 result['Total_Duration'], result['Journey_month'],
                                                                 result['Journey_day'])
        logger.info('INFO', "String created")
        custom = "INSERT INTO Data({}) VALUES({});".format(column, value)

        logger.info('INFO', "Key created")
        self.session.execute("USE flighpricedata")

        output = self.session.execute(custom)

        logger.info('INFO', "Column inserted {}".format(output))


    def getData(self):
        """
        :DESC: Retrieves Data from Database
        :return:
        """
        self.session.execute("use flighpricedata")
        row = self.session.execute("SELECT * FROM Data;")
        collection = []
        for i in row:
            collection.append(tuple(i))
        logger.info('INFO', "Retrieved Data from Database : {}".format(i))
        return tuple(collection)
