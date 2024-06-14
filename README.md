
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
      <a href="#getting-started">Steps for running the project:</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Run</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Steps for running the project:

This is an example of how you may give instructions on setting up the project locally.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
1. Create a project in [https://console.developers.google.com](https://console.developers.google.com)
2. Visit [Custom Search API](https://console.developers.google.com/apis/library/customsearch.googleapis.com) and enable 'Custom search API' for the project.
3. Go to [Credentials](https://console.developers.google.com/apis/credentials) and generate API_KEY credentials.
4. Get your CX from https://cse.google.com/cse/all

### Installation

Follow these steps to bring up the project:

1. Clone the repo
   ```sh
   git@github.com:ali-sefidmouy/Google-Search-Image.git
   ```
2. Create virtual environment and activate it:
   ```sh
   $ virtualenv venv
   $ source venv/bin/activate
   ```
3. Install requirements using pip 
   ```sh
   pip install -r requirements.txt
   ```
4. Provide environment variables like `API_KEY`, `CX`, Database configurations in `.env` file

   ```sh
   # Google Custom Search API variables
   KEY = 'yourapikey'
   CX = 'yourcx'
   GOOGLE_API_VERSION = 'v1'

   # DB variables
   DB_NAME=dbname
   ...
   ```
6. Bring up PostgreSQL container with Docker Compose
   ```sh
   docker-compose up -d
   ```

<!-- USAGE EXAMPLES -->
## Run
Change directory to src/ and run the project:
```sh
$ python image_search.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
