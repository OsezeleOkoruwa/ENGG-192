#Osezele Okoruwa
#05/30/24
#For the completion of ENGG 192


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Value of Statistical Life Year range from Viscusi(2003) citing Rosen(1998)
VSLY_min = 31000  #$ 
VSLY_max = 130000 #$

# Age distribution estimates from Vermont Department of Health for 2019 based on analyzed census data from 2010
population_0_17 = 114005
population_18_66 = 401349
population_67_up = 102621

#Life years are the years remaining that a person can likely contribute to the labor force
youth = 48              # life years
prime_work_age_min = 48 # life years remaining at 18
prime_work_age_max = 1  # life years remaining at 66
retiree = 0             # life years

# Reduction in life expectancy range for woodstoves from Orru(2022) and Martins(2023)
# Ranges were 0.1 to 0.63 and 0.1 to 0.5 life years lost respectively
life_expectancy_reduction_min = 0.1  #life years
life_expectancy_reduction_max = 0.63 #life years

# Number of simulations for Monte Carlo
num_simulations = 10000000
subsidy_cost = 800  # Fixed cost of subsidy per case --> Each case is a household. Household member assumptions below

# Simulated reduction in life expectancy
life_expectancy_reductions = list(np.random.uniform(life_expectancy_reduction_min, life_expectancy_reduction_max, num_simulations)[:, np.newaxis].flatten())
#flattening to flat list

# Simulated value of statistical life year for different age groups
VSLY = list(np.random.uniform(VSLY_min, VSLY_max, num_simulations))

prime_work_age = list(np.random.uniform(prime_work_age_min, prime_work_age_max, num_simulations))

# Calculation of the total damages per household
# Assumptions are based on the "average Vermont household" having 2.32 members.
# This suggests a higher proportion of adults without dependents to adults without dependents.
# Assuming that a quarter of retirees become dependents for their adult children the ratio of dependent youth to dependent retirees is below
deprat = population_0_17 / (population_0_17 + (population_67_up / 4))

damages_per_household = [ (a * b * ((youth * deprat * 0.32) + (c * 2))) for a, b, c in zip(VSLY, life_expectancy_reductions, prime_work_age)]
#zipping to combine the uniform samples for the calculation

# Calculate summary statistics
mean_damages = np.mean(damages_per_household)
median_damages = np.median(damages_per_household)
std_damages = np.std(damages_per_household)
range_damages = (np.min(damages_per_household), np.max(damages_per_household))


# Cost-benefit analysis
expected_value = mean_damages - 800
exceed_subsidy_count = np.sum(np.array(damages_per_household) > subsidy_cost)
proportion_exceed_subsidy = exceed_subsidy_count / num_simulations

# Data table for summary statistics
summary_statistics = {
    "Summary Statistics": ["Mean", "Median", "Standard Deviation", "Range (Minimum)", "Range (Maximum)", "Expected Value"],
    "Value($)": [mean_damages, median_damages, std_damages, range_damages[0], range_damages[1], expected_value]
}

df_summary_statistics = pd.DataFrame(summary_statistics)
df_summary_statistics["Value($)"] = df_summary_statistics["Value($)"].apply(lambda x: f"${x:,.2f}")


# Plotting the results. Used StackOverflow to figure out combining the plots
fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})

ax_box.boxplot(damages_per_household, vert=False)
ax_box.axvline(800, color='r', linestyle='-')

# Set labels for the boxplot & histogram
ax_box.set_xlabel('Damage per Household($ Millions)')
ax_box.set_ylabel('Boxplot')
sns.histplot(damages_per_household, bins=50, kde=True, ax=ax_hist)
ax_hist.set_xlabel('Damage per Household($ Millions)')
ax_hist.set_ylabel('# of Simulations')

# Create a figure for the summary statistics table
fig_table, ax_table = plt.subplots()

# Hide table sides 
ax_table.xaxis.set_visible(False)
ax_table.yaxis.set_visible(False)
ax_table.set_frame_on(False)

# Create the table
table = ax_table.table(cellText=df_summary_statistics.values, colLabels=df_summary_statistics.columns, cellLoc='center', loc='center')

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)

plt.subplots_adjust(left=0.2, top=0.9, bottom=0.2, right=0.9)

# Show the plot
plt.show()

print(f"Proportion of simulations where damages exceed subsidy cost: {proportion_exceed_subsidy:.2%}")
if proportion_exceed_subsidy > 0.5:
    print("The $800/case subsidy is effective.")
else:
    print("The $800/case subsidy is not effective.")

x = input()

ax_hist.legend()
plt.tight_layout()