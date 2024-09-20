#Categorizing dates into seasons by month

def filter_month(clean_date):
    import pandas as pd
    df=pd.DataFrame()
    """Categorizing dates into seasons by month"""
    if pd.isna(clean_date):
        return None
    month = clean_date.month
    if month in [12,1,2]:
        return "winter"
    elif month in [3,4,5]:
        return "spring"
    elif month in [6,7,8]:
        return "summer"
    elif month in [9,10,11]:
        return "autumn"

# Function to clean time format and handle formats like 10h30
def clean_time_format(time_str):
    import pandas as pd
    import re
    df=pd.DataFrame()
    """Function to clean time format and handle formats like 10h30"""
    if pd.isnull(time_str):
        return None
    clean_time = re.sub(r'[^\d:]', ':', time_str)
    try:
        time = pd.to_datetime(clean_time, format='%H:%M', errors='coerce').time()
        return time
    except:
        return None

# Function to categorize time into time slots
def categorize_cleaned_time(time):
    import pandas as pd
    df=pd.DataFrame()
    """Function to categorize time into time slots"""
    if pd.isnull(time):
        return 'Unknown'
    if pd.to_datetime('05:00', format='%H:%M').time() <= time < pd.to_datetime('12:00', format='%H:%M').time():
        return 'Morning'
    elif pd.to_datetime('12:00', format='%H:%M').time() <= time < pd.to_datetime('17:00', format='%H:%M').time():
        return 'Afternoon'
    elif pd.to_datetime('17:00', format='%H:%M').time() <= time < pd.to_datetime('20:00', format='%H:%M').time():
        return 'Evening'
    else:
        return 'Night'

# Creating a new categories for activities 
def activity_new (row):
    """Creating a new categories for activities"""
    if row["Activity"] == "Surfing":
        return "Surfing"
    elif row["Activity"] == "Swimming":
        return "Swimming"
    elif row["Activity"] == "Wading":
        return "Wading"
    elif row["Activity"] == "Fishing":
        return "Fishing"
    elif row["Activity"] == "Diving":
        return "Diving"
    else:
        return "Other activities"


# Standardize text for injuries
def clean_injuries(injury):
    import pandas as pd
    import re
    df=pd.DataFrame()
    """Standardize text for injuries"""
    if pd.isna(injury):
        return 'Unknown'
    injury = injury.lower()
    injury = re.sub(r'http\S+|www\S+', '', injury)  # Removing any URLs if present
    injury = re.sub(r'[^a-z\s]', '', injury)  # Removing numbers and special characters
    # Categorizing injuries based on keywords
    if 'fatal' in injury:
        return 'Fatal'
    elif 'bite' in injury:
        return 'Bite'
    elif 'laceration' in injury or 'cut' in injury:
        return 'Laceration'
    elif 'minor' in injury:
        return 'Minor injury'
    elif 'leg' in injury or 'foot' in injury or 'limb' in injury:
        return 'Lower Limb Injury'
    elif 'hand' in injury or 'arm' in injury:
        return 'Upper Limb Injury'
    elif 'no injury' in injury:
        return 'No injury'
    else:
        return 'Other'

# Modify the function to handle non-string entries
def clean_location(location):
    import re
    """Modify the function to handle non-string entries"""
    if isinstance(location, str):
        # Remove any text after a comma (county details) or redundant information such as "Off"
        cleaned = re.sub(r',.*', '', location)  # Remove everything after a comma
        cleaned = re.sub(r'Off\s*', '', cleaned)  # Remove any "Off" text
        cleaned = cleaned.strip()  # Strip any leading/trailing spaces
        return cleaned
    return location

# Function to calculate Chi-squared p-value and Cramér's V
def chi2_cramers_v(data, col1, col2):
    import pandas as pd
    import scipy.stats as stats
    import numpy as np
    """Create a contingency table"""
    contingency_table = pd.crosstab(data[col1], data[col2])

    """Perform the Chi-squared test"""
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

    """Calculate Cramér's V"""
    n = contingency_table.sum().sum()  # Total sample size
    cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))

    return p, cramers_v