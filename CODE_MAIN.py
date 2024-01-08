from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
import asyncio
import aiohttp
import json
import plotly.graph_objects as go
import requests
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import base64
import shutil
from io import BytesIO


app = FastAPI()
templates = Jinja2Templates(directory="")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    page = """
    <!DOCTYPE html>
        <html>
        <head>
            <title>SpaceX Launches</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                  integrity="sha384-0mSbJDEHial+OrHiFpD2PyXuUPtkvv3p3qOvE1z3sf5VOpPr/CGOt8tf1KFUiSN0"
                  crossorigin="anonymous">
            <style>
                /* Change the font for the page */
                body {
                    font-family: Arial, sans-serif;
                    background-image: url("/static/vrush.jpg");
        
                    background-size: cover;
                    background-color: #cccccc;
        
                }
                
                                       body {{
                background-image: url('/static/vrush.jpg');
                background-size: cover;
            }}
            /* Set opacity of the background image */
            body::before {{
                content: '';
                display: block;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                opacity: 0.5;
                background-color: #000;
            }}

        
                /* Style the header */
                .navbar {
                    border-radius: 0;
                    margin-bottom: 0;
                    list-style-type: none;

                }
        
                .navbar-brand {
                    color: #51e2f5;
                    font-size: 1.5em;
                    list-style-type: none;

                }
        
                .navbar-toggler {
                    border: none;
                    list-style-type: none;

                }
        
                .nav-link:hover {
                    color: #fff;
                    background-color: #007bff;
                }
        
                .nav-item.active .nav-link {
                    color: #fff;
                    background-color: #007bff;
                    
                }
        
                .nav-link {
                    color: #8458B3;
                    transition: all 0.3s ease-in-out;
                    
                    
                }
                .nav-link1{
                color: #8458B3;
                    transition: all 0.3s ease-in-out;
                    float: right;

                 }
        
                /* Add some padding to the body */
                .container {
                    padding-top: 60px;
                    margin-bottom: 30px;

                }
        
                /* Style the title */
                h1 {
                    color: #fff;
                    font-size: 3em;
                    font-weight: 700;
                    text-align: center;
                    margin-bottom: 10px;
                    font-family: 'Montserrat', sans-serif;
                }
              
                .navbar-nav li {
                              list-style: none;
                            }
            </style>
        </head>
        <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
            <div class="container">
                <a class="navbar-brand" href="/">Launches</a>
               
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/launches">All Launches</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/rockets">Rockets</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/live_map">Launch Sites</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/explore_planets">Explore Planets</a>
                        </li>
                         <li class="nav-item">
                            <a class="nav-link" href="/space-info">Space knowledge</a>
                        </li>
                        <li class="nav-item ml-auto"> 
                        <a class="nav-link1" href="/contact_us">Contact Us</a>
                        </li>   
                        
                         <li class="nav-item ml-auto"> 
                        <a class="nav-link" href="/applicant_results">Applicant results</a>
                        </li>  
                    
                        
                    </ul>
                    
                </div>
             </div>
            </nav>
            <div class="container">
                <h1>Welcome to CSV Aerospace</h1>
            </div>
         </body>
        </html>
        """
    return HTMLResponse(content=page)



