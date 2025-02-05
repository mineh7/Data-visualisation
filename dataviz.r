# Part 1: Data Cleaning and Exploration (R)

library(dplyr)

# 1. Loading the dataset and checking the first 5 rows.
data <- read.csv('/mnt/data/crime_data.csv')
head(data)

# 2. Identifing columns with missing values and their respective counts and dropping columns where more than 50% of the data is missing.
missing_counts <- colSums(is.na(data))
missing_counts[missing_counts > 0]

# Dropping columns with more than 50% missing data
threshold <- nrow(data) * 0.5
data_cleaned <- data[, colSums(is.na(data)) < threshold]

# 3. Converting DATE OCC column to datetime format. Extracting year, month, day. Create new column for the hour using TIME OCC.
data_cleaned$DATE_OCC <- as.Date(data_cleaned$DATE_OCC, format = "%m/%d/%Y")
data_cleaned$Year <- format(data_cleaned$DATE_OCC, "%Y")
data_cleaned$Month <- format(data_cleaned$DATE_OCC, "%m")
data_cleaned$Day <- format(data_cleaned$DATE_OCC, "%d")

# Assuming TIME OCC is in HHMM format
data_cleaned$Hour <- as.numeric(substr(sprintf("%04d", data_cleaned$TIME_OCC), 1, 2))

# 4. Filtering dataset for crimes in 2023 and BURGLARY in Crm Cd Desc.
crimes_2023 <- filter(data_cleaned, Year == 2023)
burglary_2023 <- filter(crimes_2023, grepl("BURGLARY", Crm.Cd.Desc, ignore.case = TRUE))

# 5. Grouping by AREA NAME, calculate total number of crimes and average victim age and sorting by total crimes.
grouped_area <- data_cleaned %>% 
  group_by(AREA.NAME) %>% 
  summarise(Total_Crimes = n(), Avg_Victim_Age = mean(Vict.Age, na.rm = TRUE)) %>% 
  arrange(desc(Total_Crimes))

print(grouped_area)

# Part 3: Further Exploration 

# 1. Grouping by Month and count number of crimes
crimes_by_month <- data_cleaned %>% 
  group_by(Month) %>% 
  summarise(Total_Crimes = n())

print(crimes_by_month)

# 2. Counting the number of crimes where a weapon was used
weapon_crimes_count <- sum(!is.na(data_cleaned$Weapon.Used.Cd))
print(weapon_crimes_count)

# 3. Grouping by Premis Desc and count number of crimes
crimes_by_premis <- data_cleaned %>% 
  group_by(Premis.Desc) %>% 
  summarise(Total_Crimes = n())

print(crimes_by_premis)

# Part 4: Advanced Analysis 

# Creating Severity Score
data_cleaned <- data_cleaned %>% 
  mutate(Severity_Score = ifelse(!is.na(Weapon.Used.Cd), 5, 0) +
                           ifelse(grepl("BURGLARY", Crm.Cd.Desc, ignore.case = TRUE), 3, 1))

# Grouping by AREA NAME and find total severity score
severity_by_area <- data_cleaned %>% 
  group_by(AREA.NAME) %>% 
  summarise(Total_Severity_Score = sum(Severity_Score, na.rm = TRUE))

print(severity_by_area)
