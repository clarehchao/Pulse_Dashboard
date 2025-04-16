import pandas as pd
import plotly.express as px
import re
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objects as go
import numpy as np
import circlify

parent_concern_dct = {'academic stress': 'Career and Academic Development',
                          'mental health and emotional well-being': 'Mental Health Well-being',
                          'teen emotional wellbeing': 'Mental Health Well-being',
                          'excessive technology and social media use': 'Excessive Technology Use',
                          'nothing concerns me today': 'Nothing',
                          'balance between school, sports, and family': 'Life Balance',
                          'work/life balance': 'Life Balance',
                          'social challenges (bullying, social isolation)': 'Social Challenges',
                          'social issues': 'Social Challenges',
                          'mental health': 'Mental Health Well-being',
                          'mental health wellbeing': 'Mental Health Well-being',
                          'emotional well-being': 'Mental Health Well-being',
                          'substance abuse - self-harm behaviour': 'Substance Abuse & Self-harm',
                          'identity development (peer pressure, gender exploration)': 'Identity Development',
                          }

# AdviceSource1-5: Categories (Therapist & Professionals, Families & Friends, Other Parents, Google, A.I., Online Resources)
# advicesrc_categories_dct = {
#     'therapists': 'Therapist & Professionals',
#     'therapy': 'Therapist & Professionals',
#     'therapist': 'Therapist & Professionals',
#     'psychologist': 'Therapist & Professionals',
#     'psychologists': 'Therapist & Professionals',
#     'pediatrician': 'Therapist & Professionals',
#     'psicóloga': 'Therapist & Professionals',
#     'therapy/professional help': 'Therapist & Professionals',
#     'professionals': 'Therapist & Professionals',
#     'holistic therapy': 'Therapist & Professionals',
#     'husband': 'Families & Friends',
#     'family': 'Families & Friends',
#     'your partner': 'Families & Friends',
#     'friends': 'Families & Friends',
#     'friends/family': 'Families & Friends',
#     'friends / family': 'Families & Friends',
#     'my own parents': 'Families & Friends',
#     'siblings': 'Families & Friends',
#     'google': 'Online Resources',
#     'instagram following lisa damour and other adolescent psychs': 'Online Resources',
#     'facebook groups':'Online Resources',
#     'podcasts': 'Online Resources',
#     'spiritual coach': 'Religious & Spiritual community',
#     'religious community': 'Religious & Spiritual community',
#     'parenting books': 'Books',
#     'other moms': 'Other Parents',
#     'couple': 'Other Parents',
#     'friends who are also parents': 'Other Parents',
#     'friends who are parents': 'Other Parents',
#     'other parents/friends': 'Other Parents',
#     'chatgpt': 'Artificial Intelligence',
#     'a.i': 'Artificial Intelligence'
# }

advicesrc_categories_dct = {
    'therapists': 'Therapist & Professionals',
    'therapy': 'Therapist & Professionals',
    'therapist': 'Therapist & Professionals',
    'psychologist': 'Therapist & Professionals',
    'psychologists': 'Therapist & Professionals',
    'pediatrician': 'Therapist & Professionals',
    'psicóloga': 'Therapist & Professionals',
    'therapy/professional help': 'Therapist & Professionals',
    'professionals': 'Therapist & Professionals',
    'holistic therapy': 'Therapist & Professionals',
    'husband': 'Families & Friends',
    'family': 'Families & Friends',
    'your partner': 'Families & Friends',
    'friends': 'Families & Friends',
    'friends/family': 'Families & Friends',
    'friends / family': 'Families & Friends',
    'my own parents': 'Families & Friends',
    'parents': 'Families & Friends',
    'siblings': 'Families & Friends',
    'google': 'Online Resources',
    'instagram following lisa damour and other adolescent psychs': 'Online Resources',
    'facebook groups':'Online Resources',
    'podcasts': 'Online Resources',
    'spiritual coach': 'Religious & Spiritual community',
    'religious community': 'Religious & Spiritual community',
    'parenting books': 'Books',
    'other moms': 'Other Parents',
    'couple': 'Other Parents',
    'friends who are also parents': 'Other Parents',
    'friends who are parents': 'Other Parents',
    'other parents/friends': 'Other Parents',
    'chatgpt': 'Artificial Intelligence',
    'a.i': 'Artificial Intelligence'
}