#Endpoint to display launches
@app.get("/launches", response_class=HTMLResponse)
async def all_launches(request: Request):
    # Create a launch frequency plot using get_launch_frequency() function
    launch_frequency_plot = get_launch_frequency()

    response = requests.get("https://api.spacexdata.com/v4/launches")
    launches = response.json()
    page = f"""
        <!DOCTYPE html>
        <html>
          <head>
            <title>SpaceX Launches - All Launches</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-0mSbJDEHial+OrHiFpD2PyXuUPtkvv3p3qOvE1z3sf5VOpPr/CGOt8tf1KFUiSN0" crossorigin="anonymous">
            <style>
              body {{
                font-family: Arial, sans-serif;
                background-color: #a0d2eb;

              }}
              h1{{
              font-weight: 00;
              text-align: center;
              margin-bottom: 30px;
              font-family: 'Montserrat', sans-serif; }}
              .navbar {{
    
              background-color: #111;
              border-radius: 0;
              margin-bottom: 0;
            }}
            .navbar-toggler {{
              padding: 50px 100px;

            }}
            
            
            .nav-link:hover {{
                    color: #fff;
                    background-color: #007bff;
                }}
                .nav-item.active .nav-link {{
                    color: #fff;
                    background-color: #007bff;
                }}
                
            .nav-link {{
                    color: #fff;
                    transition: all 0.3s ease-in-out;
                }}
                            
            /* Add some padding to the body */
            .container {{
              padding-top: 60px;
              margin-bottom: 30px;
            }}
            .navbar-brand {{
              font-size: 1.5em;
              float: right;
              color: white;
              max-width: 200px;
              margin:  auto;
              padding: 20px;
              display: flex;
              flex-wrap: wrap;
              }}
                .navbar-brand {{
                            background-color: white;
                            color: black;
                            padding: 5px 10px;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
                        .navbar-brand:hover {{
                            background-color: #a0d2eb;
                        }}              
                 .navbar {{
                            background-color: black;
                            color: black;
                            padding: 10px 20px;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
                       
            </style>
          </head>
          <body>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
                <div class="container1">
                    <a class="navbar-brand" href="/">Home</a>
                </div>
                <div class="collapse navbar-collapse" id="navbarNav">
                  <ul class="navbar-nav">
                    <li class="nav-item">
                      <a class="nav-link" href="/launches">All Launches</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="/launches/upcoming">Upcoming Launches</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="/launches/past">Past Launches</a>
                    </li>
                    
               
                  </ul>
                </div>
              </div>
            </nav>
             <div id="plot"></div>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <script>
                fetch('/launch_frequency')
                    .then(response => response.json())
                    .then(data => {{
                        const plotDiv = document.getElementById('plot');
                        Plotly.newPlot(plotDiv, JSON.parse(data));
                    }})
                </script>
            <div class="container">
              <h1>SpaceX Launches - All Launches</h1>
              <table class="table table-striped table-bordered">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Flight Number</th>
                    <th>Mission Name</th>
                    <th>Launch Date</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
        """
    for launch in launches:
        page += f"""
                  <tr>
                    <td>{launch['id']}</td>
                    <td>{launch['flight_number']}</td>
                    <td>{launch['name']}</td>
                    <td>{launch['date_utc']}</td>
                    <td>{launch['details']}</td>
                  </tr>
            """
    page += """
                </tbody>
              </table>
            </div>
          </body>
        </html>
        """
    return HTMLResponse(content=page)


