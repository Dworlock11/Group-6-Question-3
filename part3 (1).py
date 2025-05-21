import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

sports_teams = {
                  'mens_swimming': [
                    'https://csidolphins.com/sports/mens-swimming-and-diving/roster/2023-2024?view=2',
                    'https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster?view=2',
                    "https://yorkathletics.com/sports/mens-swimming-and-diving/roster",
                    "https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster/2022-23?view=2",
                    "https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster/2021-22?view=2",
                    "https://mckbearcats.com/sports/mens-swimming-and-diving/roster/2023-24?view=2",
                    "https://ramapoathletics.com/sports/mens-swimming-and-diving/roster",
                    "https://oneontaathletics.com/sports/mens-swimming-and-diving/roster",
                    "https://binghamtonbearcats.com/sports/mens-swimming-and-diving/roster/2021-22?view=2",
                    "https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22"
                    ],
                  'mens_volleyball': [
                    'https://ccnyathletics.com/sports/mens-volleyball/roster?view=2',
                    'https://lehmanathletics.com/sports/mens-volleyball/roster?view=2',
                    "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster?view=2",
                    "https://johnjayathletics.com/sports/mens-volleyball/roster?view=2",
                    "https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster?view=2",
                    "https://www.huntercollegeathletics.com/sports/mens-volleyball/roster?view=2",
                    "https://yorkathletics.com/sports/mens-volleyball/roster"
                    
                    ],
                  'womans_swimming': [
                    'https://csidolphins.com/sports/womens-swimming-and-diving/roster/2022-2023?view=2',
                    "https://queensknights.com/sports/womens-swimming-and-diving/roster/2019-20",
                    "https://yorkathletics.com/sports/womens-swimming-and-diving/roster",
                    "https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?view=2",
                    "https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster/2022-23?view=2",
                    "https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster/2021-22?view=2",
                    "https://mckbearcats.com/sports/womens-swimming-and-diving/roster?view=2",
                    "https://ramapoathletics.com/sports/womens-swimming-and-diving/roster?view=2",
                    "https://keanathletics.com/sports/womens-swimming-and-diving/roster?view=2",
                    "https://oneontaathletics.com/sports/womens-swimming-and-diving/roster/2021-22?view=2"

                  ],
                  'womans_volleyball': [
                    "https://bmccathletics.com/sports/womens-volleyball/roster/2022?view=2",
                    "https://yorkathletics.com/sports/womens-volleyball/roster",
                    "https://hostosathletics.com/sports/womens-volleyball/roster/2022-2023?view=2",
                    "https://bronxbroncos.com/sports/womens-volleyball/roster/2021?view=2",
                    "https://queensknights.com/sports/womens-volleyball/roster?view=2",
                    "https://augustajags.com/sports/wvball/roster?view=2",
                    "https://flaglerathletics.com/sports/womens-volleyball/roster?view=2",
                    "https://pacersports.com/sports/womens-volleyball/roster",
                    "https://www.golhu.com/sports/womens-volleyball/roster?view=2"
                  ]

                }

def getData(url_list):
  """
    Scrape names and heights from a list of team roster URLs.

    Parameters:
    url_list (list): List of URLs for team rosters.

    Returns:
    DataFrame: A pandas DataFrame containing names and heights in inches.
    """
  # list to store heights
  heights = []
  names = []

  # vist each url in the list
  for url in url_list:

    # headers Source: https://www.zenrows.com/blog/web-scraping-headers#user-agent
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive'
      }

    # making a request to the server
    page = requests.get(url, headers=headers)

    # scrape data only if connection is successful
    if page.status_code == 200:
      # import the raw html into BeautifulSoup
      soup = BeautifulSoup(page.content, 'html.parser')

      # find all td tags with a class of height
      raw_heights = soup.select('td[class*="height"]')
      # find all td tags with a class of sidearm-table-player-name
      name_tags = soup.select('td[class*="sidearm-table-player-name"]')
      # extracting the name from the name tags
      for name_tag in name_tags:
        names.append(name_tag.get_text().strip())

      # extract the raw height from the list
      for raw_height in raw_heights:

        x = raw_height.get_text()
        # splitting the string by the '-'
        if x.split('-')[0] == '' or x.split('-')[1] == "":
          continue
        feet = float(x.split('-')[0]) * 12
        inches = float(x.split('-')[1])

        heights.append(feet + inches)
    print(heights.__len__())
    print(names.__len__())
    
  # organized the data as a dictionary
  data = {
      'Name': names,
      'Height': heights
  }

  df = pd.DataFrame(data)
  return df

