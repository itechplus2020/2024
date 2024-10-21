# File: download_github_folder.py
import requests
import os

def download_github_folder(owner, repo, folder_path, branch="main"):
    """
    Downloads all files from a folder in a GitHub repository.
    
    Parameters:
    - owner: GitHub username or organization.
    - repo: Repository name.
    - folder_path: Path to the folder in the repository.
    - branch: Branch name (default is 'main').
    """
    # GitHub API URL to get the contents of the folder
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_path}?ref={branch}"

    # Send GET request to GitHub API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        contents = response.json()

        # Create the local folder to save the downloaded files
        os.makedirs(folder_path, exist_ok=True)

        # Loop through each item in the folder
        for item in contents:
            if item['type'] == 'file':  # Ensure it is a file
                file_url = item['download_url']  # Get the raw file URL
                file_name = item['name']  # Get the file name

                # Download the file
                file_response = requests.get(file_url)

                # Save the file locally
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)

                print(f"Downloaded {file_name}")
    else:
        print(f"Failed to retrieve folder contents. Status code: {response.status_code}")
