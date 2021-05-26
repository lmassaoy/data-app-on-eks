from utils.images_downloader import ImageRenderDownloader
from PIL import Image
import os
from os.path import join
import base64
import streamlit as st
import pandas as pd
import awswrangler as wr
import altair as alt


DATASETS_BUCKET_NAME = os.environ['BUCKET_NAME']
GENRES_FILE_NAME = os.environ['GENRES_FILE']
ANIME_FILE_NAME = os.environ['ANIME_FILE']


def session_break(times):
    for i in range(times):
        st.write('')


def block_break():
    st.markdown('---')


def title(text,size,align,color):
    st.markdown(f'<h1 style="font-weight:bolder;font-size:{size}px;color:{color};text-align:{align};">{text}</h1>',unsafe_allow_html=True)


def header(text):
    st.markdown(f"<p style='color:white;'>{text}</p>",unsafe_allow_html=True)


def generate_top_n_by_genre(genre_name,order_by_column):
    return joined_df[joined_df[genre_name]==1][joined_df[order_by_column]>0]\
            .sort_values(order_by_column,ascending=True)\
            .head(3)[[order_by_column,'id','title',genre_name]]\
            .rename(columns={order_by_column: 'Position', 'id': 'ID', 'title': 'Title'})\
            .reset_index(drop=True)


def generate_recommend_block(column_id,anime):
    st.markdown(f'### #{column_id} - [{anime[2]}](https://myanimelist.net/anime/{anime[1]}/)')
    download_agent = ImageRenderDownloader(int(anime[1]),str(joined_df[joined_df['id'] == anime[1]]["photo"].values[0]))
    folder_path = download_agent.download()
    st.image(Image.open(folder_path))

    score = f'''
    ##### **Score**: {float(joined_df[joined_df['id'] == anime[1]]['details.Score'])}
    '''
    rank = f'''
    ##### **Rank**: {int(joined_df[joined_df['id'] == anime[1]]["details.Ranked"])}
    '''
    popularity = f'''
    ##### **Popularity**: {int(joined_df[joined_df['id'] == anime[1]]["details.Popularity"])}
    '''
    members = f'''
    ##### **Members**: {f"{int(joined_df[joined_df['id'] == anime[1]]['details.Members']):,}"}
    '''
    st.markdown(score)
    st.markdown(rank)
    st.markdown(popularity)
    st.markdown(members)
    synopsis = joined_df[joined_df['id'] == anime[1]]['synopsis'].values
    st.markdown(f"###### {synopsis[0]}")


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_blank">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code


def generate_page_header():
    header_col1, header_col2 = st.beta_columns((2.5,1))

    with header_col1:
        title("Data App on Amazon EKS",60,"left","white")
        st.markdown('AWS + DevOps + Open Source = :purple_heart:')

    with header_col2:
        session_break(2)
        st.image('images/aws_logo.png')

    block_break()


docs_project = '''
- [GitHub](https://github.com/lmassaoy/data-app-on-eks)
- AWS
'''

docs_devops = '''
- [AWS CodeCommit](https://aws.amazon.com/pt/codecommit/)
- [AWS CodeBuild](https://aws.amazon.com/pt/codebuild/)
- [AWS CodePipeline](https://aws.amazon.com/pt/codepipeline/)
- [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/pt/ecr/)
'''

docs_kbs = '''
- [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/pt/eks/)
- [AWS Fargate](https://aws.amazon.com/pt/fargate/)
- [Classic Elastic Load Balancer (ELB)](https://aws.amazon.com/pt/elasticloadbalancing/classic-load-balancer/)
'''

docs_app = '''
- [AWS Data Wrangler](https://aws-data-wrangler.readthedocs.io/en/stable/)
- [Streamlit](https://streamlit.io/)
- [Amazon Simple Storage Service (S3)](https://aws.amazon.com/pt/s3/)
'''

