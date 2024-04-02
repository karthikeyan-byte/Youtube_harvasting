# YouTube Data Analysis Tool

This Python script allows users to retrieve data from YouTube channels and perform various analyses on the channel information and video data obtained through the YouTube Data API.

## Features

- Fetch channel details including name, description, subscriber count, view count, and video count.
- Retrieve information about videos uploaded to a specific channel including title, description, publish date, view count, like count, and duration.
- Store the fetched data in CSV and JSON formats for further analysis or visualization.
- Perform data analysis tasks such as:
  - Displaying channel statistics
  - Showing top videos by views, likes, comments, etc.
  - Analyzing video duration and engagement metrics
  - Identifying channels with the most videos and views
  - Finding videos with the highest engagement metrics

## Usage

1. Clone the repository to your local machine:

    ```bash
    [git clone https://github.com/yourusername/youtube-data-analysis-tool.git](https://github.com/karthikeyan-byte/Youtube_harvasting)
    ```

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Obtain a YouTube Data API key from the [Google Developers Console](https://console.developers.google.com/).

4. Replace the placeholder API key in the script with your own API key:

    ```python
    api_key = 'YOUR_API_KEY_HERE'
    ```

5. Run the script:

    ```bash
    python youtube_data_analysis.py
    ```

6. Follow the prompts to enter the channel name and other required information.

## Requirements

- Python 3.x
- Google API Client Library for Python (`google-api-python-client`)
- `pandas`, `streamlit`, `sqlite3`, `numpy`, `pymongo`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the Google Developers team for providing the YouTube Data API.
- Special thanks to the developers of the libraries used in this project.
