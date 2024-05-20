<p align="center">
    <img width="214" height="42" src="./ui/static/assets/logo-red.png" alt="paradrop">
</p>

<h2 align="center">Cybersecurity Asset Management</h2>

[![Demo][demo_url_img]][demo_url]
[![Admin Docs][admin_doc_img]][admin_doc_url]
[![API Docs][api_doc_img]][api_doc_url]
[![License][repo_license_img]][repo_license_url]

paradrop is an open source, cybersecurity asset management tool that collects operating system information, including configurations, security settings, resource metrics, and installed and running software. The paradrop UI provides accessible, searchable, and filterable views on the data the paradrop agent collects from supported platforms. Our end goal is to build an easily customizable solution that provides methods to automate United States Government challenges around System Security Plans (SSP), Authorization to Operate (ATO), and Software Bill of Materials (SBOMs).

## ⚡️ Quick start

> 🐳  **Docker Compose** Method  
> First install NodeJS 18.x, Make, cURL and Docker

```bash
make local
# Optional: Load test / example demo data
make seed
```

> 🖥️  **Vagrant** Method

```bash
vagrant up
```

Go to https://localhost:8443/ui/

## 📖 Docs

**Main Docs**: https://demo.paradrop.io/docs

**Swagger API Docs**: https://demo.paradrop.io/apidocs/

## ⚙️ Development

### `Opensearch`
Elasticsearch compatible database also works

> 🔔 Requires cURL, Make and Docker

```bash
make elk
```

### `api` 
Python Flask API

> 🔔 Requires Python >=3.10.

```bash
make api
```

### `ui`
Bootstrap 5 & CoreUI Static HTML/CSS/JS

> 🔔 Requires Python 3.x or serve static assets from build UI directory.

```bash
make ui
```

### `agent`
Golang Agent (Windows/Linux/Darwin/amd64/arm64 supported)
> 🔔 Requires Go >=1.22 

```bash
cd agent
make
```


## 🚧 Project Status

The paradrop tool is early in development, and we're still building more documentation to help you deploy across different architectures, accelerate iterating on changes, and enhance security controls this year.

We hope you star this project, engage with us, and check back when you can for further updates coming soon.


## ⚠️ License

[`paradrop`][repo_url] is free and open source software licensed under 
the [GNU General Public License v3.0][repo_license_url]


<!-- Links -->
[admin_doc_url]: https://demo.paradrop.io/docs

[repo_license_url]: https://github.com/Metrostar/paradrop/blob/main/COPYING

[repo_url]: https://github.com/MetroStar/paradrop

[repo_license_img]: https://img.shields.io/badge/license-GPLv3-purple?style=for-the-badge&logo=none

[admin_doc_img]: https://img.shields.io/badge/admin_docs-click_here-blue?style=for-the-badge&logo=none

[api_doc_img]: https://img.shields.io/badge/api_docs-click_here-pink?style=for-the-badge&logo=none

[api_doc_url]: https://demo.paradrop.io/apidocs/

[demo_url]: https://demo.paradrop.io/ui/login/

[demo_url_img]: https://img.shields.io/badge/demo-click_here-red?style=for-the-badge&logo=none