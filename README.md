# Hong Kong Legislation Processing

This repository contains the code for processing / parsing Hong Kong legislation. The parsed information are suited for building semantic databases.

## Steps

1. Download the source files from the [data.gov.hk](https://data.gov.hk/en-data/dataset/hk-doj-hkel-legislation-current) website.
    ```bash
    ./download.sh
    ```
    - The source files are downloaded to the `raw_legislation` directory.
    - This will take a few minutes to download all the files.
2. Run the `parse.py` script to parse the source files.
    ```bash
    pip install -r requirements.txt
    python parse.py
    ```
    - The parsed files are saved to the `parsed_data` directory.