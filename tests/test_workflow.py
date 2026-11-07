import json
import tempfile
import unittest
from pathlib import Path
from pydantic import ValidationError
from insightweaver.workflow import FixtureProvider, run_analysis
from insightweaver.app import read_input

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path('examples/input.json').read_text())
        self.provider = FixtureProvider('examples/fixture_responses.json')

    def test_every_stage_executes_once_and_fan_in_is_complete(self):
        calls = []
        def recording(name, schema, task, data):
            if name == 'insights':
                self.assertIn('feedback', data)
                self.assertIn('sales', data)
            calls.append(name)
            return self.provider(name, schema, task, data)
        result = run_analysis(self.data, recording)
        self.assertCountEqual(calls, ['feedback', 'sales', 'insights', 'email', 'marketing'])
        self.assertEqual(len(result['events']), 5)
        self.assertIn('subject', result['email'])

    def test_offline_output_is_explicitly_labeled(self):
        self.assertEqual(run_analysis(self.data, self.provider)['mode'], 'offline_fixture')

    def test_invalid_input_rejected_before_provider_calls(self):
        with self.assertRaises(ValidationError):
            run_analysis({**self.data, 'customer_feedback': ''}, self.provider)

    def test_provider_failure_does_not_create_success_output(self):
        def broken(*args):
            raise RuntimeError('provider unavailable')
        with self.assertRaises(RuntimeError):
            run_analysis(self.data, broken)

    def test_malformed_structured_response_rejected(self):
        def malformed(*args):
            return {}, {}
        with self.assertRaises(ValidationError):
            run_analysis(self.data, malformed)

    def test_uploaded_csv_is_bounded_and_unicode_safe(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'sample.csv'
            path.write_text('review,score\nHelpful,5\n', encoding='utf-8')
            self.assertIn('Helpful | 5', read_input('', str(path)))
            path.write_text('x'*1_000_001)
            with self.assertRaises(ValueError):
                read_input('', str(path))
