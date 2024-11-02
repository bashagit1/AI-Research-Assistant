import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Set up the app layout and design
st.set_page_config(page_title="AI Research Assistant", layout="centered")  # Centered layout

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f0f8ff;  /* Light blue background */
        color: #2c3e50;  /* Darker text color */
    }
    .header {
        text-align: center;
        color: #2980b9; /* Blue header */
        font-size: 2em;  /* Slightly smaller header */
        margin: 10px;
    }
    .result {
        background-color: #ffffff; /* White background for results */
        border-radius: 10px;
        padding: 10px;  /* Smaller padding */
        margin: 5px 0;  /* Smaller margin */
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
    }
    .container {
        max-width: 800px; /* Limiting width */
        margin: 0 auto; /* Centering container */
        padding: 20px; /* Adding padding */
    }
    </style>
""", unsafe_allow_html=True)

# Add a cartoon animation
st.markdown("""
    <div style="text-align: center;">
        <img src="https://media.giphy.com/media/RbDKaczqWovIugyJmW/giphy.gif" alt="Cartoon Animation" style="width: 150px;"/>  <!-- Smaller animation -->
    </div>
""", unsafe_allow_html=True)

# Use a container for centering elements
with st.container():
    st.title("AI Research Assistant")
    st.header("Search for the latest information!")

    # Dropdown for country selection
    countries = {
        "United States": "United States",
        "Canada": "Canada",
        "United Kingdom": "United Kingdom",
        "Australia": "Australia",
        "India": "India",
        "Germany": "Germany",
        "France": "France",
        "Japan": "Japan",
        "China": "China",
        "Brazil": "Brazil",
        "Mexico": "Mexico",
        "South Africa": "South Africa",
        "Russia": "Russia",
        "Italy": "Italy",
        "Spain": "Spain",
        "Netherlands": "Netherlands",
        "Sweden": "Sweden",
        "Norway": "Norway",
        "Denmark": "Denmark",
        "Finland": "Finland",
        "Belgium": "Belgium",
        "Switzerland": "Switzerland",
        "New Zealand": "New Zealand",
        "Singapore": "Singapore",
        "Ireland": "Ireland",
        "Austria": "Austria",
        "Czech Republic": "Czech Republic",
        "Portugal": "Portugal",
        "Malaysia": "Malaysia",
        "Philippines": "Philippines",
        "Thailand": "Thailand",
        # Add more countries as needed
    }

    # User input for search query
    search_query = st.text_input("What would you like to research?", key="search_query", max_chars=50)

    # Dropdown for country selection
    selected_country = st.selectbox("Select Country", list(countries.keys()))

    if st.button("Get Search Results"):
        if search_query:
            url = "https://google.serper.dev/search"
            payload = json.dumps({
                "q": search_query,
                "location": countries[selected_country],  # Use the selected country
                "tbs": "qdr:d"
            })
            headers = {
                'X-API-KEY': SERPER_API_KEY,
                'Content-Type': 'application/json'
            }

            # Make the POST request
            response = requests.post(url, headers=headers, data=payload)

            # Check if the response is successful
            if response.status_code == 200:
                results = response.json()
                st.subheader("Search Results")

                # Check if organic results exist
                organic_results = results.get("organic", [])
                if organic_results:
                    for index, result in enumerate(organic_results):
                        title = result.get("title")
                        link = result.get("link")
                        snippet = result.get("snippet")
                        date = result.get("date")

                        # Display each result in a styled container
                        st.markdown(f"<div class='result'>", unsafe_allow_html=True)
                        st.write(f"{index + 1}. **{title}**: [Link]({link})")
                        st.write(snippet)
                        st.write(f"*Posted on:* {date}\n")
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("No organic results found for your query.")
            else:
                st.error("Failed to retrieve search results. Status code: " + str(response.status_code))
                st.write(response.text)  # Print the error message for debugging
        else:
            st.warning("Please enter a search query.")
