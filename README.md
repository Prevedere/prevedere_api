# prevedere-api

prevedere-api provides the ability to access retrieve indicator series data, as well as other information.
For full documentation, go to the [Prevedere Swagger API GUI](https://api.prevedere.com/swagger) page.

# Installation
`pip install prevedere-api`

# Use
```
import prevedere

api_key = "xyz123"
provider = "provider_a"
provider_id = "a123"

p = prevedere.Api(api_key)
p.indicator_series(provider, provider_id)
```