metric_annotate_txt_dct = {
        'Parent_Involve': '0: Not Involved, 5: Very Involved',
        'Teen_Share': '0: Never Share, 5: Always Share'
}

metric_col_lst = ['Age', 'Gender', 'NumofTeens', 'MedianTeenAge', 'Marital Status', 'Ethnicity', 'State',
                  'Parent_Involve', 'Teen_Share']
metric_label = ['Age', 'Gender', 'Number of Teens', 'Median Age of Teens', 'Marital Status',
                'Ethnicity', 'State', 'Parent Involvement Level', 'Teens Sharing Comfort Level']
metric_dct = dict(zip(metric_col_lst, metric_label))


def Read_Clean_Data(fname, grptype=None):
    # return a dataframe with the var_of_interested updated and clean

    the_df = pd.read_csv(fname)

    if grptype == 'parents':
        # Add age columns for future analysis: # of teens, median teen age, age histogram of teens
        df_tmp = the_df.loc[:, ['Teen1', 'Teen2', 'Teen3', 'Teen4', 'Teen5']]
        the_df['NumofTeens'] = df_tmp.count(axis=1)
        the_df['MedianTeenAge'] = df_tmp.median(axis=1, skipna=True)

        # clean and one hot encode PARENT CONCERN
        cols_PC = ['ParentConcern1', 'ParentConcern2', 'ParentConcern3', 'ParentConcern4']
        df_pc = OneHotEncodeCategory(the_df, cols_PC, 'PC_', parent_concern_dct)

        # clean and one hot encode Advice Source
        cols_Adsrc = [f'AdviceSource{n}' for n in range(1, 6)]
        df_adsrc = OneHotEncodeCategory(df_pc, cols_Adsrc, 'AdS_', advicesrc_categories_dct)

        # clean and one hot encode Helpful Advice
        cols_Hads = ['HelpfulAdviceSrc1', 'HelpfulAdviceSrc2']
        # print(df_parents['HelpfulAdviceSrc2'].unique())
        df_Hads = OneHotEncodeCategory(df_adsrc, cols_Hads, 'HAdS_', advicesrc_categories_dct)

        # clean and one hot encode Social Media
        cols_SM = [f'ParentSM{ii}' for ii in range(1, 6)]
        df_SM = OneHotEncodeCategory(df_Hads, cols_SM, 'PSM_')

        # clean and one hot encode Desire App Feature
        cols_AppFeats = [f'DesiredAppFeature{ii}' for ii in range(1, 5)]
        df_more = OneHotEncodeCategory(df_SM, cols_AppFeats, 'AFeat_')
    elif grptype == 'teens':
        # clean teens csv data
        the_df.columns = the_df.iloc[0].tolist()
        the_df = the_df[1:]

        # strong emotion
        cols_stgemo = ['HandleStrongEmo']
        df_sm = OneHotEncodeCategory(the_df, cols_stgemo, 'StgEmo_')

        # ppl teens reach out to
        cols_reachout = [f'ReachOut{nn}' for nn in range(1, 7)]
        df_ro = OneHotEncodeCategory(df_sm, cols_reachout, 'RO_')

        # social media use
        cols_socmd = [f'SM{nn}' for nn in range(1, 7)]
        df_sm = OneHotEncodeCategory(df_ro, cols_socmd, 'SM_')

        # social media impact reason
        cols_smreason = [f'SMImpactReason{nn}' for nn in range(1, 3)]
        df_more = OneHotEncodeCategory(df_sm, cols_smreason, 'SMR_')

    return df_more

