import dash
from dash import dcc, html, callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import plotly.express as px
import mysql.connector

# Initialize Dash app
app = dash.Dash(__name__)

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="db"
)
cursor = conn.cursor()

# Layout of the dashboard
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Waste Reduction and Recycling Dashboard', style={'textAlign': 'center', 'color': 'green'}),
        html.Hr()
    ]),

    # Waste Tracking and Analytics Section
    html.Div([
        html.H2('Waste Tracking and Analytics', style={'color': 'blue'}),
        dcc.Graph(id='waste-chart')
    ]),

    # Recycling Education and Engagement Section
    html.Div([
        html.H2('Recycling Education and Engagement', style={'color': 'blue'}),
        html.Div([
            html.P('Learn more about recycling:', style={'marginBottom': '5px'}),
            dcc.Link('Recycling Guide', href='/recycling_guide', style={'marginRight': '10px'}),
            html.A('Watch Video', href="", target="_blank")
        ])
    ]),

    # Community Recycling Events and Initiatives Section
    html.Div([
        html.H2('Community Recycling Events and Initiatives', style={'color': 'blue'}),
        dcc.Dropdown(
            id='community-events-dropdown',
            options=[
                {'label': 'Earth Day Cleanup', 'value': 'earth_day_cleanup'},
                {'label': 'Clean India Green India', 'value': 'clean india green india'},
                {'label': 'E-Waste Collection Drive', 'value': 'e_waste_collection_drive'}
            ],
            value='earth_day_cleanup',
            style={'width': '50%', 'marginBottom': '10px'}
        ),
        html.Div(id='community-events-output')
    ]),

    # Recycled Materials Marketplace Section
    html.Div([
        html.H2('Recycled Materials Marketplace', style={'color': 'blue'}),
         html.Div([
             html.P('Learn more about recycling:', style={'marginBottom': '5px'}),
            dcc.Link('Sell', href='/Sell Products', style={'marginRight': '10px'}),
            html.A('Purchase', href='buyer.html', target="_blank")
        ])
    ]),

    # Complaints Section
    html.Div([
        html.H2('Complaints', style={'color': 'blue'}),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px 0'
            },
            multiple=True
        ),
        html.Div(id='image-preview'),
        dcc.Input(id='region-input', type='text', placeholder='Enter region', style={'margin': '10px 0'}),
        html.Button('Submit Complaint', id='submit-complaint', n_clicks=0, style={'margin': '10px 0'}),
        html.Div(id='complaint-status')
    ]),

    # Preview of Complaints Section
    html.Div([
        html.H2('Preview of Complaints', style={'color': 'blue'}),
        html.Div(id='complaints-preview')
    ])
])

# Callback to update waste chart
@app.callback(
    Output('waste-chart', 'figure'),
    [Input('waste-chart', 'id')]
)
def update_waste_chart(value):
    # Fetch data from database and create chart
    # Example:
    # df = pd.read_sql_query("SELECT * FROM waste_data", conn)
    # fig = px.bar(df, x='waste_type', y='quantity', color='waste_type', barmode='group')
    fig = px.bar(
        x=['Organic Waste', 'Plastic Waste', 'Metal Waste', 'Paper Waste'],
        y=[100, 150, 80, 120],
        color=['Organic Waste', 'Plastic Waste', 'Metal Waste', 'Paper Waste'],
        labels={'x': 'Waste Type', 'y': 'Quantity'},
        title='Waste Generation by Type',
        template='plotly_dark'
    )
    return fig

# Callback to display uploaded image preview
@app.callback(
    Output('image-preview', 'children'),
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename')]
)
def display_uploaded_image(contents, filename):
    if contents is not None:
        image_html = html.Img(src=contents[0], style={'width': '300px', 'height': 'auto'})
        return image_html
    else:
        return html.Div()

# Callback to submit complaint
@app.callback(
    Output('complaint-status', 'children'),
    [Input('submit-complaint', 'n_clicks')],
    [State('upload-image', 'contents'), State('region-input', 'value')]
)
def submit_complaint(n_clicks, image_contents, region):
    if n_clicks > 0 and image_contents is not None and region:
        # Save complaint details to database
        # Example:
        # cursor.execute("INSERT INTO complaints (image, region) VALUES (%s, %s)", (image_contents[0], region))
        # conn.commit()
        # Redirect to a new webpage after successful submission
        raise PreventUpdate()
        return dcc.Location(pathname='/complaint_submitted', id='complaint-redirect')
    elif n_clicks > 0:
        return html.Div('Please upload an image and specify the region.', style={'color': 'red'})
    else:
        return html.Div()

# Callback to display preview of complaints
@app.callback(
    Output('complaints-preview', 'children'),
    [Input('submit-complaint', 'n_clicks')]
)
def display_complaints_preview(n_clicks):
    # Fetch complaints from database and create preview
    # Example:
    # df = pd.read_sql_query("SELECT * FROM complaints", conn)
    # if not df.empty:
    #     complaints_preview = html.Div([html.Img(src=row['image'], style={'width': '300px', 'height': 'auto'}), html.P(f"Region: {row['region']}")] for index, row in df.iterrows())
    #     return complaints_preview
    return html.Div()

# Callback to redirect to new webpage after complaint submission
@app.callback(
    Output('complaint-redirect', 'pathname'),
    [Input('complaint-redirect', 'id')]
)
def redirect_to_complaint_submitted(pathname):
    return '/complaint_submitted'

if __name__ == '__main__':
    app.run_server(debug=True)
