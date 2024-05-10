"""Upload files to SWIFT storage."""

import aiohttp
import aiohttp_retry
import xarray as xr

async def get_client(**kwargs):

    retry_options = aiohttp_retry.ExponentialRetry(
            attempts=3,
            exceptions={OSError, aiohttp.ServerDisconnectedError})
    retry_client = aiohttp_retry.RetryClient(raise_for_status=False, retry_options=retry_options)
    return retry_client

ds = xr.open_zarr("data/converted/trajectory.zarr")

try:
    ds.to_zarr("swift://swift.dkrz.de/dkrz_a88749b4-3884-49bb-8c65-76571c660914/trajectories/NAtl_925hPa.zarr", storage_options={"get_client": get_client}, mode="w")
except aiohttp.client_exceptions.ClientResponseError:
    print("Please check that OS_STORAGE_URL and OS_AUTH_TOKEN are set. Is the container already created?")