#Endpoint to display upcoming launches
@app.get("/launches/upcoming", response_class=HTMLResponse)
async def upcoming_launches(request: Request):
    response = requests.get("https://api.spacexdata.com/v4/launches/upcoming")
    launches = response.json()
    page = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>SpaceX Launches - Upcoming Launches</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-0mSbJDEHial+OrHiFpD2PyXuUPtkvv3p3qOvE1z3sf5VOpPr/CGOt8tf1KFUiSN0" crossorigin="anonymous">
        <style>
              body {{
                font-family: Arial, sans-serif;
                background-color: #5cbdb9;

              }}
              h1{{
              font-weight: 00;
              text-align: center;
              margin-bottom: 30px;
              font-family: 'Montserrat', sans-serif; }}
              .navbar {{
    
              background-color: #111;
              border-radius: 0;
              margin-bottom: 0;
            }}
            
            .navbar-brand {{
              font-size: 1.5em;
            }}
            
            .navbar-toggler {{
              border: none;

            }}
            
            .nav-link:hover {{
                    color: #fff;
                    background-color: #007bff;
                }}
                .nav-item.active .nav-link {{
                    color: #fff;
                    background-color: #007bff;
                }}
                
            .nav-link {{
                    color: #fff;
                    transition: all 0.3s ease-in-out;
                }}
                            
            /* Add some padding to the body */
            .container {{
              padding-top: 60px;
              margin-bottom: 30px;
            }}
             .navbar-brand {{
              font-size: 1.5em;
              float: right;
              color: white;
              max-width: 200px;
              margin:  auto;
              padding: 20px;
              display: flex;
              flex-wrap: wrap;
              }}
                .navbar-brand {{
                            background-color: white;
                            color: black;
                            padding: 5px 10px;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
                        .navbar-brand:hover {{
                            background-color: #5cbdb9;
                        }}              
                 .navbar {{
                            background-color: black;
                            color: black;
                            padding: 10px 20px;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
            </style>
        </head>
        <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
            <div class="container1">
                <a class="navbar-brand" href="/">Home</a>
            </div>
            <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav">
                <li class="nav-item">
                  <a class="nav-link" href="/launches">All Launches</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/launches/upcoming">Upcoming Launches</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/launches/past">Past Launches</a>
                </li>
                
              </ul>
            </div>
          </div>
        </nav>
        <div class="container">
          <h1>SpaceX Launches - Upcoming Launches</h1>
          <table class="table table-striped table-bordered">
            <thead>
              <tr>
                <th>ID</th>
                <th>Flight Number</th>
                <th>Mission Name</th>
                <th>Launch Date</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
    """
    for launch in launches:
        page += f"""
              <tr>
                <td>{launch['id']}</td>
                <td>{launch['flight_number']}</td>
                <td>{launch['name']}</td>
                <td>{launch['date_utc']}</td>
                <td>{launch['details']}</td>
              </tr>
        """
    page += """
            </tbody>
          </table>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=page)

#Endpoint to display past launches
@app.get("/launches/past", response_class=HTMLResponse)
async def past_launches(request: Request):
    response = requests.get("https://api.spacexdata.com/v4/launches/past")
    launches = response.json()
    page = f"""
        <!DOCTYPE html>
        <html>
          <head>
            <title>SpaceX Launches - Past Launches</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-0mSbJDEHial+OrHiFpD2PyXuUPtkvv3p3qOvE1z3sf5VOpPr/CGOt8tf1KFUiSN0" crossorigin="anonymous">
            <style>
              body {{
                font-family: Arial, sans-serif;
                background-color: #d0bdf4;

              }}
              h1{{
              font-weight: 00;
              text-align: center;
              margin-bottom: 30px;
              font-family: 'Montserrat', sans-serif; }}
              .navbar {{
    
              background-color: #111;
              border-radius: 0;
              margin-bottom: 0;
            }}
            
            .navbar-brand {{
              font-size: 1.5em;
            }}
            
            .navbar-toggler {{
              border: none;

            }}
            
            .nav-link:hover {{
                    color: #fff;
                    background-color: #007bff;
                }}
                .nav-item.active .nav-link {{
                    color: #fff;
                    background-color: #007bff;
                }}
                
            .nav-link {{
                    color: #fff;
                    transition: all 0.3s ease-in-out;
                }}
                            
            /* Add some padding to the body */
            .container {{
              padding-top: 60px;
              margin-bottom: 30px;
            }}
             .navbar-brand {{
                          font-size: 1.5em;
                          float: right;
                          color: white;
                          max-width: 200px;
                          margin:  auto;
                          padding: 20px;
                          display: flex;
                          flex-wrap: wrap;
                          }}
                .navbar-brand {{
                            background-color: white;
                            color: black;
                            padding: 5px 10px;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
                        .navbar-brand:hover {{
                            background-color:#d0bdf4 ;
                        }}              
                 .navbar {{
                            background-color: black;
                            color: black;
                            padding: 10px 20px;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
        </style>
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
                <div class="container1">
                    <a class="navbar-brand" href="/">Home</a>
                </div>
                <div class="collapse navbar-collapse" id="navbarNav">
                  <ul class="navbar-nav">
                    <li class="nav-item">
                      <a class="nav-link" href="/launches">All Launches</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="/launches/upcoming">Upcoming Launches</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="/launches/past">Past Launches</a>
                    </li>
                   
                  </ul>
                </div>
              </div>
            </nav>
            <div class="container">
              <h1>SpaceX Launches - Past Launches</h1>
              <table class="table table-striped table-bordered">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Flight Number</th>
                    <th>Mission Name</th>
                    <th>Launch Date</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
        """
    for launch in launches:
        page += f"""
                  <tr>
                    <td>{launch['id']}</td>
                    <td>{launch['flight_number']}</td>
                    <td>{launch['name']}</td>
                    <td>{launch['date_utc']}</td>
                    <td>{launch['details']}</td>
                  </tr>
            """
    page += """
                </tbody>
              </table>
            </div>
          </body>
        </html>
        """
    return HTMLResponse(content=page)


async def fetch_launchpad(session, url):
    async with session.get(url) as response:
        return await response.json()

@app.get('/live_map', response_class=HTMLResponse)
async def get_live_map(request: Request):
    # Send a GET request to get the launch data
    response = requests.get("https://api.spacexdata.com/v4/launches/")
    launches = response.json()

    # Create an empty list to store the launchpad locations and names
    launchpad_locations = []

    # Create a list of launchpad URLs to fetch using aiohttp
    launchpad_urls = [f"https://api.spacexdata.com/v4/launchpads/{launch['launchpad']}" for launch in launches]

    # Fetch launchpad data asynchronously using aiohttp
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_launchpad(session, url) for url in launchpad_urls]
        launchpad_data = await asyncio.gather(*tasks)

    # Store the launchpad name and location in the list
    for data in launchpad_data:
        launchpad_locations.append({
            'name': data['full_name'],
            'latitude': data['latitude'],
            'longitude': data['longitude']
        })

    # Create a Plotly figure with a mapbox scatter plot and all the launchpad locations
    fig = go.Figure(
        go.Scattermapbox(
            lat=[location['latitude'] for location in launchpad_locations],
            lon=[location['longitude'] for location in launchpad_locations],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14,
                color='red',
            ),
            text=[location['name'] for location in launchpad_locations],
            hoverinfo='text',
        )
    )

    # Set up the mapbox layout
    fig.update_layout(
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1Ijoiam9uLXNub3ciLCJhIjoiY2xmMW9mczV0MGFkdzN5bGhqcDZ6YjcwayJ9.11myOgTfwGjLI854lHyu1A',
            center=go.layout.mapbox.Center(
                lat=launchpad_locations[0]['latitude'],
                lon=launchpad_locations[0]['longitude'],
            ),
            zoom=3,
        ),
    )
    fig.update_layout(
        title={
            'text': 'Available Launch-sites',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': 'green','size': 24, 'family': 'Arial, sans-serif'}
        }
    )
    # Define the HTML and CSS code
    html_content = f"""
            <html>
                <head>
                    <style>
                        /* Define the CSS for the map container */
                        #map-container {{
                            height: 1000px;
                            width: 100%;
                        }}
                        body {{
                            margin: 0;
                            padding: 0;
                            font-family: Arial, sans-serif;
                            background-image: url("/static/vrush1.jpeg");

                        }}
                        .container1 {{
                            display: flex;
                            justify-content: flex-end;
                            padding: 20px;
                        }}
                        .navbar {{
                            background-color: white;
                            color: black;
                            padding: 10px 20px;
                            border-radius: 5px;
                            text-decoration: none;
                        }}
                        .navbar:hover {{
                            background-color: black;
                            color: white;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container1">
                        <a class="navbar" href="/">Home</a>
                    </div>
                    <div id="map-container">{fig.to_html()}</div>
                </body>
            </html>

    """

    return HTMLResponse(content=html_content, status_code=200)