def OneHotEncodeCategory(df, cols, prefstr,cat_dct=None):
    # df: the data_frame with all the data
    # cols: column names of interest
    # cat_dct: category dictionary to transform the string data
    # prefstr: prefix string to add to category column name

    # remove leading and trailing space and period
    cols_upd = [f'{ss}_upd' for ss in cols]
    df[cols_upd] = df[cols].apply(lambda x: x.str.strip().str.lower().str.rstrip('.'), axis=0)

    cols_cat = [f'{ss}_category' for ss in cols]
    if cat_dct is None: # make sure all text are capitalized with the first letters
        df[cols_cat] = df[cols_upd].map(lambda x: x.title() if pd.notna(x) else x)
        print('no cat_dct is defined')
    else:
        # Returns x if x (key) doesn't exist but dict[x] if it does via dict.get()
        df[cols_cat] = df[cols_upd].map(lambda x: cat_dct.get(x, x).title() if pd.notna(x) else x)
        print('cat_dct is defined')

    # drop all the cols and updated cols to just have the cols that we find to merge back with the orginal data
    df = df.drop(cols_upd, axis=1)

    df['Combined'] = df[cols_cat].apply(lambda row: ', '.join(row.dropna().astype(str)), axis=1)

    # one hot encoding of all Parent concern category into 0/1
    binary_df = df['Combined'].str.get_dummies(sep=', ')
    new_col = [f'{prefstr}{ss}' for ss in binary_df.columns]
    binary_df.columns = new_col

    df_new = pd.concat([df, binary_df], axis=1)
    df_new = df_new.drop(cols_cat + ['Combined'], axis=1)

    return df_new

def plot_horizontal_bar(df_all, col_prefix, xx, yy, x_title, txt_fmt,title='',ht=None,wd=None, x_range=None, hovername=None, customdata=None,color=None):

    # get count data from one hot encoded columns
    the_cols = [ss for ss in df_all.columns if ss.startswith(col_prefix)]
    the_df = df_all[the_cols].mean().sort_values(ascending=False).reset_index()
    the_df.columns = ['Category', '% Total']
    the_df['100-Ptotal'] = the_df.apply(lambda row: 1 - row['% Total'], axis=1)
    cat_order = the_df['Category'].tolist()

    # make yaxislabel dictionary for the right label
    yylabel_values = [ss.removeprefix(col_prefix) for ss in the_cols]
    yylabel_dct = dict(zip(the_cols, yylabel_values))

    # plot horizontal bar chart via plotly express and return fig
    if isinstance(xx, list) and x_range is not None: # color should a dictionary of color map
        # print('xx is a list!')
        fig = px.bar(
            data_frame=the_df,
            x=xx,
            y=yy,
            orientation='h',
            text_auto=txt_fmt,
            category_orders={'Category':cat_order},
            height=ht,
            width=wd,
            hover_name=hovername,
            custom_data=customdata,
            color_discrete_map= color,
            title = title
        )
        fig.update_layout(
            title = {
                'text': title,
                'font': {
                    'family':  "Inter, sans-serif",
                    'size': 18,
                    'weight':'bold',
                    'color':'#555b6e'
                },
            },
            xaxis_title={
                'text': x_title,
                'font': {'size': 14, 'family': 'Arial', 'weight':'bold'}
            },
            yaxis_title={ # remove y-axis title
                'text':''
            },
            xaxis={
                'tickformat': txt_fmt,
                'range':x_range
            },
            yaxis={
                'tickfont':{
                    'family':'Arial',
                    'size': 12,
                    'weight':'bold'
                }
            },
            showlegend = False
        )
    else:  # color should be a single color in a list
        fig = px.bar(
            data_frame=the_df,
            x=xx,
            y=yy,
            orientation='h',
            text_auto=txt_fmt,
            category_orders={'Category':cat_order},
            height=ht,
            width=wd,
            hover_name=hovername,
            custom_data=customdata,
            color_discrete_sequence = color
        )
        fig.update_layout(
            title={
                'text': title,
                'font': {
                    'family': "Inter, sans-serif",
                    'size': 18,
                    'weight': 'bold',
                    'color': '#555b6e'
                },
            },
            xaxis_title={
                'text': x_title,
                'font': {'size': 14, 'family': 'Arial', 'weight':'bold'}
            },
            yaxis_title={ # remove y-axis title
                'text':''
            },
            xaxis={
                'tickformat': txt_fmt
            },
            yaxis={
                'tickfont':{
                    'family':'Arial',
                    'size': 12,
                    'weight':'bold'
                }
            }
        )

    # # update y-axis label if any
    # if ylabeldct is not None:
    fig.update_yaxes(labelalias=yylabel_dct)

    #Top category
    top_cat = yylabel_dct[the_df.loc[0, 'Category']]

    return fig, top_cat


