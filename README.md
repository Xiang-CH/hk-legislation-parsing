# Hong Kong Legislation Processing

This repository contains the code for processing / parsing Hong Kong legislation. The parsed information are suited for building semantic databases.

## Steps

0. Create a virtual environment and activate it. Install `uv` first.
    ```bash
    uv venv --python 3.12 --seed
    source .venv/bin/activate
    ```

1. Download the source files from the [data.gov.hk](https://data.gov.hk/en-data/dataset/hk-doj-hkel-legislation-current) website.
    ```bash
    ./download.sh
    ```
    - The source files are downloaded to the `raw_legislation` directory.
    - This will take a few minutes to download all the files.

* skip to step 5 if you don't want to parse the references with LLM.

3. Install vllm
    ```bash
    uv pip install vllm --torch-backend=auto
    ```

4. Run the `serve.py` script to start the llm inference server.
    ```bash
    ./serve.sh
    ```
    - This will start the server on port 5000.
    - The server is OpenAI-compatible, so you can use any OpenAI-compatible client to interact with it.

5. Run the `parse.py` script to parse the source files.
    ```bash
    uv pip install -r requirements.txt
    python parse.py
    ```
    - The parsed files are saved to the `parsed_data` directory.