def get_launch_frequency():
    @app.get("/launch_frequency")
    async def get_launch_frequency():
        # Retrieve the SpaceX launch data from the API endpoint
        response = requests.get("https://api.spacexdata.com/v4/launches")
        data = json.loads(response.text)

        # Convert launch dates to datetime objects
        launch_dates = []
        for launch in data:
            launch_dates.append(launch["date_utc"])

        # Create a dictionary to store the number of launches per year
        launches_per_year = {}
        for date in launch_dates:
            year = date[:4]
            if year in launches_per_year:
                launches_per_year[year] += 1
            else:
                launches_per_year[year] = 1

        # Create a list of x and y values for the plot
        x_values = list(launches_per_year.keys())
        y_values = list(launches_per_year.values())

        # Create the plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Launch Frequency'))

        # Set the plot title and axis labels
        fig.update_layout(title='Launch Frequency over Time', xaxis_title='Year', yaxis_title='Number of Launches')

        # Set the plot colors and font size
        fig.update_traces(marker=dict(color='rgb(255, 102, 102)', size=10),
                          line=dict(color='rgb(255, 102, 102)', width=2))
        fig.update_layout(font=dict(size=16))
        fig.update_traces(marker=dict(color='black', size=10),
                          line=dict(color='black', width=2))
        fig.update_layout(
            title='Launch Frequency over Time',
            xaxis_title='Year',
            yaxis_title='Number of Launches',
            plot_bgcolor='#a0d2eb',  # Set the plot background color
            paper_bgcolor='#a0d2eb'  # Set the paper background color
        )

        # Return the plot as HTML response
        return fig.to_json()


