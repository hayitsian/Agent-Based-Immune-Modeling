import plotly.express as px
import pandas as pd

data = {"2005": 11.2,
        "2006": 11.2,
        "2007": 10.7,
        "2008": 9.2,
        "2009": 7.8,
        "2010": 6.8,
        "2011": 6.1,
        "2012": 5.3,
        "2013": 5.2,
        "2014": 6.7,
        "2015": 13.8,}

df = pd.DataFrame({"Years": data.keys(), "Success Rate (%)": data.values()})
fig = px.bar(df, x="Years", y="Success Rate (%)")
fig.add_hline(y=df["Success Rate (%)"].mean(), line_width=7, annotation_text="Average", annotation_position="bottom", annotation_font_size=48, line_dash="dash", line_color="black")
fig.update_layout(font=dict(size=40), 
                  title=dict(text="Clinical Trial Success Rate in the US: 2005-2015", font=dict(size=80), x=0.5, y=1.0, xanchor="center"),
                  margin=dict(l=10, r=10, t=125, b=15))
fig.show()