def sort_strings_with_numbers(ss):
    def extract_first_number(s):
        # Extract numbers from the string
        numbers = re.findall(r'\d+', s)

        # Convert to integer or use a large number if no digits found; take first number string
        return int(numbers[0]) if numbers else float('inf')

    # sorted will sort the list of string according a pre-defined function in 'key'
    return sorted(ss, key=extract_first_number)



def plot_vertical_bar(the_df,metric):
    df_grp = the_df.groupby(by=metric)[metric].count().reset_index(name='Counts')

    fig = px.bar(
        data_frame=df_grp,
        x=metric,
        y='Counts',
        color_discrete_sequence=px.colors.qualitative.Set2,
        height=600,
        width=930
    )
    fig.update_layout(
        xaxis_title={
            'text': metric_dct[metric],
            'font': {'size': 20, 'family': 'Arial', 'weight': 'bold'}
        },
        yaxis_title={
            'text': '# of Counts',
            'font': {'size': 20, 'family': 'Arial', 'weight': 'bold'}
        },
        xaxis={
            'tickfont': {
                'family': 'Arial',
                'size': 16,
            }
        },
        yaxis = {
            'tickfont': {
                'family': 'Arial',
                'size': 16,
            }
        }
    )

    if metric in ['Parent_Involve', 'Teen_Share']:
        xxt = df_grp[metric].tolist()
        fig.update_layout(
            xaxis={
                'tickmode': 'array',
                'tickvals': xxt
            }
        )
        fig.add_annotation(
            text=metric_annotate_txt_dct[metric],
            xref="paper",
            yref="paper",
            x=0.05,  # Center horizontally
            y=0.98,  # Position below the plot
            showarrow=False,
            font=dict(size=18)
        )

    return fig

def state_name_to_code(state_name):
    state_codes = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'DC':'DC'
    }
    # print(state_name, state_codes.get(state_name, "Invalid state name"))
    return state_codes.get(state_name, "Invalid state name")


SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def get_ordinal(i):
    # Adapted from https://codereview.stackexchange.com/questions/41298/producing-ordinal-numbers
    nn = int(i)
    if (nn % 100 >= 10) and (nn % 100 <= 20):
        return 'th'
    else:
        return SUFFIXES.get(nn % 10, 'th')




def create_card(h3_id,h3_class,h4_id,h4_class):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H3(id=h3_id,className=h3_class),
                    ],
                    className="d-flex align-items-center",
                ),
                html.H4(id=h4_id, className=h4_class),
            ],
            # className=h4_class,
        ),
        className="card",
    )



def circle_chart(df_all, metric, colors, title):

    the_df = df_all[metric].value_counts().reset_index()

    circles = circlify.circlify(
        the_df['count'].tolist(),
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

    # Create circles for each library
    fig = go.Figure()

    for i, (_, row) in enumerate(the_df.iterrows()):
        x, y, _ = circles[i]
        cc = np.sqrt(row['count']) / 10
        # print(f'x = {x}, y = {y}, i = {i}, count = {row['count']}')

        if metric == 'SMImpact':
        #     if i == 0:
        #         y = y - 0.1
            if i == 2:
                x = x - 0.2
                y = y + 0.13
        #     if i == 3:
        #         x = x - 0.3
        #         y = y + 0.05

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=cc*320,  # Adjust this multiplier to change overall bubble sizes
                color=colors[i],
                opacity=1.0,
                line=dict(width=0, color='DarkSlateGrey')
            ),
            text=f"{row[metric]}<br>{row['count']:,}",
            textposition='middle center',
            textfont=dict(
                family='Arial',
                color='black',
                size=20 if row['count'] > 100 else 15
            ),
            name=row['SMImpact'],
            hoverinfo='text',
            hovertext=f"{row[metric]}: {row['count']:,}"
        ))

    # Set layout
    fig.update_layout(
        title={
            'text': title,
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        showlegend=False,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        plot_bgcolor='white',
        # width=900,
        # height=800,
        margin=dict(t=40, b=40, l=40, r=40)
    )

    # Make x and y scales equal to ensure circles appear as circles, not ovals
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )

    return fig



