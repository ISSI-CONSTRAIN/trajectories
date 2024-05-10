# Trajectories

## Access

```python
>>> import intake
>>> cat = intake.open_catalog("https://raw.githubusercontent.com/ISSI-CONSTRAIN/trajectories/main/catalog.yaml")
>>> ds = cat['NAtl_925hPa'].to_dask()
<xarray.Dataset> Size: 1GB
Dimensions:     (trajectory: 385704, obs: 180)
Coordinates:
    lat         (trajectory, obs) float32 278MB dask.array<chunksize=(24107, 12), meta=np.ndarray>
    lon         (trajectory, obs) float32 278MB dask.array<chunksize=(24107, 12), meta=np.ndarray>
  * obs         (obs) int64 1kB 0 1 2 3 4 5 6 7 ... 173 174 175 176 177 178 179
  * trajectory  (trajectory) float32 2MB 1.0 2.0 3.0 ... 3.857e+05 3.857e+05
Data variables:
    local_time  (trajectory, obs) float32 278MB dask.array<chunksize=(24107, 12), meta=np.ndarray>
    time        (trajectory, obs) datetime64[ns] 555MB dask.array<chunksize=(24107, 12), meta=np.ndarray>
Attributes:
    featureType:  trajectory
```
