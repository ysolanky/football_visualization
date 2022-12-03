import pandas as pd
#from IPython.display import display
pd.set_option('display.max_columns', None)
import plotly.express as px
import streamlit as st
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import plotly.graph_objects as go
from PIL import Image
import matplotlib.pyplot as plt
import ast
import numpy as np
import math
from mplsoccer.pitch import Pitch

base_data=pd.read_csv("Fifa_data_mod.csv",
                       dtype={'Known As':str,
                                'Full Name':str,
                                'Overall':float,
                                'Potential':float,
                                'Value(in Euro)':float,
                                'Positions Played':str,
                                'Best Position':str,
                                'Nationality':str,
                                'Image Link':str,
                                'Age':float,
                                'Height(in cm)':float,
                                'Weight(in kg)':float,
                                'TotalStats':float,
                                'BaseStats':float,
                                'Club Name':str,
                                'Wage(in Euro)':float,
                                'Release Clause':float,
                                'Club Position':str,
                                'Contract Until':str,
                                'Club Jersey Number':str,
                                'Joined On':int,
                                'On Loan':str,
                                'Preferred Foot':str,
                                'Weak Foot Rating':float,
                                'Skill Moves':float,
                                'International Reputation':float,
                                'National Team Name':str,
                                'National Team Image Link':str,
                                'National Team Position':str,
                                'National Team Jersey Number':str,
                                'Attacking Work Rate':str,
                                'Defensive Work Rate':str,
                                'Pace Total':float,
                                'Shooting Total':float,
                                'Passing Total':float,
                                'Dribbling Total':float,
                                'Defending Total':float,
                                'Physicality Total':float,
                                'Crossing':float,
                                'Finishing':float,
                                'Heading Accuracy':float,
                                'Short Passing':float,
                                'Volleys':float,
                                'Dribbling':float,
                                'Curve':float,
                                'Freekick Accuracy':float,
                                'LongPassing':float,
                                'BallControl':float,
                                'Acceleration':float,
                                'Sprint Speed':float,
                                'Agility':float,
                                'Reactions':float,
                                'Balance':float,
                                'Shot Power':float,
                                'Jumping':float,
                                'Stamina':float,
                                'Strength':float,
                                'Long Shots':float,
                                'Aggression':float,
                                'Interceptions':float,
                                'Positioning':float,
                                'Vision':float,
                                'Penalties':float,
                                'Composure':float,
                                'Marking':float,
                                'Standing Tackle':float,
                                'Sliding Tackle':float,
                                'Goalkeeper Diving':float,
                                'Goalkeeper Handling':float,
                                ' GoalkeeperKicking':float,
                                'Goalkeeper Positioning':float,
                                'Goalkeeper Reflexes':float,
                                'ST Rating':float,
                                'LW Rating':float,
                                'LF Rating':float,
                                'CF Rating':float,
                                'RF Rating':float,
                                'RW Rating':float,
                                'CAM Rating':float,
                                'LM Rating':float,
                                'CM Rating':float,
                                'RM Rating':float,
                                'LWB Rating':float,
                                'CDM Rating':float,
                                'RWB Rating':float,
                                'LB Rating':float,
                                        'CB Rating':float,
                                        'RB Rating':float,
                                        'GK Rating':float
                                        }
                                        )

# Set layout
st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center;'>Football Visualization Project</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>By Yash Pratap Solanky, Aditya Joseph James</h5>", unsafe_allow_html=True)


#st.header("Football Visualization Project")
#st.caption("By Yash Pratap Solanky, Aditya Joseph James")
st.subheader('Visualization of FIFA 23 in game player statistics')

expander = st.expander("Read me")
expander.write("""
    This visualization tool enables the user to compare player statistics across positions and attributes. The data is taken from the FIFA 23 game by EA sports.
    To start one needs to select the position that they are interested in. The user can then compare all the players across 
    and two dimensions available. The user can choose to color the scatter plot by any metric. They can also select a base
    player against whom they want to make a comparison. Once they have the scatter plot they can zoom into the plot to find 
    suitable alternate players for the position and then compare the player against the base player that they have selected.

    Use cases that this tool aims to solve: 
    1) Player replacement 
    2) Team strengthening
""")
col0, col1,col11, col2, col3,col4,col5 = st.columns(7)
col6,col7,col8=st.columns([1,1,1])

## Getting the list of positions so that it can be used in multiselect 


# with col00:
#     compare_player_ = st.selectbox('Compare player',player_list_compare,key="compare_player")

### postions select
x=list(base_data['Positions Played'])
t_pos_list=[]
for i in x:
    pos=i.split(",")
    t_pos_list.append(pos)

