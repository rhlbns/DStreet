from datetime import datetime, timedelta
import pandas as pd
import json
import os

class Helper:
    def __init__(self):
        self.load_scrip_master()

    def load_scrip_master(self):
        path = os.path.join('resources', 'angelone', 'OpenAPIScripMaster.json')
        with open(path, 'r') as f:
            scrip_master = json.loads(f.read())
        self.scrip_master = pd.DataFrame(scrip_master)

    def get_scrip_token(self, scrip):
        scrip += '-EQ'
        vals = self.scrip_master[self.scrip_master.symbol==scrip].token.values
        if len(vals) == 1:
            return vals[0]
        raise ValueError ('invalid scrip name', scrip)

    def convert_to_default_dt_format(self, dt_str):
        # 2022-09-14T09:15:00+05:30
        dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S+05:30')
        dt_str_new = dt.strftime('%Y-%m-%d %H:%M')
        return dt_str_new

    def convert_dt_to_str(self, dt):
        dt_str = dt.strftime('%Y-%m-%d %H:%M')
        return dt_str

    def convert_str_to_dt(self, dt_str):
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        return dt
