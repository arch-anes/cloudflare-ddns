# Cloudflare DDNS

A dynamic Cloudflare DDNS client with round-robin DNS, multiple zones and
variable refresh rate and Docker Secret supports.

## Environment variables

- `CF_API_KEY`: Cloudflare API token 
- `CF_API_KEY_FILE`: Cloudflare API token stored in a file (for Docker Secret)
- `ZONES`: Cloudflare zones separated with commas (ex: `example.com, example.ca`)
- `DELAY`: delay between each check (default `300` seconds)
