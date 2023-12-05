# MANIFEST GENERATOR

This tool is a fast replacement tool to generate manifests using Syft. This tool can be helpful to add it to a CI/CD in order to generate mupltiple manifests quickly.

The working is pretty simple:

There are two ways of generating the manifests. We either use a YAML file with all the different repos (see tools.yml as example):

    python3 manifest_generator.py -f <filename.yml>

Or we can directly generate the manifests for a single repo (although using Syft will do exactly the same):

    python3 manifest_generator.py -r <repo_link> -n <product_name>


# Disclaimer
This is a work in progress tool. Use under your own responsibility.
