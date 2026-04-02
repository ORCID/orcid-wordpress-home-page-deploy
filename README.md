# Orcid WordPress Homepage Deployment

The purpose of this repository is to provide a straightforward method for both technical and non-technical users to deploy a clone of a WordPress post from https://orcidhomepage1.wpenginepowered.com/

## Homepage QA Deploy

Deploy the info.qa.orcid.org page on qa.orcid.org:

  -  Navigate to [Homepage QA Deploy](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/qa-deploy.yml)
  -  Click on "Run workflow"
  -  Select `Create a versioned artifact? = false`  and select the WordPress post that needs to be deployed (default is `25422`)
<img width="340" alt="image" src="https://github.com/ORCID/orcid-wordpress-home-page-deploy/assets/2119626/77e361a1-c683-4dda-ae83-6840d1467ae3">


## Homepage PROD Deploy

1.  Before deploying it to prod run a QA release that will create a versioned artifact
    - Navigate to [Homepage QA Deploy](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/qa-deploy.yml)
    - Click on "Run workflow"
    - Select `Create a versioned artifact? = true` and select the Prod WordPress post that needs to be deployed (default is 25422)
    - The created artifact is now published on qa.orcid.org. Please make sure with your team that this is approved for production before continuing. 

2. Deploy the version of this artifact to production
   - Navigate to [Homepage PROD Deploy](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/prod-deploy.yml)
   - Click on "Run workflow"
   - And run the latest version displayed on the [(release list page) ](https://github.com/ORCID/orcid-wordpress-home-page-deploy/releases).
   - The release will occur in three stages: a release to QA (for a final review), a release to the production-fallback machine, and a release to the production machine.
   - Before the fallback-production and production releases, you will be asked to review the previous release. You will need to approve this to continue. As show on the following image:
   - <img width="1416" alt="image" src="https://github.com/ORCID/orcid-wordpress-home-page-deploy/assets/2119626/eb120157-8ae3-4712-9cca-6eef01c0aa5a">


3. Document the date this release version was put up on production
   - Navigate to the release list version, click "Edit," and add a note about the release date for the production version. This information will provide better context for identifying the last stable version if a rollback is necessary. <img width="1132" alt="image" src="https://github.com/ORCID/orcid-wordpress-home-page-deploy/assets/2119626/fca8b496-fc47-43b6-8998-0346b284ae95">




## Rollback Deployment

   - Navigate to [Homepage PROD Deploy](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/prod-deploy.yml)
   - Click on "Run workflow"
   - And run the version you want to deploy to production [(see the full list on versioned artifacts apps) ](https://github.com/ORCID/orcid-wordpress-home-page-deploy/releases)

## Developers

#### Cloning WordPress Locally:

1- Create a new virtual environment

In the project directory:

```
python3 -m venv myenv
```

2- Activate the environment

```
source myenv/bin/activate  # macOS/Linux
```
or

```
myenv\Scripts\activate     # Windows
```

3- Install Python dependencies

```
pip install -r requirements.txt
```

4- Install Node dependencies (required for CSS minification, asset fingerprinting, and module bundling)

```
npm install
```


Running the following command will run the cloning process on your local environment (This won't deploy to S3, commit, or do GitHub releases)

```
export GITHUB_OUTPUT="./dist/output"     
export GITHUB_STEP_SUMMARY="./dist/summary"
python3 wordpress-cloning-main.py STAGE 25422 orcidhomepage1 377e0ed1 --dry-run
```

#### Are you adding a new CSS stylesheet to WordPress?

If you add a new stylesheet to WordPress, you will need to update the file [wordpress-cloning-css-script.py](https://github.com/ORCID/orcid-wordpress-home-page-deploy/blob/main/wordpress-cloning-css-script.py). This will make the cloning script to include the new stylesheet in the css output file.

#### Are you adding new JavaScript (plugin scripts) to WordPress?

If the WordPress page starts depending on a **new plugin script** (or any other new `.js` file), you must add it to the JS cloning pipeline so it ends up in `dist/wordpress-homepage.js`.

- **Update**: Add the script URL(s) to the `js_urls` list in [`wordpress-cloning-js-script.py`](https://github.com/ORCID/orcid-wordpress-home-page-deploy/blob/main/wordpress-cloning-js-script.py).
- **Order matters**: Keep dependency order the same as WordPress (e.g., jQuery first, then jQuery plugins, then the plugin “view” script).
- **Verify**: Run the local clone command (see “Cloning WordPress Locally”) and confirm the new script appears in `dist/wordpress-homepage.js` (search for `/* JS from ... */`).

Notes:
- The generated HTML loads `wordpress-homepage.js` with `defer`, so DOM-dependent scripts run after the page markup is parsed.
- Some WordPress plugin scripts ship as ESM builds that import `@wordpress/*` packages. These cannot be concatenated into `dist/wordpress-homepage.js` (classic script) without breaking the page. For those scripts, the pipeline downloads a separate module entry and bundles it (via `esbuild`) into `dist/wordpress-homepage-modules.js`, which is loaded with `<script type="module">`.

