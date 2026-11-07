import argparse
import json
import math
import platform
import statistics
from pathlib import Path
from insightweaver.workflow import FixtureProvider, OpenAIProvider, run_analysis

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['offline', 'live'], default='offline')
    parser.add_argument('--runs', type=int, default=10)
    parser.add_argument('--output', default='reports/benchmark.json')
    args = parser.parse_args()
    if not 1 <= args.runs <= 100:
        parser.error('runs must be between 1 and 100')
    data = json.loads(Path('examples/input.json').read_text())
    provider = FixtureProvider('examples/fixture_responses.json') if args.mode == 'offline' else OpenAIProvider()
    results = [run_analysis(data, provider) for _ in range(args.runs)]
    durations = sorted(r['elapsed_seconds'] for r in results)
    report = {'mode': args.mode, 'scope': 'workflow overhead with fixed offline responses; not LLM quality or latency' if args.mode == 'offline' else 'live provider latency on one example; not a general quality evaluation',
              'runs': args.runs, 'median_seconds': statistics.median(durations), 'p95_seconds': durations[math.ceil(0.95*len(durations))-1],
              'node_counts': [len(r['events']) for r in results], 'events': [r['events'] for r in results],
              'environment': {'python': platform.python_version(), 'platform': platform.platform()}}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))
