# PrevedereAPI

PrevedereAPI provides the ability to access the API and retrieve indicator series data, as well as other information.
for full documentation, go to the [Prevedere API](https://api.prevedere.com/metadata/).

# Installation
`pip install git+https://github.com/prevedere/prevedere_api`

# Use
```
import prevedere
api_key = "xyz123"
provider = "provider_a"
provider_id = "a123"

p = prevedere.Api(api_key)
p.indicator_series(provider, provider_id)
```