def print_top_bottom_athletes(df, category):
    """
    Print the names and heights of the tallest and shortest athletes in a category.

    Parameters:
    df (DataFrame): DataFrame containing names and heights.
    category (str): The category/team name.

    Returns:
    None
    """

    # Convert names and heights to two lists
    names = df['Name'].tolist()
    heights = df['Height'].tolist()

    # Combine into a list of lists: [name, height]
    athletes = []
    for i in range(len(names)):
        athletes.append([names[i], heights[i]])

    # Sort athletes by height (ascending)
    for i in range(len(athletes)):
        for j in range(i + 1, len(athletes)):
            if athletes[i][1] > athletes[j][1]:
                temp = athletes[i]
                athletes[i] = athletes[j]
                athletes[j] = temp

    # Get cutoff for shortest 5 (including ties)
    if len(athletes) >= 5:
        min_cutoff = athletes[4][1]
    else:
        min_cutoff = athletes[-1][1]

    shortest = []
    for athlete in athletes:
        if athlete[1] <= min_cutoff:
            shortest.append(athlete)

    # Get cutoff for tallest 5 (including ties)
    athletes_reversed = athletes[::-1]  # reversed list
    if len(athletes_reversed) >= 5:
        max_cutoff = athletes_reversed[4][1]
    else:
        max_cutoff = athletes_reversed[-1][1]

    tallest = []
    for athlete in athletes_reversed:
        if athlete[1] >= max_cutoff:
            tallest.append(athlete)

    # Print tallest athletes
    print("\nTallest in", category)
    for person in tallest:
        print(person[0], "-", round(person[1], 1), "inches")

    # Print shortest athletes
    print("\nShortest in", category)
    for person in shortest:
        print(person[0], "-", round(person[1], 1), "inches")


def plot_avg_heights_with_pandas(avg_dict):
    """
    Plot a bar graph showing the average height for each team category.

    Parameters:
    avg_dict (dict): Dictionary mapping team categories to average height.

    Returns:
    None
    """
    avg_df = pd.DataFrame.from_dict(avg_dict, orient='index', columns=['Average Height'])
    avg_df.plot(kind='bar')
    plt.show()

def store_in_db(dataframes):
    """
    Store each team DataFrame into a SQLite database.

    Parameters:
    dataframes (dict): Dictionary mapping team categories to DataFrames.

    Returns:
    None
    """
    conn = sqlite3.connect("athletes.db")
    for team, df in dataframes.items():
        df.to_sql(team, conn, if_exists='replace', index=False)  # Replace existing table
    conn.close()

def main_function():
    """
    Main driver function to scrape data, compute statistics, print results,
    generate a plot, and store data into a database.

    Parameters:
    None

    Returns:
    None
    """
    avg_heights = {}      # Dictionary to store average height for each category
    dataframes = {}       # Dictionary to store DataFrames for each category

    for category, urls in sports_teams.items():
        print(f"\nProcessing: {category}")
        df = getData(urls)

        if not df.empty:
            avg = df['Height'].mean()  # Compute average height
            avg_heights[category] = avg
            print(f"Average height for {category}: {avg:.2f} inches")

            print_top_bottom_athletes(df, category)  # Print top/bottom 5 athletes

            dataframes[category] = df  # Save the DataFrame for further use
            df.to_csv(category + ".csv")
        else:
            print(f"No data found for {category}")

    plot_avg_heights_with_pandas(avg_heights)  # Visualize average heights
    store_in_db(dataframes)  # Save data to database

main_function()