get_launch_frequency()

@app.get("/rockets", response_class=HTMLResponse)
async def get_rockets(request: Request):
    api_url = "https://api.spacexdata.com/v4/rockets"
    api_response = requests.get(api_url)
    api_data = api_response.json()
    rockets = []

    for rocket in api_data:
        rocket_info = {
            "name": rocket["name"],
            "photos": rocket["flickr_images"],
            "id" : rocket["id"]
        }
        rockets.append(rocket_info)
    return templates.TemplateResponse("/static/rockets.html", {"request": request, "rockets": rockets})


@app.get("/rockets/{rocket_id}", response_class=HTMLResponse)
async def get_rocket_info(request: Request, rocket_id: str):
    api_url = 'https://api.spacexdata.com/v4/rockets/'+rocket_id
    api_response = requests.get(api_url)
    rocket = api_response.json()
    if isinstance(rocket, dict):  # Check if api_data is a dictionary
        rocket_info = {
            "name": rocket["name"],
            "description": rocket["description"],
            "engines": rocket["engines"]["type"],
            "active": rocket["active"],
            "cost_per_launch": rocket["cost_per_launch"],
            "height": rocket["height"]["feet"],
            "diameter": rocket["diameter"]["meters"],
            "mass": rocket["mass"]["kg"],
            "first_flight": rocket["first_flight"],
            "success_rate_pct": rocket["success_rate_pct"],
            "wikipedia": rocket["wikipedia"]
    }
    return templates.TemplateResponse("/static/rocket_info.html", {"request": request, "rocket": rocket_info})







# Define constants for image filenames
MARS_IMAGE = "mars_image.png"
PLANET_DISTANCES = "planet_distances.png"
SPACE_EVENTS = "space_events.png"


