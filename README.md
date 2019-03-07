# prevedere-api

prevedere-api is a simple API for making HTTP requests to the Prevedere application. Requires an API key.
For full documentation, go to the [Prevedere Swagger API GUI](https://api.prevedere.com/swagger).

# Installation
`pip install prevedere-api`

# Use

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