# x[0].split(",")
pos_list=list(set(sum(t_pos_list,[])))
#st.write(pos_list)
#multiselect button to select positions
with col0:
    options = st.multiselect('Select player positions',pos_list,default='CAM')
criteria="|".join(options)

#Choose x axis
plot_variable_scatter_x=["Overall", "Potential", "Value(in Euro)","Age","Height(in cm)", "Weight(in kg)", "TotalStats", "BaseStats","Wage(in Euro)", "Release Clause", "International Reputation", "Pace Total", "Shooting Total", "Passing Total","Dribbling Total", "Defending Total", "Physicality Total", "Crossing","Finishing", "Heading Accuracy", "Short Passing", "Volleys","Dribbling", "Curve", "Freekick Accuracy", "LongPassing", "BallControl","Acceleration", "Sprint Speed", "Agility", "Reactions", "Balance","Shot Power", "Jumping", "Stamina", "Strength", "Long Shots","Aggression", "Interceptions", "Positioning", "Vision", "Penalties","Composure", "Marking", "Standing Tackle", "Sliding Tackle","Goalkeeper Diving", "Goalkeeper Handling", " GoalkeeperKicking","Goalkeeper Positioning", "Goalkeeper Reflexes", "ST Rating","LW Rating", "LF Rating", "CF Rating", "RF Rating", "RW Rating","CAM Rating", "LM Rating", "CM Rating", "RM Rating", "LWB Rating","CDM Rating", "RWB Rating", "LB Rating", "CB Rating", "RB Rating","GK Rating"]
with col2:
    x_axis_var=st.selectbox("Choose x axis variable",plot_variable_scatter_x,index=13)
plot_variable_scatter_y=plot_variable_scatter_x.copy()
#plot_variable_scatter_y.remove(x_axis_var)
with col3:
    y_axis_var=st.selectbox("Choose y axis variable",plot_variable_scatter_y,index=14)
color_var_c=plot_variable_scatter_y.copy()
#color_var_c.remove(y_axis_var)
with col4:
    color_var_c=st.selectbox("Choose color variable",color_var_c,index=0)

color_template={"Original color palette":px.colors.sequential.Magma,
                "Reversed color palette":px.colors.sequential.Magma_r}

with col5:
    color_val=st.selectbox("Choose color option",list(color_template.keys()))

filter_base_bool = base_data['Positions Played'].str.contains(criteria)
cf_st = base_data[filter_base_bool]

# with col6:
#     slider_var=st.selectbox("Filter attribute",plot_variable_scatter_x,index=2)

# min_slider=int(min(cf_st_[slider_var]))
# max_slider=int(math.ceil(max(cf_st_[slider_var])))
# st.write(min_slider,"-----",max_slider)

# with col7:
#     slider_range = st.slider("Select filter range to modify scatterplot range:",value=(min_slider, max_slider))
# st.write(slider_range[0],"-----",slider_range[1])
# with col8:
#     st.write("Filter range")
#     st.write("Between ",str(round(slider_range[0]/1000000,1))+" M"," and ",str(round(slider_range[1]/1000000,1))+" M")
# cf_st=cf_st_[(cf_st_[slider_var]>=slider_range[0]) & (cf_st_[slider_var]<=slider_range[1])]
# st.write(cf_st)
# cf_st = base_data[filter_base_bool]

player_list=list(cf_st['Known As'])
player_list_compare=list(cf_st['Known As'])

with col1:
    base_player_ = st.selectbox('Select base player',player_list)
base_player=(base_player_)

# base_player_possible_clubs=base_data[base_data['Known As'].str.contains(base_player)]
base_player_possible_clubs=cf_st[cf_st['Known As'].str.contains(base_player)]

club_list_=list(base_player_possible_clubs['Club Name'])
# st.write(base_player_possible_clubs)
# st.write(club_list_)
with col11:
    club_list=st.selectbox('Select Club',club_list_)



# club_referrer
# cf_st = base_data[base_data['Positions Played'].isin(options)] 
scatter_title=y_axis_var+" vs "+ x_axis_var+" colored by "+color_var_c

#scatter_star=cf_st[cf_st['Known As'].str.contains(base_player)]
scatter_star=cf_st[(cf_st['Known As'].str.contains(base_player)) & (cf_st['Club Name'].str.contains(club_list))]


#st.write(criteria)
#st.write(cf_st)
#Start---- Plotting scatter plot for the selected positions
fig = px.scatter(cf_st, x=x_axis_var, y=y_axis_var,
                 #color=color_var_c,color_continuous_scale=px.colors.sequential.Magma_r,
                 color=color_var_c,color_continuous_scale=color_template[color_val],
                 width=820, height=700,opacity=0.5,size_max=30,
                 hover_data={'Known As':True,
                             'Wage(in Euro)':True,
                             'Release Clause':True
                             }
                 
                 )
