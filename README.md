# Orcid WordPress home page deployment

The goal of this repository ID is to provide a simple and quick method for tech and non-technical users to quickly deploy a clone of a WordPress page ID from https://info.qa.orcid.org/ and https://info.orcid.org/


## Homepage update workflow: 

1. Make all required updates on WordPress QA (https://info.qa.orcid.org/)
2. Follow the QA Deployment steps described below once the updates are done and tested on WordPress. 
3. Follow the PROD Deployment steps described below once the updates are done and tested on qa.orcid.org. 
4. Follow the Rollback PROD Deployment if something goes wrong or if a previous version is 


## QA Deployment

- Navigate to [Clone And QA Deploy WordPress Post](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/clone-post.yml)
- Click on "Run workflow"
  - select environment = `QA` and select the WordPress page that needs to be deployed (default is `25163`) 

  - <img width="327" alt="image" src="https://github.com/ORCID/orcid-wordpress-home-page-deploy/assets/2119626/9ace3faa-5a6f-42d3-803e-af65e196d1a8">



## Prod Deployment

1. Verify info.orcid.org clone on QA:
    - Navigate to [Clone And QA Deploy WordPress Post](https://github.com/ORCID/orcid-wordpress-home-page-deploy/actions/workflows/clone-post.yml)
    - Click on "Run workflow"
    - select environment = `QA` and select the WordPress page that needs to be deployed (default is `25163`) 
    - <img width="327" alt="image" src="https://github.com/ORCID/orcid-wordpress-home-page-deploy/assets/2119626/9ace3faa-5a6f-42d3-803e-af65e196d1a8">

2. Update the fallback S3 bucket
    - Verify the default machine is working as expected: navigate to `orcid.org?home-page-force=s3-a`.
    - Navigate to the GitHub action <WIP>
    - Click on "Run workflow"
    - Select environment = `prod-s3-b` and select the GitHub version to release.
      - Please verify the version to be deployed has already been checked and approved on QA.  
      - See all available versions [here](https://github.com/ORCID/orcid-wordpress-home-page-deploy/releases).


3. Update the default S3 bucket
    - Verify the fallback machine is working as expected: navigate to `orcid.org?home-page-force=s3-b`. 
    - Navigate to the GitHub action <WIP>
    - Click on "Run workflow"
    - Select environment = `prod-s3-a` and select the GitHub version to release.
      - Please verify the version to be deployed has already been checked and approved on QA.  
      - See all available versions [here](https://github.com/ORCID/orcid-wordpress-home-page-deploy/releases).


## Rollback deploy

- WIP
  