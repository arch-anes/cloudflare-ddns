# Cloudflare DDNS

A dynamic Cloudflare DDNS client with round-robin DNS, multiple zones and
variable refresh rate and Docker Secret supports.

## Environment variables

- `CF_API_KEY`: Cloudflare API token 
- `CF_API_KEY_FILE`: Cloudflare API token stored in a file (for Docker Secret)
- `ZONES`: Cloudflare zones separated with commas (ex: `example.com, example.ca`)
- `DELAY`: delay between each check (default `300` seconds)
- `UNIQUE`: delete all other root A records except this one (default `no`)

## Docker image

Pull the project's Docker image at `archanes/cloudflare-ddns`.

## Creating a Cloudflare API token

To create a CloudFlare API token for your DNS zone go to https://dash.cloudflare.com/profile/api-tokens and follow these steps:

1. Click Create Token
2. Provide the token a name, for example, `cloudflare-ddns`
3. Grant the token the following permissions:
    * Zone - Zone Settings - Read
    * Zone - Zone - Read
    * Zone - DNS - Edit
4. Set the zone resources to:
    * Include - All zones