fig.update_layout(title_text=scatter_title)
fig.update_layout({
                    'plot_bgcolor': 'rgba(242, 242, 242, 0.8)',
                    # 'plot_bgcolor': 'rgba(0,0, 0, 1)',
                    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                    })
fig.update_traces(marker={'size': 8}) 

fig.add_trace(go.Scatter(x=scatter_star[x_axis_var], y=scatter_star[y_axis_var],mode='markers',
                            marker_symbol='star',marker_size=15,showlegend=False,marker_color='rgb(152, 0, 123)'))

fig.update_layout(font=dict(size=20))

# st.write(fig)
#End---- Plotting scatter plot for the selected positions



col_scatter, col_radial = st.columns([1.5,1])
with st.container():
    #Scatter plot
    with col_scatter:
        #st.write(fig)
        st.plotly_chart(fig, use_container_width = True)

    #Radar plot
    with col_radial:
        radar_options={'Overall':['Known As','Pace Total','Shooting Total','Passing Total','Dribbling Total','Defending Total','Physicality Total'],
            'Attacking':['Known As','Crossing','Finishing','Heading Accuracy','Short Passing','Volleys'],
        'Skill':['Known As','Dribbling','Curve','Freekick Accuracy','LongPassing','BallControl'],
        'Movement':['Known As','Acceleration','Sprint Speed','Agility','Reactions','Balance'],
        'Power':['Known As','Shot Power','Jumping','Stamina','Strength','Long Shots'],
        'Mentality':['Known As','Aggression','Interceptions','Positioning','Vision','Penalties','Composure'],
        'Defending':['Known As','Marking','Standing Tackle','Sliding Tackle'],
        'Goalkeeping':['Known As','Goalkeeper Diving','Goalkeeper Handling','GoalkeeperKicking','Goalkeeper Positioning','Goalkeeper Reflexes']
        }

        compare_player = st.selectbox('Compare player',player_list_compare,key="compare_player_rad")
        c_player_df=base_data[base_data['Known As'].str.contains(compare_player)]
        c_player_club_list_=list(c_player_df['Club Name'])
        
        c_player_club=st.selectbox('Select Club',c_player_club_list_,key='Compare player club')
        attri=st.selectbox('Attribute',list(radar_options.keys()),key='attribute')

        p_base=base_data[(base_data['Known As'].str.contains(base_player)) & (base_data['Club Name'].str.contains(club_list))]
        p2=base_data[(base_data['Known As'].str.contains(compare_player)) & (base_data['Club Name'].str.contains(c_player_club))]
        # st.write(p_base) # View data frame R. James and A. Sanchez
        # st.write(p2) # View data frame
        stat_key=attri
        radar_metric=(radar_options[stat_key])

        p_base=p_base[radar_options[stat_key]]
        p2=p2[radar_options[stat_key]]


        radar_metric.remove('Known As')

        p_base_long=pd.melt(p_base,id_vars='Known As', value_vars=radar_metric,var_name='Metric',value_name='Score')
        p2_long=pd.melt(p2,id_vars='Known As', value_vars=radar_metric,var_name='Metric',value_name='Score')

        radar_df=pd.concat([p_base_long,p2_long])
        fig_radar = px.line_polar(radar_df, r='Score', color='Known As', theta='Metric', line_close=True, 
            start_angle=0,width=700,height=500,color_discrete_sequence = px.colors.qualitative.Vivid)
        fig_radar.update_layout({
                            'polar_bgcolor': 'rgba(242, 242, 242,1)',
                            'paper_bgcolor': 'rgba(0, 0, 0,0)',
                            
                            })
        fig_radar.update_layout(title_text='Player Comparisons')
        fig_radar.update_layout(legend=dict(
                            yanchor="top",
                            y=0.4,
                            xanchor="right",
                            x=-0.1
                        ))
        fig_radar.update_layout(font=dict(size=19))

        #st.write(fig_radar)
        st.plotly_chart(fig_radar, use_container_width=True)