@app.get("/explore_planets", response_class=HTMLResponse)
async def read_root():
    html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Solar System</title>
            <style>
                body {
                    font-family: Verdana, Bold;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background-image: url("https://lh3.googleusercontent.com/CQ5E3OEjAw-vn8lj9ZDrXN5bdBzisatZsftO2aPLK8AoaDGygqAZGH8Bmxzqdt-RXryTsR6yCOIMIsYcWYLl_fSj0hZ1swlZqMQ2pZPI1NBicCk05EVQ9oazE0iniIAccNBvA9ym3JA=w2400");
                    background-repeat: no-repeat;
                    background-size: cover;
                    background-color: #FFFFF0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white; /* Set the text color to white */
                }
                .content {
                    background-color: rgba(250, 250, 250, 0.3);
                    padding: 20px;
                    max-width: 600px;
                    text-align: center;
                }

                h1, p {
                    text-align: center;
                    font-size: 15px;
                }

            </style>
        </head>
        <body>
            <div class="content">
            <h1>Welcome to the Solar System!</h1>
            <p style="font-size: 16px;">Are you curious about the secrets of our solar system's celestial bodies? Get ready to explore the history of a planets, when were they discovered and physical characteristics of these captivating orbs, including their orbit, and more. Discover their idiosyncrasies, from their axial tilt to their average periapsis, and satisfy your thirst for astronomical knowledge.<p>
        </div>

        <ul>
            <li><a href="/planets" style="font-size: 50px; font-weight: bold; color: orange;">Planets</a></li>
        </ul>

        </body>
        </html>
    """
    return html_content


@app.get("/planets", response_class=HTMLResponse)
async def read_planet():
    html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Planet Information</title>
            <style>

                body {
                    font-family: Verdana, Bold;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background-image: url("https://lh3.googleusercontent.com/pgJOYSU7liun78v_OOkeDnXBwD5uu2FeFGV5x-NdwyjbNzDrZ-yT1pyVXauo8ZIQP7FKlJ4Otw1UxtnVHNWQA4BySM2Z8CNsc2dcZ5BHsdbGdoVfGtBJtlh5oML7qNDLnUArbsFMCbk=w2400");
                    background-repeat: no-repeat;
                    background-size: cover;
                    background-color: black;
                    color: white; /* Set the text color to white */
                }
                .content {
                    background-color: rgba(250, 250, 250, 0.3);
                    padding: 20px;
                    max-width: 600px;
                    text-align: center;
                }

                h1, p {
                    text-align: center;
                    font-size: 30px;
                }
                .images-container {
                    display: flex;
                    justify-content: center;
                    margin-top:20px;
                }

                .left-text {
                    text-align: left;
                    width: 10%;
                    float: left;
                }

                .right-text {
                    text-align: left;
                    width: 10%;
                    float: right;
                } 
                .navbar-brand {
              font-size: 1.5em;
                  float: right;
              margin:  auto;
              padding: 20px;
              display: flex;
              flex-wrap: wrap;
              background-color: white;
                            color: black;
                            padding: 10px 20px;
                            border-radius: 5px;
                            text-decoration: none;

            }
                        .navbar-brand:hover {
                            background-color: yellow;
                            color: black;
                        }
            </style>

        </head>
        <body>
            <div class="container1">
                <a class="navbar-brand" href="/">Home</a>
            </div>
            <div class="content">
                <h1>The planets</h1>
                <p style="font-size: 25px;">Dataset of the planets: <p>
                <p style="font-size: 25px;"> Earth, Mercury, Venus, Mars.<p>

                <h2 style="font-size: 15px;">id, name, english name, isPlanet, moons, semimajorAxis, perihelion, aphelion, eccetricity, inclination, mass, vol</h2>
                <h2 style="font-size: 15px;">density, gravity, escape, meanRadius, equaRadius, polarRadius, flattening, dimension, sideralOrbit, aroundPlanet, discoveredBy, discoveryDate, azialTilt, avgPeriapsis, longAscNode, bodyType.</h2>
                <div class="image-container">
            <img src="https://lh3.googleusercontent.com/89frUR8CVz4Lq-uChVrwkp_V6XW4ftk-m2dUFBhAhaBD_7B0rJrwXxTZ04g0TVUhPHL4-MRss3JONBk7V-OgtsZZoNzIEMno7waZrtiFLFr8nd6-n7RwXOf11GFBQgsxeAErqK-Cde4=s140-p-k" alt="Earth">
            <img src="https://lh3.googleusercontent.com/bbO6fbq4y_JJzXP2p3Fc1YIzFwE6VKPbMcQ4V96sM__IOcugi_CXkFVePda4IqhCgoiJrJT5MW44CayXr7NRLanyul-0Dw2NYMyMHbj-2VnIXv9hG9A_VjgvPm6p5f68910FZSV73Fg=s140-p-k " alt="Mercury">
            <img src="https://lh3.googleusercontent.com/ZvLcucV_1ZYEB3gm7nqMXEjmlZ4SzdL_ed6tjOXO1qcS7D4vjh7UhBbbRtpq1XXFea3Dls5zOf3EDHx3gtdANpz54BjyMRkiQdQaJHus0quEOANz2AC04h4Hy9c2TA9nf7fjdWWGp1s=s140-p-k" alt="Venus">
            <img src="https://lh3.googleusercontent.com/gKIbSyoC3DtcFqKZaKq-JfREh2s3kLQssauAeNn651XUsE7rRGc8mOJ3iCcqYyMT_Q65MmhztegYUiA5yAHKlj5iWJmzuv4zJ0EXYbSya0MF18ieIub4BcP5G9hC8IeBez54wm8D0-4=s150-p-k" alt="Mars">
        </div>
        <br>
        <a href="/space-info" style="font-size: 20px; color: yellow;">More about Space</a>

        </body>
        </html>

    """
    return html_content


