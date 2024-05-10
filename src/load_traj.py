"""Post-process trajectories"""
import tqdm
import numpy as np
import pandas as pd
import xarray as xr
path = "data/incoming/NAtl_Trajectories_Mid_Start_925hPa_1hrLocalInterp"
file_fmt = "NAtl_Trajectories_Mid_Start_925hPa_1hrLocalInterp_{year}.nc"

def ydh_to_datetime(ds):
    """Convert year, day, hour to datetime"""
    years = ds['year_UTC'].values.flatten()
    days = ds['day_UTC'].values.flatten()
    hours = ds['hour_UTC'].values.flatten()
    datetime = pd.to_datetime(years * 1000 + days, format='%Y%j') + pd.to_timedelta(hours, unit='h')
    return datetime.to_numpy('<M8[ns]').reshape(ds['year_UTC'].shape)

datasets = []
for year in tqdm.trange(2007, 2023):
    ds = xr.open_dataset(f"{path}/{file_fmt.format(year=year)}")
    dates = ydh_to_datetime(ds)
    
    ds_new = xr.Dataset()
    ds_new['trajectory'] = xr.DataArray(ds['Trajectory_N'], dims=['trajectory'])
    ds_new['trajectory'].attrs['cf_role'] = 'trajectory_id'
    ds_new['trajectory'].attrs['long_name'] = 'trajectory number'
    ds_new['obs'] = xr.DataArray(np.arange(len(ds['hour_local_time'])), dims=['obs'])
    ds_new['time'] = xr.DataArray(dates, dims=['obs', 'trajectory'])
    ds_new['lat'] = xr.DataArray(ds['latitude'], dims=['obs', 'trajectory'])
    ds_new['lon'] = xr.DataArray(ds['longitude'], dims=['obs', 'trajectory'])
    ds_new['local_time'] = xr.DataArray(ds['hour_local_time'], dims=['obs', 'trajectory'])
    ds_new['local_time'].attrs['coordinates'] = "obs lon lat"
    ds_new.attrs['featureType'] = 'trajectory'

    datasets.append(ds_new)

ds_out = xr.concat(datasets, dim='trajectory').transpose()

ds_out.to_zarr('data/converted/trajectory.zarr', encoding={'time': {'_FillValue':-999}})