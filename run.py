import argparse
import json
from pathlib import Path
from insightweaver.workflow import FixtureProvider, OpenAIProvider, run_analysis

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='examples/input.json')
    parser.add_argument('--mode', choices=['offline', 'live'], default='offline')
    parser.add_argument('--output', default='outputs/report.json')
    args = parser.parse_args()
    provider = FixtureProvider('examples/fixture_responses.json') if args.mode == 'offline' else OpenAIProvider()
    result = run_analysis(json.loads(Path(args.input).read_text()), provider)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
