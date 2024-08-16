from sqlalchemy import create_engine
import pandas as pd

def get_engine():
    username = 'ouni'
    password = '12345'
    host = 'localhost'
    database = 'restaurant_management'
    return create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

def load_data(engine):
    query = 'SELECT * FROM detections'
    df = pd.read_sql(query, engine)
    df['detection_time'] = pd.to_datetime(df['detection_time'])
    return df



def load_data_2(engine):
    query = 'SELECT * FROM face_recognition_events'
    df = pd.read_sql(query, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df