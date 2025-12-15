import argparse
import csv
import sys
import os
from collections import defaultdict

try:
    from tabulate import tabulate
except Exception:
    print('Missing dependency: tabulate. Install with: pip install tabulate')
    sys.exit(2)


def find_field(fieldnames, candidates):
    if not fieldnames:
        return None
    lowered = {f.lower().strip(): f for f in fieldnames}
    for c in candidates:
        key = c.lower()
        if key in lowered:
            return lowered[key]
    return None


def read_files(file_paths):
    data = defaultdict(list)  # position -> list of floats
    found_any = False
    for path in file_paths:
        if not os.path.exists(path):
            print(f"Warning: file not found: {path}")
            continue
        with open(path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            pos_key = find_field(reader.fieldnames, ['position'])
            perf_key = find_field(reader.fieldnames, ['performance'])
            if pos_key is None or perf_key is None:
                print(f"Skipping {path}: required columns 'position' and 'performance' not found")
                continue
            found_any = True
            for row in reader:
                pos = row.get(pos_key, '').strip()
                if pos == '':
                    continue
                perf_raw = row.get(perf_key, '').strip()
                if perf_raw == '':
                    continue
                perf_raw = perf_raw.replace(',', '.')
                try:
                    perf = float(perf_raw)
                except ValueError:
                    continue
                data[pos].append(perf)
    if not found_any:
        print('No valid input files processed.')
    return data


def compute_averages(data):
    result = []
    for pos, vals in data.items():
        if not vals:
            continue
        avg = sum(vals) / len(vals)
        result.append((pos, avg))
    # sort descending by average
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def write_csv(report_name, rows):
    out_name = f"{report_name}.csv"
    with open(out_name, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['position', 'average_performance'])
        for pos, avg in rows:
            w.writerow([pos, f"{avg:.6f}"])
    return out_name


def main():
    parser = argparse.ArgumentParser(description='Form performance report from closed tasks CSV files')
    parser.add_argument('--files', '-f', nargs='+', required=True, help='Input CSV file(s)')
    parser.add_argument('--report', '-r', required=True, help='Report name to generate (e.g. performance)')
    args = parser.parse_args()

    data = read_files(args.files)
    averages = compute_averages(data)

    if not averages:
        print('No data to report.')
        sys.exit(0)

    table = [(pos, f"{avg:.2f}") for pos, avg in averages]
    print(tabulate(table, headers=['Position', 'Average Performance'], tablefmt='github'))

    csv_file = write_csv(args.report, averages)
    print(f"Saved CSV report: {csv_file}")


if __name__ == '__main__':
    main()