@app.get("/space-info", response_class=HTMLResponse)
async def get_space_info():
    try:
            # Save the images in the "static" folder
            mars_image_path = f"static/{MARS_IMAGE}"
            planet_distances_path = f"static/{PLANET_DISTANCES}"
            space_events_path = f"static/{SPACE_EVENTS}"

            # Get the Mars image and save it to a file
            image_url = "https://www.nasa.gov/sites/default/files/thumbnails/image/pia23623-1041.jpg"
            image_data = requests.get(image_url).content
            with open(mars_image_path, "wb") as f:
                f.write(image_data)
        # Display a message and the image
            html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Space Information</title>
                </head>
                <body>
                    <h1>Space Information</h1>
                    <p>Image 1: Concept for a Mars base, with ice home </p>
                    <img src="/static/{MARS_IMAGE}" alt="Mars Image" width="500">
            """
        # Generate the heatmap of distances between planets
            url = "https://nineplanets.org/distance-between-planets/"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table')
            df = pd.read_html(str(table))[0]
            distances = df.pivot(index='From', columns='To', values='AU')
            plt.figure()
            sns.heatmap(distances, cmap='coolwarm', annot=True, fmt='.2f')
            plt.title('Distance Between Planets (AU)', fontsize=12)
            plt.xlabel('To')
            plt.ylabel('From')

            # Save the heatmap as a base64 encoded string
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            planet_distances_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            html_content += f"""
                    <p>The second plot generated shows a heatmap of the distances between planets in astronomical units (AU). The heatmap highlights the varying distances between planets and provides insights into the challenges of interplanetary travel.</p>
                    <img src="/static/{planet_distances_path}" alt="Planet Distances Heatmap" width="500">
            """
            # Generate the scatter plot of top space travel events
            url = "https://www.iexplore.com/articles/activity-guides/space-travel/top-10-overall"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            ol_element = soup.find("ol")
            list_items = ol_element.find_all("li")
            events = []
            years = []
            for item in list_items:
                event = item.find("strong").text
                year = re.search(r"\d{4}", item.text)
                if year:
                    year = year.group()
                events.append(event)
                years.append(year)
            data = {"Event": events, "Year": years}
            table = pd.DataFrame(data)
            table = table.sort_values("Year")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.scatter(table["Year"], range(len(table)), s=100, color="blue")
            for i, event in enumerate(table["Event"]):
                ax.annotate(event, (table["Year"].iloc[i], i), xytext=(10, 0), textcoords="offset points")
            ax.set_title("Top 10 Space Travel Events")
            ax.set_xlabel("Year")
            ax.set_ylabel("Event Rank")
            # Save the scatter plot as a base64 encoded string
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            space_events_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Space Information</title>
                        <style>
                       body {{
                background-image: url('/static/sifa.jpg');
                background-size: cover;
            }}
            /* Set opacity of the background image */
            body::before {{
                content: '';
                display: block;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                opacity: 0.5;
                background-color: #000;
            }}


                                                h1 {{
                                    color: #008080;
                                    font-size: 36px;
                                    font-family: Arial, sans-serif;
                                }}
                                p {{
                                    color: #333;
                                    font-size: 18px;
                                    line-height: 1.5;
                                    font-family: Arial, sans-serif;
                                    color: white;
                                }}
                                img {{
                                    display: block;
                                    margin: 20px auto;
                                }}
                                
                            .navbar-brand {{
                                          font-size: 1.5em;
                                          float: right;
                                            margin:  auto;
                                            padding: 20px;
                                            display: flex;
                                            flex-wrap: wrap;
                                            background-color: white;
                                                        color: black;
                                            			font-family: Arial, sans-serif;

                            padding: 10px 20px;
                            border-radius: 5px;
                            text-decoration: none;

            }}
                        .navbar-brand:hover {{
                            background-color: #008080;
                            color: white;
                        }}
                            </style>
                    </head>
                    <body>
                    <div class="container1">
                        <a class="navbar-brand" href="/">Home</a>
                        </div>
                        <h1>Space Information</h1>
                        <p>Image 1: Concept for a Mars base, with ice home (see attached mars_image.png)</p>
                        <img src="/static/{MARS_IMAGE}" alt="Mars Image" width="500">
                        <p>The second plot generated shows a heatmap of the distances between planets in astronomical units (AU). The heatmap highlights the varying distances between planets and provides insights into the challenges of interplanetary travel.</p>
                        <img src="data:image/png;base64,{planet_distances_base64}" alt="Planet Distances Heatmap" width="500">
                        <p>The fourth plot created is a scatter plot that shows the top ten space travel events and their corresponding year. The scatter plot provides a clear visualization of the events and their respective years. The plot highlights significant events such as the first man-made object to orbit the Earth and the landing on the Moon.</p>
                        <img src="data:image/png;base64,{space_events_base64}" alt="Space Travel Events Scatter Plot" width="500">
                    </body>
                    </html>
                """

            return html_content

    except Exception as e:
        return f"An error occurred: {str(e)}"
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:54:32 2023

