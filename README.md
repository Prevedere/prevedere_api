# prevedere-api

prevedere-api is a simple API for making HTTP requests to the Prevedere application. Requires an API key.
For full documentation, go to the [Prevedere Swagger API GUI](https://api.prevedere.com/swagger).

# Installation
`pip install prevedere-api`

# Use

## Authentication
There is a file called `prevedere_api.ini.example` that can be used to store your API key. To use it, make a copy of the file, remove `.example` from the filename, and replace the API key in the file with your own. If you cannot find the file, initializing `prevedere.Api()` will produce the expected location of the .ini file.
Once completed, you will no longer have to enter in your API key when creating a connection to the Prevedere API.
```
from prevedere import Api
p = Api()
```

## Endpoints
- `indicator`: returns basic information about an indicator.
- `indicator_series`: returns the data for an indicator.
- `correlation`: calculates Pearson's r and other statistics at different offsets between an endogenous and exogenous indicator.
- `raw_model`: returns all information about a forecast model.
- `forecast`: returns historical fit and forecasted values of a forecast model.
- `workbench`: returns the indicators used in a workbench.

## Example
```
import prevedere

api_key = "xyz123"
provider = "provider_a"
provider_id = "a123"

p = prevedere.Api(api_key)
p.indicator_series(provider, provider_id)
```