## Start------- Goals
    st.subheader('Visualization of FIFA 2018 World Cup goals')
    expander = st.expander("Read me")
    expander.write("""
        In the below visualization we visualize the goals scored during the 2018 world cup. In order to view the goals we need
        to select the stage of the world cup (i.e. group stage, round of 16 etc.). We next select the match based on the two
        countries that played the game. Finally we are able to see the goals as they were scored.
        The visualization use cases that this tool aims to solve are: 
        1) Final location of the football with respect to the goal post as seen from the penalty spot 
        2) Pitch view of the location from where the goal was scored and where the ball ended up
        3) Table with the goals ordered by minute
        4) Goals by minute
        
        * Plot does not reflect own goals due to unavailability of data

    """)
    goal_img = Image.open("ball1.png")

    goals_data = pd.read_csv("goals_27Nov.csv",
                        dtype={'match_id':str,
                        'player':str,
                        'possession_team':str,
                        'shot_end_location':str,
                        'possession_team_id':float,
                        'z':float,
                        'x':float,
                        'y':float,
                        'match':str,
                        'competition_stage':str,
                        'score':str
                            },sep="|"
                            )
    goals_data['competition_stage'] = goals_data['competition_stage'].str.replace('3rd Place Final','3rd Place')

    col_stage,col_match,col_score=st.columns([1,1,1])
    with col_stage:
        stages=[*set(list(goals_data['competition_stage']))]
        stage_goal=st.selectbox('Select stage',stages,key='WC stage')
    with col_match:
        stage_flt=goals_data[(goals_data['competition_stage'].str.contains(stage_goal))]
        matches=[*set(list(stage_flt['match']))]
        match_goal=st.selectbox('Select match',matches,key='WC match')
    with col_score:
        final_goal=stage_flt[(stage_flt['match'].str.contains(match_goal))]
        score=list(set(list(final_goal['score'])))[0]
        st.write("Final Score")
        st.write(score)
    #st.write("Plot does not reflect own goals due to unavailabilty of data")


    col_goal_chart,col_goal_button,col_goal_table  = st.columns([1,1,0.5])
    with st.container():

        with col_goal_button:
            ### Plot Pitch view

            pitch = Pitch(linewidth=0.5)
            fig, ax = pitch.draw(figsize=(3,2))


            import plotly.tools as tls
            from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
            import matplotlib.pyplot as plt
            from mplsoccer import Pitch, VerticalPitch

            # fig, ax = plt.subplots()

            # tmp = set()
            #
            # tmp.add(final_goal["possession_team"].iloc[0])
            #
            # for i, row in final_goal.iterrows():
            #
            #     if row["possession_team"] in tmp:
            #
            #         plt.plot(row["location_x"], row["location_y"], marker="o", markersize=6, color="yellow", alpha=0.4,
            #                  label=(row["minute"], row["player"]))
            #         plt.plot(row["z"], row["x"], marker="o", markersize=1, color="yellow")
            #         plt.plot((row["location_x"], row["z"]), (row["location_y"], row["x"]), color="yellow", alpha=0.1)
            #
            #     else:
            #
            #         plt.plot(row["location_x"], row["location_y"], marker="o", markersize=6, color="blue", alpha=0.4,
            #                  label=(row["minute"], row["player"]))
            #         plt.plot(row["z"], row["x"], marker="o", markersize=1, color="Blue")
            #         plt.plot((row["location_x"], row["z"]), (row["location_y"], row["x"]), color="blue", alpha=0.1)

                # fig.legend(["Goals"])

            plotly_fig = tls.mpl_to_plotly(fig)

            # go.Figure(layout=layout, data=go.Scatter(x=[113], y=[31]))

            plotly_fig.add_shape(type="circle",
                                 x0=50, y0=50, x1=70, y1=30,
                                 line_color="lightgrey",
                                 )



            plotly_fig.update_layout({
                'paper_bgcolor':'rgba(250, 249, 246,1)',
                'plot_bgcolor':'rgba(0,0,0,0)',
                'xaxis': {'visible': False},
                'yaxis': {'visible': False},
                'width':700, 'height': 400
            })
            #plotly_fig.update_layout(font=dict(size=1), hovermode='closest', hoverlabel = dict(namelength = -1))

            plotly_fig.add_trace(
                go.Scatter(x=final_goal['location_x'], y=final_goal['location_y'], mode='markers',
                           text=final_goal['player'],
                           marker=dict(color=final_goal.possession_team_id, size=20, opacity=1),
                           hovertemplate="""Player: %{text} <br><extra></extra>"""), )


            plotly_fig.add_trace(
                go.Scatter(x=final_goal['z'], y=final_goal['x'], mode='markers',
                           text=final_goal['player'],
                           marker=dict(color=final_goal.possession_team_id, size=5, opacity=1),
                           hovertemplate="""Player: %{text} <br><extra></extra>"""), )

            for i, row in final_goal.iterrows():

                plotly_fig.add_shape(type="line", x0=row['z'], y0=row['x'], x1=row['location_x'],
                                 y1=row['location_y'], line=dict(color="black", width=1) , opacity=0.2)

            #plotly_fig.update_layout(font=dict(size=20), title="Final location of football with respect to goal pitch")


            #iplot(plotly_fig)

            #st.write(plotly_fig)

            st.subheader("Goals scored - Pitch view")

            st.plotly_chart(plotly_fig, use_container_width=True)




        with col_goal_table:
            keep_cols=['minute','player','possession_team']
            goal_summary=final_goal[keep_cols]
            goal_summary.sort_values(by=['minute'],inplace=True)
            goal_summary.rename(columns={'minute': 'Minute', 'player': 'Player','possession_team':'Team'}, inplace=True)
            goal_summary=goal_summary[['Minute','Player','Team']]
            goal_summary['Minute'] = goal_summary['Minute'].astype(int)

            st.subheader("Goals scored")


            # CSS to inject contained in a string
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.table(goal_summary)



        with col_goal_chart:
            #### Plot goal
            layout = go.Layout(
                paper_bgcolor='rgba(250, 249, 246,1)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=700,height=400
            )

            fig_goal = go.Figure(layout=layout)
            # Set axes ranges
            fig_goal.update_xaxes(range=[35.9, 45])
            fig_goal.update_yaxes(range=[0, 2.7])

            fig_goal.add_shape(type="line",x0=36, y0=0, x1=36, y1=2.67,line=dict(color="black",width=5))
            fig_goal.add_shape(type="line",x0=44.22, y0=0, x1=44.22, y1=2.67,line=dict(color="black",width=5))
            fig_goal.add_shape(type="line",x0=35.978, y0=2.67, x1=44.24, y1=2.67,line=dict(color="black",width=5))
            fig_goal.add_trace(go.Scatter(x=final_goal['x'], y=final_goal['y'],mode='markers',text=final_goal['player'],
                                marker=dict(color=final_goal.possession_team_id,size=20,opacity=1),
                                hovertemplate="""Player: %{text} <br><extra></extra>"""),
                                )

            for i, row in final_goal.iterrows():
                # country_iso = row["iso_alpha2"]
                fig_goal.add_layout_image(
                    dict(
                        # source=f"https://raw.githubusercontent.com/matahombres/CSS-Country-Flags-Rounded/master/flags/{country_iso}.png",
                        source=goal_img,
                        xref="x",
                        yref="y",
                        xanchor="center",
                        yanchor="middle",
                        x=row["x"],
                        y=row["y"],
                        sizex=0.35,
                        sizey=0.35,
                        # sizing="contain",
                        opacity=0.8,
                        layer="above"
                    )
                )

            fig_goal.update_yaxes(visible=False, showticklabels=False)
            fig_goal.update_xaxes(visible=False, showticklabels=False)
            #fig_goal.update_layout(font=dict(size=20), title="Final location of football with respect to goal post")

            st.subheader("Goals scored - Goalpost view")

            st.plotly_chart(fig_goal, use_container_width=True)
            #st.write(fig_goal)