@author: user
"""
from fastapi import UploadFile, File, Request


df = pd.read_json('https://data.nasa.gov/resource/9g7e-7hzz.json')

df.center.value_counts()

@app.get('/centers')
def get_center(name: str):
    shortcut = {
        'marshall': "Marshall Space Flight Center",
        'kennedy': "Kennedy Space Center",
        'langley': "Langley Research Center",
        'glenn': "Glenn Research Center",
        'jet': "Jet Propulsion Lab",
        'goddard': "Goddard Space Flight Center",
        'stennis': 'Stennis Space Center',
        'ac_management': "NASA Aircraft Management Center",
        'michoud': 'Michoud Assembly Facility',
        'ames': 'Ames Research Center',
        'wallops': 'Wallops Flight Facility/GSFC',
        'armstrong': 'Armstrong Flight Research Center',
        'johnson': 'Johnson Space Center'
    }
    df = pd.read_json('https://data.nasa.gov/resource/9g7e-7hzz.json')

    if name in shortcut:
        return {'center': shortcut[name]}
        # return(df[df.center == shortcut[name]])
    return {"Data": "Not Found"}

@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("uploadfile.html", {"request": request})


@app.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.get("/contact_us", response_class=HTMLResponse)
async def upload(request: Request):
    text = open("contact_us.txt", encoding='utf-8')

    my_output = "<h1>Contact Us</h1>"
    my_output += '<img src ="https://cie.spacefoundation.org/wp-content/uploads/2022/07/Astronaut.jpg" width="400">'
    my_output += '<br><br><br>'
    for line in text:
        my_output += line + '<br>'

    return templates.TemplateResponse("uploadfile.html", {"request": request})


name1 = 'kennedy'

shortcut = {
    'marshall': "Marshall Space Flight Center",
    'kennedy': "Kennedy Space Center",
    'langley': "Langley Research Center",
    'glenn': "Glenn Research Center",
    'jet': "Jet Propulsion Lab",
    'goddard': "Goddard Space Flight Center",
    'stennis': 'Stennis Space Center',
    'ac_management': "NASA Aircraft Management Center",
    'michoud': 'Michoud Assembly Facility',
    'ames': 'Ames Research Center',
    'wallops': 'Wallops Flight Facility/GSFC',
    'armstrong': 'Armstrong Flight Research Center',
    'johnson': 'Johnson Space Center'
}
df[df.center == shortcut[name1]]


@app.get("/applicant_results")
async def read_txt_file():
    with open("static/file_rank_output.txt") as f:
        content = f.read()
    return {"content": content}