intro_text = '''
Based on your preferences of anime genres this app will suggest the most well rated to you by doing data analysis using AWS Data Wrangler to explore a dataset with more than 20k Anime titles 
(from myanimelist.net), stored at Amazon S3 and querying using Pandas Dataframes.
'''

# ------------------------------------------------------------------------------------------------------------------------
# App Configs and Layout

st.set_page_config(
    page_title="Data App on Amazon EKS",
    page_icon="📊"
)
st.markdown(""" <style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: 2rem;
    }} </style> """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------------------------------------
# Main

st.write('update testing CI/CD - update 16h50')

generate_page_header()

title("Architecture",35,"center","white")
session_break(1)
st.image('images/arch_art.png',use_column_width=True)
session_break(1)

block_break()

title("Documentations",35,"center","white")

docs_col1, docs_col2, docs_col3, docs_col4 = st.beta_columns((1,2,2,2))

with docs_col1:
    title("Project",20,"center","yellow")
    st.markdown(docs_project)

with docs_col2:
    title("DevOps Pipeline",20,"center","green")
    st.markdown(docs_devops)

with docs_col3:
    title("Kubernetes Environment",20,"center","red")
    st.markdown(docs_kbs)

with docs_col4:
    title("Data App",20,"center","purple")
    st.markdown(docs_app)

block_break()

title('The App',35,'center','white')
title(intro_text,20,'center','white')
session_break(1)

# journey_col1, journey_col2, journey_col3 = st.beta_columns((1,.1,.25))

# with journey_col1:
#     st.markdown('### Check the box if you want to experience this journey')

# with journey_col2:
#     st.markdown('# :point_right:')

# with journey_col3:
#     session_break(2)
#     ux_check_box = st.checkbox('Let\'s do it!')

# journey_subcol1, journey_subcol2, journey_subcol3 = st.beta_columns((1,1,1))

# with journey_subcol2:
#     if ux_check_box:
#         st.success('You did it! :clap::clap::clap::clap::clap:')

block_break()


# ------------------------------------------------------------------------------------------------------------------------
# Datasets read

title('Loading datasets from Amazon S3',35,'center','white')
with st.spinner('Wait a moment...'):
    @st.cache(persist=True,suppress_st_warning=True)
    def get_s3_parquet(filename):
        return wr.s3.read_parquet(
            f's3://{DATASETS_BUCKET_NAME}/{filename}'
        )

    genres_df = get_s3_parquet(GENRES_FILE_NAME)
    genres_list =  genres_df.columns.values.tolist()
    del genres_list [0:2]

    animes_df = get_s3_parquet(ANIME_FILE_NAME)

    joined_df = pd.merge(animes_df, genres_df, on='id')

loading_col1, loading_col2, loading_col3 = st.beta_columns((1.7,1.5,.8))

with loading_col2:
    st.markdown('### Genres :white_check_mark:\n### Animes :white_check_mark:')

block_break()

# ------------------------------------------------------------------------------------------------------------------------
# Journey - Step 1

# Form filling
title('User\'s Preferences',35,'center','white')
title('Please fill the form below:',20,'center','white')

with st.beta_expander('Anime Preference Form'):
    with st.form("Anime Preference"):
        form_col1_size = 1

        st.write('Type Your Name')
        form_col1, form_col2 = st.beta_columns((form_col1_size,1))
        with form_col1:
            user_name = st.text_input(label='Name')

        st.write('Select up to 5 genres you like the most')
        form_col1, form_col2 = st.beta_columns((form_col1_size,1))
        with form_col1:
            selected_genres = st.multiselect(label='Genres',options=genres_list)

        st.write('Do you prefer the recommendation based on the Anime\'s Rank or Popularity')
        form_col1, form_col2 = st.beta_columns((form_col1_size,1))
        with form_col1:
            recommendation_based_on = st.selectbox(label='Based on',options=['Rank','Popularity'])

        session_break(1)
        submitted = st.form_submit_button("Submit")

    if submitted:
        if user_name == '':
            st.markdown("Let us know your beautiful name :wink:")
        elif len(selected_genres) == 0:
            st.markdown("You didn't select your favorite genre. Try at least 1 :wink:")
        elif len(selected_genres) > 5:
            st.markdown("Please select up to 5 genres :pensive:")
        else:
            st.markdown("Done!")

if submitted and len(selected_genres) >0 and len(selected_genres) <= 5 and user_name != '':
    title(f'Thanks for sharing, {user_name}!',25,'center','white')
    form_response_col1, form_response_col2, form_response_col3 = st.beta_columns((7,4,4))

    with form_response_col2:
        st.markdown('# :pray:')

block_break()

if submitted and len(selected_genres) >0 and len(selected_genres) <= 5 and user_name != '':
# ------------------------------------------------------------------------------------------------------------------------
# Journey - Step 2

# Data Analytics - Metric as a fact

    # title('Before We Get There, Did You Know...',35,'center','white')

    # curiosity_header_col1, curiosity_header_col2, curiosity_header_col3 = st.beta_columns((7,4,4))
    # with curiosity_header_col2:
    #         st.markdown('# :thinking_face:')

    # title('#1 - Top 3 Animes (by \'Rank\')',25,'center','white')

    # top_n = 3
    # def generate_top_n_by(attribute):
    #     return joined_df[joined_df[attribute]>0]\
    #         .sort_values(attribute,ascending=True)\
    #         .head(top_n)[[attribute,'id','title','details.Genres_x']]\
    #         .rename(columns={attribute: 'Position', 'id': 'ID', 'title': 'Title', 'details.Genres_x': 'Genres'})\
    #         .reset_index(drop=True)

    # top_n_rank = generate_top_n_by('details.Ranked')
    # top_n_rank_list = top_n_rank.values.tolist()

    # podium_col1, podium_col2, podium_col3 = st.beta_columns((1,1,1))

    # with podium_col1:
    #     session_break(4)
    #     title(top_n_rank_list[2][2],20,'right','brown')

    # with podium_col2:
    #     title(top_n_rank_list[0][2],20,'center','gold')

    # with podium_col3:
    #     session_break(2)
    #     title(top_n_rank_list[1][2],20,'left','silver')

    # podium_subcol1, podium_subcol2, podium_subcol3 = st.beta_columns((1,2,1))
    # with podium_subcol2:
    #     st.image('images/podium.png')
    #     st.markdown('##### Image downloaded from [good-ware page at flaticon.com](https://www.flaticon.com/authors/good-ware)')

    # session_break(1)

    # top1_chmp_col1, top1_chmp_col2, top1_chmp_col3 = st.beta_columns((1.5,2,1))
    # with top1_chmp_col2:
    #     st.markdown('## Champion\'s data :trophy:')

    # with st.beta_expander('Details'):
    #     top1_img_col1, top1_img_col2, top1_img_col3 = st.beta_columns((1.5,2,1))
    #     download_agent = ImageRenderDownloader(int(top_n_rank_list[0][1]),str(joined_df[joined_df['id'] == top_n_rank_list[0][1]]["photo"].values[0]))
    #     folder_path = download_agent.download()
    #     with top1_img_col2:
    #         st.image(build_image(folder_path))

    #     xray_header_col1, xray_header_col2, xray_header_col3, xray_header_col4, xray_header_col5 = st.beta_columns((1.,0.4,0.4,0.4,0.7))
    #     xray_header_label_col1, xray_header_label_col2, xray_header_label_col3, xray_header_label_col4, xray_header_label_col5 = st.beta_columns((1.,0.4,0.4,0.4,0.7))

    #     with xray_header_col1:
    #         title(top_n_rank_list[0][2],20,'left','gold')
    #     with xray_header_col2:
    #         st.header(float(joined_df[joined_df['id'] == top_n_rank_list[0][1]]['details.Score']))
    #     with xray_header_col3:
    #         st.header(int(joined_df[joined_df['id'] == top_n_rank_list[0][1]]["details.Ranked"]))
    #     with xray_header_col4:
    #         st.header(int(joined_df[joined_df['id'] == top_n_rank_list[0][1]]["details.Popularity"]))
    #     with xray_header_col5:
    #         st.header(f"{int(joined_df[joined_df['id'] == top_n_rank_list[0][1]]['details.Members']):,}")

    #     with xray_header_label_col1:
    #         st.markdown('###### Name')
    #     with xray_header_label_col2:
    #         st.markdown('###### Score')
    #     with xray_header_label_col3:
    #         st.markdown('###### Rank')
    #     with xray_header_label_col4:
    #         st.markdown('###### Popularity')
    #     with xray_header_label_col5:
    #         st.markdown('###### Members')

    #     session_break(1)
    #     st.markdown(f"Visit the title\'s [MyAnimeList.Net page](https://myanimelist.net/anime/{top_n_rank_list[0][1]}/) to check more info about it :)")

    # session_break(1)
    # title('#2 - Top 3 Animes (by \'Popularity\')',25,'center','white')

    # top_n_pop = generate_top_n_by('details.Popularity')
    # top_n_pop_list = top_n_pop.values.tolist()

    # podium_col1, podium_col2, podium_col3 = st.beta_columns((1,1,1))

    # with podium_col1:
    #     session_break(4)
    #     title(top_n_pop_list[2][2],20,'right','brown')

    # with podium_col2:
    #     title(top_n_pop_list[0][2],20,'center','gold')

    # with podium_col3:
    #     session_break(2)
    #     title(top_n_pop_list[1][2],20,'left','silver')

    # podium_subcol1, podium_subcol2, podium_subcol3 = st.beta_columns((1,2,1))
    # with podium_subcol2:
    #     st.image('images/podium.png')
    #     st.markdown('##### Image downloaded from [good-ware page at flaticon.com](https://www.flaticon.com/authors/good-ware)')

    # session_break(1)

    # top1_chmp_col1, top1_chmp_col2, top1_chmp_col3 = st.beta_columns((1.5,2,1))
    # with top1_chmp_col2:
    #     st.markdown('## Champion\'s data :trophy:')

    # with st.beta_expander('Details'):
    #     top1_img_col1, top1_img_col2, top1_img_col3 = st.beta_columns((1.5,2,1))
    #     download_agent = ImageRenderDownloader(int(top_n_pop_list[0][1]),str(joined_df[joined_df['id'] == top_n_pop_list[0][1]]["photo"].values[0]))
    #     folder_path = download_agent.download()
    #     with top1_img_col2:
    #         st.image(build_image(folder_path))

    #     xray_header_col1, xray_header_col2, xray_header_col3, xray_header_col4, xray_header_col5 = st.beta_columns((1.,0.4,0.4,0.4,0.7))
    #     xray_header_label_col1, xray_header_label_col2, xray_header_label_col3, xray_header_label_col4, xray_header_label_col5 = st.beta_columns((1.,0.4,0.4,0.4,0.7))

    #     with xray_header_col1:
    #         title(top_n_pop_list[0][2],20,'left','gold')
    #     with xray_header_col2:
    #         st.header(float(joined_df[joined_df['id'] == top_n_pop_list[0][1]]['details.Score']))
    #     with xray_header_col3:
    #         st.header(int(joined_df[joined_df['id'] == top_n_pop_list[0][1]]["details.Ranked"]))
    #     with xray_header_col4:
    #         st.header(int(joined_df[joined_df['id'] == top_n_pop_list[0][1]]["details.Popularity"]))
    #     with xray_header_col5:
    #         st.header(f"{int(joined_df[joined_df['id'] == top_n_pop_list[0][1]]['details.Members']):,}")

    #     with xray_header_label_col1:
    #         st.markdown('###### Name')
    #     with xray_header_label_col2:
    #         st.markdown('###### Score')
    #     with xray_header_label_col3:
    #         st.markdown('###### Rank')
    #     with xray_header_label_col4:
    #         st.markdown('###### Popularity')
    #     with xray_header_label_col5:
    #         st.markdown('###### Members')

    #     session_break(1)
    #     st.markdown(f"Visit the title\'s [MyAnimeList.Net page](https://myanimelist.net/anime/{top_n_pop_list[0][1]}/) to check more info about it :)")

    # session_break(1)
    # title('#3 - Title\'s Distribution by \'Genre\'',25,'center','white')

    # top_n_genres = 20
    # genres_labels = []
    # genres_sizes = []

    # for genre in genres_list:
    #     filtered_genre_df = joined_df[joined_df[genre]==1]
    #     genre_agg_df = filtered_genre_df[[genre,'id']]\
    #                         .groupby(genre, as_index=False)\
    #                         .agg('count')
    #     genres_labels.append(genre)
    #     if len(genre_agg_df.index) > 0:
    #         genres_sizes.append(genre_agg_df['id'].values[0])
    #     else:
    #         genres_sizes.append(0)

    # genres_dict = {'Genres': genres_labels, 'Animes': genres_sizes}  
    # genre_agg_df = pd.DataFrame(genres_dict)

    # bar = alt.Chart(genre_agg_df).mark_bar().encode(
    #     x=alt.X('Genres:O', sort='-y'),
    #     y='Animes:Q',
    #     color=alt.Color(
    #         'Genres:O',
    #         legend=None
    #     )
    # )
    # text = bar.mark_text(
    #     align='left',
    #     baseline='middle',
    #     dx=-12,
    #     dy=-7
    # ).encode(
    #     text='Animes:Q'
    # )

    # st.altair_chart((bar+text).transform_window(
    #                                 rank='rank(Animes)',
    #                                 sort=[alt.SortField('Animes', order='descending')]
    #                             ).transform_filter(
    #                                 alt.datum.rank <= 20
    #                             ), use_container_width=True)

    # session_break(1)

    # block_break()

# ------------------------------------------------------------------------------------------------------------------------
# Journey - Step 3

    title('Our Recommendations To You Today',35,'center','white')

    for genre in selected_genres:
        if recommendation_based_on == 'Rank':
            filtered_by_genre_df = generate_top_n_by_genre(genre,'details.Ranked')
        else:
            filtered_by_genre_df = generate_top_n_by_genre(genre,'details.Popularity')
        filtered_by_genre_list = filtered_by_genre_df.values.tolist()

        title(f'{genre}',25,'center','white')
        recommend_body_col1, recommend_body_col2, recommend_body_col3 = st.beta_columns((1,1,1))
        with recommend_body_col1:
            generate_recommend_block(1,filtered_by_genre_list[0])
        with recommend_body_col2:
            generate_recommend_block(2,filtered_by_genre_list[1])
        with recommend_body_col3:
            generate_recommend_block(3,filtered_by_genre_list[2])

    session_break(2)
    block_break()

# ------------------------------------------------------------------------------------------------------------------------
# Thank you

    title('THANK YOU!',60,'center','white')
    ty_col1, ty_col2, ty_col3 = st.beta_columns((1.1,2,1))

    with ty_col2:
        st.markdown(get_img_with_href('images/thank_you.gif', 'https://github.com/lmassaoy'), unsafe_allow_html=True)

    session_break(1)
    st.markdown('### If you enjoyed this data app, please leave your :star: in the GitHub repository and follow me in the social medias :heart:')
    session_break(1)
    social_medias_col1, social_medias_col2, social_medias_col3, social_medias_col4 = st.beta_columns((.2,.5,.5,.5))

    with social_medias_col2:
        st.markdown(get_img_with_href('images/github.png', 'https://github.com/lmassaoy/data-app-on-eks'), unsafe_allow_html=True)

    with social_medias_col3:
        st.markdown(get_img_with_href('images/linkedin.png', 'https://www.linkedin.com/in/luis-yamada/'), unsafe_allow_html=True)

    with social_medias_col4:
        st.markdown(get_img_with_href('images/twitter.png', 'https://twitter.com/massaoyamada'), unsafe_allow_html=True)