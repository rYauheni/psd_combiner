from parse_templates.parse_template import ParseTemplate

PARSE_TEMPLATES = (
    ParseTemplate(
        title='buy_in',
        detector=r'Tournament #\d+',
        start=r'[$¥€]',
        end=r' ',
        required=True
    ),

    ParseTemplate(
        title='total_received',
        detector=r'received a total',
        start=r'[$¥€]',
        end=r'\.\n',
        required=True
    ),

    ParseTemplate(
        title='re_entry',
        detector=r're-entries',
        start=r'made ',
        end=r' ',
        required=False
    )
)
