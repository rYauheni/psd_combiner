from parse_templates.parse_template import ParseTemplate

buy_in_template = ParseTemplate(
    title='buy_in',
    detector=r'Tournament #\d+',
    start=r'[$¥€]',
    end=r' '
)

total_received_template = ParseTemplate(
    title='total_received',
    detector='received a total',
    start=r'[$¥€]',
    end=r'\.\n'
)

PARSE_TEMPLATES = (buy_in_template, total_received_template)
