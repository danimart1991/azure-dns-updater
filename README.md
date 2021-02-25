[![GitHub release (latest by date)](https://img.shields.io/github/v/release/danimart1991/azure-dns-updater)](https://github.com/danimart1991/azure-dns-updater/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/danimart1991/azure-dns-updater)](https://github.com/danimart1991/azure-dns-updater/commits)
[![License](https://img.shields.io/github/license/danimart1991/azure-dns-updater)](https://github.com/danimart1991/azure-dns-updater/blob/main/LICENSE)

[![Docker Cloud Build](https://img.shields.io/docker/cloud/build/danimart1991/azure-dns-updater)](https://hub.docker.com/r/danimart1991/azure-dns-updater)
[![Docker Pulls](https://img.shields.io/docker/pulls/danimart1991/azure-dns-updater)](https://hub.docker.com/r/danimart1991/azure-dns-updater)
[![Docker Stars](https://img.shields.io/docker/stars/danimart1991/azure-dns-updater)](https://hub.docker.com/r/danimart1991/azure-dns-updater)

[![Tip Me via PayPal](https://img.shields.io/badge/PayPal-tip%20me-blue?logo=paypal&style=flat)](https://www.paypal.me/danimart1991)
[![Sponsor Me via GitHub](https://img.shields.io/badge/GitHub-sponsor%20me-blue?logo=github&style=flat)](https://github.com/sponsors/danimart1991)

# Azure DNS Updater

Azure Dynamic DNS updater based on Python (Docker Included)

Based on [AzureDynDns](https://github.com/evkapsal/AzureDynDns) by [@evkapsal](https://github.com/evkapsal)

## Requirements

[Microsoft Azure Portal](https://portal.azure.com/):

- Create an _App Service Domain_.
- Activate _DNS Zone_ for that domain.
- Create all _DNS Record Sets_ you need to be updated (recommend to set the current server `IP` as value).

From this page, you could get.

![Azure DNS Zone example](https://github.com/danimart1991/azure-dns-updater/blob/main/docs/images/dns-zone.png?raw=true)

- SUBSCRIPTION_ID: `38926cdc-fcb2-4e67-bed8-8e619ab2d5a4`.
- DOMAIN: `foo.com`.
- RESOURCE_GROUP: `default-web-northeurope`.
- RECORD_SET: `*,@`.

In [Azure Cloud Shell](https://docs.microsoft.com/en-us/azure/cloud-shell/overview) execute:

```powershell
$ az ad sp create-for-rbac -n "azure-dns-updater" --scopes /subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Network/dnszones/{DOMAIN}

Example:

$ az ad sp create-for-rbac -n "azure-dns-updater" --scopes /subscriptions/38926cdc-fcb2-4e67-bed8-8e619ab2d5a4/resourceGroups/default-web-northeurope/providers/Microsoft.Network/dnszones/foo.com

Changing "azure-dns-updater" to a valid URI of "http://azure-dns-updater", which is the required format used for service principal names
Creating a role assignment under the scope of "/subscriptions/38926cdc-fcb2-4e67-bed8-8e619ab2d5a4/resourceGroups/default-web-northeurope/providers/Microsoft.Network/dnszones/foo.com"
  Retrying role assignment creation: 1/36
{
  "appId": "ad5931a6-3f16-4bdd-ae95-5943a8ddbf79",
  "displayName": "azure-dns-updater-foo",
  "name": "http://azure-dns-updater-foo",
  "password": "AeN~+~12ufhGH1yfh210vhq91j231SDGjP",
  "tenant": "a454b7b6-7014-4e65-b114-d48a83355acd"
}
```

Annotate these variables too:

- APP_ID: `ad5931a6-3f16-4bdd-ae95-5943a8ddbf79`.
- TENANT_ID: `a454b7b6-7014-4e65-b114-d48a83355acd`
- APP_SECRET: `AeN~+~12ufhGH1yfh210vhq91j231SDGjP`

Now, you have all the necessary to make que **Azure DNS Updater** works.

## Usage

There are two methods to use **Azure DNS Updater**: _Python_ or _Docker_.

Both need the variables previously obtained plus `INTERVAL`, that defines the number of seconds between each check.

`RECORD_SET` variable accepts one _DNS Record_ or a list of _DNS Records_ separated by comma.

### Python

Download the `azure-dns-updater.py` and load it using this command:

```bash
$ python .\azure-dns-updater.py
\ --APP_ID="ad5931a6-3f16-4bdd-ae95-5943a8ddbf79"
\ --TENANT_ID="a454b7b6-7014-4e65-b114-d48a83355acd"
\ --SUBSCRIPTION_ID="38926cdc-fcb2-4e67-bed8-8e619ab2d5a4"
\ --APP_SECRET="AeN~+~12ufhGH1yfh210vhq91j231SDGjP"
\ --RECORD_SET="*,@"
\ --DOMAIN="foo.com"
\ --RESOURCE_GROUP="default-web-northeurope"
\ --INTERVAL=300
```

### Docker

```bash
$ docker run -d
\ --name="Azure_DNS_Updater"
\ --hostname=azure_dns_updater
\ --restart=always
\ -e TZ="Europe/Madrid"
\ -e APP_ID="ad5931a6-3f16-4bdd-ae95-5943a8ddbf79"
\ -e TENANT_ID="a454b7b6-7014-4e65-b114-d48a83355acd"
\ -e SUBSCRIPTION_ID="38926cdc-fcb2-4e67-bed8-8e619ab2d5a4"
\ -e APP_SECRET="AeN~+~12ufhGH1yfh210vhq91j231SDGjP"
\ -e RECORD_SET="*,@"
\ -e DOMAIN="foo.com"
\ -e RESOURCE_GROUP="default-web-northeurope"
\ -e INTERVAL=300
\ danimart1991/azure-dns-updater:latest
```

> `name`, `hostname`, `restart` and `-e TZ="Europe/Madrid"` are optional or could be changed to your behavior.
