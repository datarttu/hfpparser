# Parse raw HFP data

Parse a raw text file where each line consists of [HFP](https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/) topic string and JSON payload.
Save as a CSV file.

## Usage

```
python path/to/parse_hfp1_vp.py path/to/raw_hfp_file.txt output_csv_file.csv
```

## TODO features

- HFP v1 vehicle positions parsing
- Handle missing input fields
- Handle erroneous lines
- Select output fields
- Logging summary
- HFP v2
  - Vehicle positions
  - TLP
