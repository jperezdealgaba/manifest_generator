import argparse
import os
import sys
import shutil
import subprocess
import yaml
import json

from git import Repo

def clone_repo(link, product_name):
    print(f"Cloning {link}")
    try:
        Repo.clone_from(link, product_name)
    except Exception as e:
        print(f"Error cloning repository: {e}")

def generate_manifests(product_name):
    print("Generating manifest")
    try:
        subprocess.run(["syft", product_name ,"-o", "syft-json", "--file", os.path.join("results",product_name)])
    except Exception as e:
        print(f"Error generating manifest")

def delete_artifacts(product_name):
    # We delete the folder
    shutil.rmtree(product_name)

def main():
    print("Starting Manifesting Tool")

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="filename",
                        help="Define file with list of repos", metavar="FILE")
    parser.add_argument("-r", dest="repo",
                        help="Define repo to get manifests", metavar="FILE")
    parser.add_argument("-n", dest="name",
                        help="Name of product", metavar="FILE")
    parser.add_argument("-o", dest="output_file",
                        help="Define the name for the output file", metavar="FILE")

    args = parser.parse_args()

    if args.filename and args.repo:
        print("Please, select either -f or -r but not both at the same time. Exiting proces...")
        sys.exit(1)

    if args.filename:
        print(f"The file {args.filename} will be used to generate the manifests")
    elif args.repo:
        if args.name is None:
            print("Please, use -n with -r parameter to specify the name of the product")
            sys.exit(1)
        print(f"The repository {args.repo} will be used to generate the manifests")
    else:
        print("No file or repo was provided to generate the manifests. Exiting...")

    if args.repo:
        clone_repo(args.repo, args.name)
        generate_manifests(args.name)
        delete_artifacts(args.name)

    elif args.filename:
        if not os.path.isfile(args.filename):
            print("Provided file doesn't exist. Exiting...")
            sys.exit(1)

        # We convert the file to JSON to operate in an easier way
        with open(args.filename, 'r') as file:
            tools_file = yaml.safe_load(file)

            for key,value in tools_file.items():
                for product_name, repo_link in value.items():
                    product_name = key + "-" + product_name
                    clone_repo(repo_link, product_name)
                    generate_manifests(product_name)
                    delete_artifacts(product_name)


if __name__ == "__main__":
    main()