import pandas as pd


class DataStream:
    def __init__(self):
        raise NotImplemented

    def __next__(self):
        raise NotImplemented


class PandasDataStream(DataStream):
    def __init__(self, df_data: pd.DataFrame, t: int=0):
        self.df_data = df_data
        self.ids_asset = list(self.df_data.columns)
        self.t = 0
    
    def __next__(self):
        row = self.df_data.iloc[self.t]
        self.t += 1
        return row


class LiveDataStream(DataStream):
    def __init__(self):
        pass
    
    def __next__(self):
        pass