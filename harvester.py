name: Swell forecast

on:
  workflow_dispatch:
  schedule:
    - cron: "45 10 * * *"
    - cron: "45 22 * * *"

permissions:
  contents: write

concurrency:
  group: forecast
  cancel-in-progress: false

jobs:
  harvest:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - name: Get the repository files
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install libraries
        run: pip install --quiet ecmwf-opendata eccodes numpy requests

      - name: Run the harvester
        run: python harvester.py

      - name: Save results back to the repository
        run: |
          git config user.name "swell-bot"
          git config user.email "actions@users.noreply.github.com"
          git add docs/
          git commit -m "Forecast update $(date -u +'%Y-%m-%d %H:%MZ')" || echo "No changes to commit"
          git push
