# Retail Data Pipeline

This repository contains an AI-powered ETL pipeline for processing retail order data.

## Features
- **Modular Design**: Separate functions for Loading, Cleaning, Transforming, and Saving.
- **Data Quality**: Automatic deduplication and null imputation.
- **Performance**: Early filtering of invalid records.
- **Logging**: Full execution traceability in `pipeline.log`.
- **Testing**: Automated test suite using `pytest`.

## Project Structure
- `pipeline/main.py`: Core ETL logic.
- `pipeline/test_pipeline.py`: Unit tests.
- `pipeline/requirements.txt`: Python dependencies.
- `.github/workflows/`: CI/CD automation.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r pipeline/requirements.txt
   ```
2. Place your `orders.csv` in the root directory.
3. Execute the pipeline:
   ```bash
   python3 pipeline/main.py
   ```

## How to Test
Run the following command:
```bash
python3 -m pytest pipeline/test_pipeline.py
```
