import sys
import json
import csv


def open_data(data_to_read):
    with open(data_to_read, 'r') as file:
        json_data = json.load(file)
        return json_data


def write_results(record_type, data_to_record):
    list_length = len(next(iter(data_to_record.values())))

    if "-j" in record_type:
        result = []

        for i in range(list_length):
            group = {}
            for key, value_list in data_to_record.items():
                group[key] = value_list[i]
            result.append(group)

        with open("output.json", "w") as file:
            json.dump(result, file, indent=4)

    elif "-csv" in record_type:
        with open("output.csv", "w") as file:
            writer = csv.writer(file)

            for i in range(list_length):
                row = []
                for key, value_list in data_to_record.items():
                    row.append(f"{key}: {value_list[i]}")
                writer.writerow(row)
                writer.writerow([])
    else:
        for i in range(list_length):
            for key, value_list in data_to_record.items():
                print(f"{key}: {value_list[i]}")
            print()


def find_key_values(data, target_keys, results):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in target_keys:
                results[key].append(value)
            elif isinstance(value, (dict, list)):
                find_key_values(value, target_keys, results)

    elif isinstance(data, list):
        for item in data:
            find_key_values(item, target_keys, results)


def main():
    json_data = open_data(sys.argv[1])
    output_type = sys.argv[2]
    results_data = {key: [] for key in sys.argv[3:]}

    find_key_values(json_data, results_data.keys(), results_data)

    write_results(output_type, results_data)


if __name__ == "__main__":
    main()
