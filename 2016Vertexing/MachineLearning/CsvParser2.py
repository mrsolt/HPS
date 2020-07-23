from utils import logi
import pandas as pd
import os
import matplotlib.pyplot as plt


class CsvParser2(object):
    '''
    CsvParser objects attributes map the CSV structure
    '''
    # Attributes
    CSV_FILE      = ''
    CSV_HEADER    = ''
    NAME          = ''
    DESCRIPTION   = ''
    RAW_DF        = None
    RAW_NP        = None
    RAW_ROWS      = 0
    RAW_COLUMNS   = 0
    RAW_NX        = 0
    RAW_M         = 0
    DATA_HEADER   = ''
    DATA_DF       = None
    DATA_NP       = None # numpy array of shape (nx, m)
    DATA_ROWS     = 0
    DATA_COLUMNS  = 0
    DATA_NX       = 0
    DATA_M        = 0
    FILTERED_DF   = None # Filtered out rows

    def __init__(self, csvFile, clean=True, filter=True, name='', descr='') -> None:
        '''

        :param csvFile: CSV File location
        '''
        df               = pd.read_csv(csvFile)
        rows             = df.shape[0]
        columns          = df.shape[1]
        logi('Reading CSV file %s found %d rows and %d columns' % (csvFile, rows, columns))
        self.RAW_NX          = columns
        self.RAW_M           = rows
        self.RAW_ROWS    = rows
        self.RAW_COLUMNS = columns
        logi('Found %d features and %d samples' % (self.RAW_NX, self.RAW_M))
        self.CSV_FILE    = csvFile
        self.CSV_HEADER  = self.getHeader(df)
        self.NAME        = name
        self.DESCRIPTION = descr
        self.updateRaw(df)
        if filter:
            df = self.filter(df)
        if clean:
            logi('Cleaning data')
            df = self.clean(df)
        self.updateData(df)
        self.assertShapes()

    def updateRaw(self, df):
        self.RAW_DF = df
        self.RAW_NP = df.to_numpy()

    def updateData(self, df):
        self.DATA_DF                      = df
        self.DATA_NP                      = df.to_numpy().T
        self.DATA_ROWS, self.DATA_COLUMNS = df.shape
        self.DATA_M   , self.DATA_NX      = df.shape

    def getHeader(self, df):
        return list(df.columns)


    def getDF(self):
        '''
        Get the dataframe from csvFile
        :return:
        '''
        return self.RAW_DF

    def clean(self, df):
        '''
        Clean RAW_DF based on a hard coded condition 'condition1'
        :return: clean DataFrame
        '''
        condition1                        = df['uncM'] > -9999.
        # condition2 ....

        condition                         = condition1 & 1 # & all conditions

        self.FILTERED_DF                  = df[~condition]
        df                                = df[condition]
        self.DATA_ROWS, self.DATA_COLUMNS = df.shape
        self.DATA_M, self.DATA_NX         = df.shape
        logi('Cleaned %d samples ' % (self.RAW_M - self.DATA_M))
        return df

    def filter(self, df):
        # list of columns/features in the output dataframe
        column_select = ['truthZ','uncM']

        self.DATA_HEADER = column_select
        logi('Filtering data removing these columns %s' % column_select)
        df = df[column_select]
        return df

    def assertShapes(self):
        assert(self.RAW_DF.shape  == (self.RAW_ROWS  , self.RAW_COLUMNS ))
        assert(self.RAW_NP.shape  == (self.RAW_ROWS  , self.RAW_COLUMNS ))
        assert(self.DATA_NP.shape == (self.DATA_NX   , self.DATA_M      ))


