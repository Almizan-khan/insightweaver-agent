import csv
import io
import json
import os
from pathlib import Path
from .workflow import FixtureProvider, OpenAIProvider, run_analysis

ROOT = Path(__file__).resolve().parent.parent

def read_input(text, filename):
    if not filename:
        return text.strip()
    path = Path(filename)
    if path.suffix.lower() != '.csv' or path.stat().st_size > 1_000_000:
        raise ValueError('Upload a CSV smaller than 1 MB')
    content = path.read_text(encoding='utf-8-sig')
    rows = list(csv.reader(io.StringIO(content)))
    if not rows or len(rows) > 1001:
        raise ValueError('CSV must have a header and at most 1000 data rows')
    result = '\n'.join(' | '.join(row) for row in rows)
    if len(result) > 40000:
        raise ValueError('Input exceeds the 40,000-character demo limit')
    return result

def main():
    import gradio as gr
    from dotenv import load_dotenv
    load_dotenv()
    demo_mode = os.getenv('INSIGHTWEAVER_MODE', 'offline')
    if demo_mode not in {'offline', 'live'}:
        raise ValueError('INSIGHTWEAVER_MODE must be offline or live')

    def process(feedback, feedback_file, sales, sales_file, business, tone):
        try:
            provider = FixtureProvider(ROOT/'examples/fixture_responses.json') if demo_mode == 'offline' else OpenAIProvider()
            data = {'customer_feedback': read_input(feedback, feedback_file), 'sales_summaries': read_input(sales, sales_file),
                    'business_type': business, 'email_tone': tone}
            return json.dumps(run_analysis(data, provider), indent=2)
        except Exception as error:
            if isinstance(error, (ValueError, OSError)):
                raise gr.Error(str(error)) from error
            raise gr.Error('Analysis failed. Check provider availability and server logs; no message was sent.') from error

    sample = json.loads((ROOT/'examples/input.json').read_text())
    with gr.Blocks(title='InsightWeaver') as demo:
        gr.Markdown('# InsightWeaver\nBusiness feedback and sales analysis with a five-stage LangGraph workflow.')
        if demo_mode == 'offline':
            gr.Markdown('**Offline fixture demo:** fixed sample responses demonstrate the workflow and output schema. They do not analyze new inputs. No API is contacted.')
        else:
            gr.Markdown('**Live mode:** submitted text is sent to the configured AI provider. Use non-sensitive sample data. Generated emails remain drafts.')
        with gr.Row():
            feedback = gr.Textbox(label='Customer feedback', value=sample['customer_feedback'], lines=6)
            sales = gr.Textbox(label='Sales summary', value=sample['sales_summaries'], lines=6)
        with gr.Row():
            feedback_file = gr.File(label='Feedback CSV', file_types=['.csv'], type='filepath')
            sales_file = gr.File(label='Sales CSV', file_types=['.csv'], type='filepath')
        business = gr.Textbox(label='Business type', value='SaaS')
        tone = gr.Dropdown(['formal', 'friendly', 'empathetic'], value='formal', label='Email tone')
        output = gr.Code(label='Structured report', language='json')
        gr.Button('Run analysis').click(process, [feedback, feedback_file, sales, sales_file, business, tone], output)
    demo.launch(server_name='127.0.0.1', share=False)

if __name__ == '__main__':
    main()
