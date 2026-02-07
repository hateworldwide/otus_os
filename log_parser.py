import re
import os
import json
import glob
from collections import defaultdict
from typing import Tuple, List, Dict, Any
import argparse


class StreamingLogParser:
    def __init__(self):
        self.log_pattern = r'(\S+)\s.*?\s(\[[^\]]+\])\s+"([A-Z]+)\s+(\S+?)\s+.+\s+(\d+)$'

    def parse_line(self, line: str) -> Dict[str, Any]:
        line = line.strip()
        if not line:
            return None
        match = re.match(self.log_pattern, line)
        if not match:
            return None
        try:
            return {
                'ip': match.group(1),
                'time_str': match.group(2),
                'method': match.group(3).upper(),
                'url': match.group(4),
                'duration': int(match.group(5))
            }
        except:
            return None


class LogAnalyzer:
    def __init__(self):
        self.parser = StreamingLogParser()

    def analyze_file(self, filename: str) -> Tuple[int, Dict[str, int], List[Tuple[str, int]], List[Dict]]:
        total = 0
        methods = defaultdict(int)
        ips = defaultdict(int)
        slow = []

        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    total += 1
                    parsed = self.parser.parse_line(line)
                    if not parsed:
                        continue

                    methods[parsed['method']] += 1
                    ips[parsed['ip']] += 1

                    req = {
                        'method': parsed['method'],
                        'url': parsed['url'],
                        'ip': parsed['ip'],
                        'duration': parsed['duration'],
                        'time_str': parsed['time_str'],
                    }

                    entry = (parsed['duration'], req)
                    if len(slow) < 3:
                        slow.append(entry)
                        slow.sort(key=lambda x: x[0])
                    elif parsed['duration'] > slow[0][0]:
                        slow[0] = entry
                        slow.sort(key=lambda x: x[0])

        except Exception as e:
            return 0, {}, [], []

        top_ips = sorted(ips.items(), key=lambda x: x[1], reverse=True)[:3]
        slowest = [data for _, data in sorted(slow, key=lambda x: x[0], reverse=True)]

        return total, dict(methods), top_ips, slowest

    def analyze_and_save_file(self, input_file: str, output_file: str = None) -> bool:
        total, methods, top_ips, slowest = self.analyze_file(input_file)
        if total == 0:
            return False

        result = self.format_to_json(total, methods, top_ips, slowest)

        if not output_file:
            output_file = f"{os.path.splitext(input_file)[0]}_analysis.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Сохранен: {output_file}")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return True

    def analyze_and_save_directory(self, input_dir: str, output_dir: str = None, pattern: str = "*.log"):
        files = glob.glob(os.path.join(input_dir, pattern))
        if not files:
            return

        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for input_file in files:
            if output_dir:
                output_file = os.path.join(output_dir,
                                           f"{os.path.splitext(os.path.basename(input_file))[0]}_analysis.json")
            else:
                output_file = f"{os.path.splitext(input_file)[0]}_analysis.json"

            self.analyze_and_save_file(input_file, output_file)

    def format_to_json(self, total: int, methods: Dict[str, int], top_ips: List[Tuple[str, int]],
                       slowest: List[Dict]) -> Dict[str, Any]:
        ips_dict = {ip: cnt for ip, cnt in top_ips}

        longest = []
        for req in slowest:
            longest.append({
                'ip': req['ip'],
                'date': req['time_str'],
                'method': req['method'],
                'url': req['url'] if req['url'] else '-',
                'duration': req['duration']
            })

        return {
            "top_ips": ips_dict,
            "top_longest": longest,
            "total_stat": methods,
            "total_requests": total
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Файл или директория')
    parser.add_argument('--output', '-o', help='Директория или файл для сохранения JSON')
    parser.add_argument('--pattern', '-p', default='*.log', help='Шаблон файлов')
    args = parser.parse_args()

    analyzer = LogAnalyzer()

    if os.path.isfile(args.path):
        if args.output:
            analyzer.analyze_and_save_file(args.path, args.output)
        else:
            analyzer.analyze_and_save_file(args.path)

    elif os.path.isdir(args.path):
        analyzer.analyze_and_save_directory(args.path, args.output, args.pattern)

    else:
        print(f"Не найден: {args.path}")


if __name__ == "__main__":
    main()