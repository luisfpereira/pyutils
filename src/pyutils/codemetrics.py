import os
import json
import re

import numpy as np
import altair as alt

IGNORE_PATHS = ('.', 'docs', 'doc', 'tests', 'test', 'notebooks')
IGNORE_LANGS = ('reStructuredText', 'Markdown', 'make')
IGNORE_EXTS = ('geo', 'xmf', 'xdmf', 'h5', 'hdf5', 'xml', 'json',
               'yml', 'yaml', 'csv', 'svg', 'png')


def create_loc_chart(loc_df):
    loc_sum = loc_df.groupby('language').sum().reset_index().melt(
        id_vars=['language']).rename(columns={'variable': 'type', 'value': 'lines'})

    chart = alt.Chart(loc_sum).mark_bar().encode(
        x=alt.X('lines:Q'),
        y=alt.Y('language:N', sort=alt.EncodingSortField(field='lines', op='sum', order='descending')),
        color=alt.Color('type:N', scale=alt.Scale(scheme='accent')),
        tooltip=['lines:Q', 'type:O'],
    ).properties(title='Lines of code')

    return chart


def exclude_paths(df, ignore_paths=IGNORE_PATHS, col_name='path'):
    if '.' in ignore_paths:
        df = exclude_root_files(df, col_name=col_name)
        ignore_paths = list(ignore_paths)
        ignore_paths.remove('.')

    exc_indices = _exclude_str(df[col_name], ignore_paths, method='startswith')
    return df[~exc_indices]


def exclude_root_files(df, col_name='path'):
    inc_indices = _exclude_str(df[col_name], ['/'], 'contains')
    return df[inc_indices]


def exclude_languages(df, ignore_langs=IGNORE_LANGS):
    exc_indices = _exclude_str(df['language'], ignore_langs, method='match')

    return df[~exc_indices]


def exclude_file_types(df, ignore_exts=IGNORE_EXTS, col_name='path'):
    ignore_exts = [f'.{ext}' for ext in ignore_exts]
    exc_indices = _exclude_str(df[col_name], ignore_exts, 'endswith')

    return df[~exc_indices]


def include_only_paths(df, include_paths, col_name='path'):
    for path in include_paths:
        inc_indices = _exclude_str(df[col_name], include_paths,
                                   method='startswith')

    return df[inc_indices]


def _exclude_str(df_col, ignores, method):
    exc_indices = np.array([False] * df_col.size)

    for ignore in ignores:
        fnc = getattr(df_col.str, method)
        exc_indices = np.logical_or(exc_indices, fnc(ignore))

    return exc_indices


def create_html_report(project_name, charts_json,
                       filename='codemetrics_report.html'):
    """
    Args:
        charts_json (dict): JSON data.
            Must contain: 'loc', 'contr', 'loc_age', 'hotspots'.
    """

    # read template
    template_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'codemetrics_template.html')
    with open(template_filename, 'r') as file:
        template = file.read()

    # add json data
    html = template
    for plot_name, chart_data in charts_json.items():
        search_str = r'\{\{' + plot_name + r'\}\}'
        html = re.sub(search_str, json.dumps(chart_data),
                      html)

    # add project name
    html = re.sub(r'\{\{project_name\}\}', project_name, html)

    # create html file
    with open(filename, 'w') as file:
        file.write(html)


def create_html_report_from_files(project_name, charts_dir,
                                  filename='codemetrics_report.html'):

    # read json
    charts_json = {}
    for plot_name in ['loc', 'contr', 'loc_age', 'hotspots']:
        chart_filename = os.path.join(charts_dir, plot_name)

        with open(f'{chart_filename}.json', 'r') as file:
            charts_json[plot_name] = json.load(file)

    return create_html_report(project_name, charts_json, filename=filename)


def altair2json(chart):
    return json.loads(chart.to_json())
