import numpy as np
import codemetrics as cm
import altair as alt

IGNORE_PATHS = ('.', 'docs', 'doc', 'tests', 'test', 'notebooks')
IGNORE_LANGS = ('reStructuredText', 'Markdown', 'make')
IGNORE_EXTS = ('geo', 'xmf', 'xdmf', 'h5', 'hdf5', 'xml', 'json',
               'yml', 'yaml', 'csv', 'svg', 'png')

# TODO: include only also?


def get_loc(repo, ignore_paths=IGNORE_PATHS, ignore_langs=IGNORE_LANGS,
            ignore_exts=IGNORE_EXTS, **kwargs):
    df = cm.get_cloc(repo, **kwargs)

    # exclude paths and/or languages
    df = exclude_paths(df, ignore_paths=ignore_paths)
    df = exclude_languages(df, ignore_langs=ignore_langs)
    df = exclude_file_types(df, ignore_exts=ignore_exts)

    return df


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
    exc_indices = _exclude_str(df[col_name], ['/'], 'contains', negate=True)
    return df[~exc_indices]


def exclude_languages(df, ignore_langs=IGNORE_LANGS):
    exc_indices = _exclude_str(df['language'], ignore_langs, method='match')

    return df[~exc_indices]


def exclude_file_types(df, ignore_exts=IGNORE_EXTS, col_name='path'):
    ignore_exts = [f'.{ext}' for ext in ignore_exts]
    exc_indices = _exclude_str(df[col_name], ignore_exts, 'endswith')

    return df[~exc_indices]


def _exclude_str(df_col, ignores, method, negate=False):
    exc_indices = np.array([False] * df_col.size)

    for ignore in ignores:
        fnc = getattr(df_col.str, method)
        new_exc_indices = ~(fnc(ignore)) if negate else fnc(ignore)
        exc_indices = np.logical_or(exc_indices, new_exc_indices)

    return exc_indices
