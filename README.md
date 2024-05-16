# Orcid WordPress Homepage Deployment

The purpose of this repository is to provide a straightforward method for both technical and non-technical users to deploy a clone of a WordPress page from https://info.qa.orcid.org/ and https://info.orcid.org/.

## Homepage Update Workflow:

1. Make all required updates on WordPress STAGIN (https://info.qa.orcid.org/).
2. Follow the QA Deployment steps described below once the updates are done and tested on WordPress.
3. Follow the PROD Deployment steps described below once the updates are done and tested on qa.orcid.org.
4. Follow the Rollback PROD Deployment if something goes wrong or a previous version is needed.

## Homepage QA Deploy

- Navigate to [Homepage QA Deploy](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/qa-deploy.yml)
- Click on "Run workflow"
  - Select environment = `STAGIN` and select the WordPress page that needs to be deployed (default is `25163`)
<img src="https://github.com/ORCID/orcid-wordpress-home-page-deploy/assets/2119626/4c42594c-94a6-44fb-870a-624c9faf2b2a" height="200">

```
Note: 
TODO: Provide more info to users who might not know how to get the page id 
from the WordPress page they want to publish. 
```

## Homepage PROD Deploy

1. Verify the info.orcid.org page on qa.orcid.org before deploying it to prod:
    - Navigate to [Homepage QA Deploy](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/qa-deploy.yml)
    - Click on "Run workflow"
    - Select environment = `PROD` and select the Prod WordPress page that needs to be deployed

2. Deploy the info.orcid.org page to prod:
   - Navigate to [Homepage PROD Deploy](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/prod-deploy.yml)
   - -- WIP 👷‍♂️ ---


## Rollback Deployment

-- WIP 👷‍♂️ ---

## Developers

#### Cloning WordPress:

Running the following command will run the cloning process on your local environment (This won't deploy to S3, commit, or do GitHub releases)

```
python3 wordpress-cloning-main.py qa 25163 orcidstaging fb8dd998
```

If changes need to be committed run (This won't deploy to S3, or create a GitHub releases)

```
python3 wordpress-cloning-main.py qa 25163 orcidstaging fb8dd998 --commit
```
-- WIP 👷‍♂️ ---
