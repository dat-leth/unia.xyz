# unia.xyz
[![Netlify Status](https://api.netlify.com/api/v1/badges/d1c85854-db0d-4443-bb71-670d13fa61b2/deploy-status)](https://app.netlify.com/sites/unia/deploys)

A simple URL shortener from unia.xyz to University of Augsburg's webpages hosted on [Netlify](https://www.netlify.com/) and using Netlify's speedy CDN-based [Redirects API](https://docs.netlify.com/routing/redirects/).

# Add or update short URLs
Modify `redirects.toml` and run `python build.py`. The build script will then parse the routing rules and generate the webpage and redirects file for Netlify.

1. Fork this repository.
2. Make changes as necessary.
3. Commit and push changes to your own fork.
4. Open a Pull Request on GitHub.

If your Pull Request is accepted and merged into `main`, all changes will be automagically deployed and you will be able to see your changes on unia.xyz within minutes.

# Build script
Quickly hacked together, but it works. And it works in the following way:

- Parse `./redirects.toml`.
- Fetch Base CSS from jsdelivr. We are using [new.css](https://newcss.net).
- Minify Custom CSS with rcssmin.
- Create output folder `./out/` if not exists.
- Generate `./out/index.html` using Jinja2.
- Generate `./out/_redirects` using Jinja2.