##game progess
final_goal['summary']= 500
# st.write(final_goal)

layout = go.Layout(
                paper_bgcolor='rgba(250, 249, 246,1)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=1600,height=250
            )

fig_summary = go.Figure(layout=layout)
# Set axes ranges
match_end=max(max(final_goal['minute'])+5,93)
# st.write(match_end)
fig_summary.update_xaxes(range=[-3, match_end],tickvals=np.arange(0, match_end,10))

fig_summary.add_trace(go.Scatter(x=final_goal['minute'], y=final_goal['summary'],mode='markers',text=final_goal['player'],
                    marker=dict(color=final_goal.possession_team_id,size=47.5,opacity=1),customdata=['possession_team']))
                    

for i, row in final_goal.iterrows():
    
    fig_summary.add_layout_image(
        dict(
            
            source=goal_img,
            xref="x",
            yref="y",
            xanchor="center",
            yanchor="middle",
            x=row["minute"],
            y=row["summary"],
            sizex=3.5,
            sizey=3.5,
            # sizing="contain",
            opacity=0.8,
            layer="above"
        )
    )

fig_summary.update_yaxes(visible=False, showticklabels=False)
fig_summary.update_xaxes(visible=True, showticklabels=True)
fig_summary.update_traces(
    hovertemplate="<br>".join([
        "Player: %{text}",
        "Minute: %{x}","<extra></extra>"
    ])
)
# st.write(fig_summary)

fig_summary.update_layout(font=dict(size=20),xaxis_title="Time in minutes",)
#st.write(fig_summary)

st.subheader("Goal Timeline")
st.plotly_chart(fig_summary, use_container_width=True)

