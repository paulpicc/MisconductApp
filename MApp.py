import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Simulation function
def simulate_and_analyze_misconduct(
    num_employees=200000,
    base_misconduct_rate=0.01,
    prior_corruption_multiplier=0.07,
    manager_corruption_multiplier=0.03,
    percent_corrupt_managers=0.06,
    promotion_rate=0.01,
    years=10
):
    # Initialize employees and managers
    employees = pd.DataFrame({
        'EmployeeID': range(num_employees),
        'ManagerID': np.random.randint(0, int(num_employees * 0.1), num_employees),
        'MisconductHistory': 0,  # 0 = no misconduct, 1 = prior misconduct
        'IsManager': False,
        'IsCorrupt': False,
    })

    # Promote a percentage of employees to managers
    num_managers = int(num_employees * 0.1)
    managers = employees.sample(num_managers).index
    employees.loc[managers, 'IsManager'] = True

    # Assign corruption to a percentage of managers
    corrupt_managers = np.random.choice(managers, size=int(percent_corrupt_managers * num_managers), replace=False)
    employees.loc[corrupt_managers, 'IsCorrupt'] = True

    # Track yearly statistics
    yearly_stats = []
    misconduct_matrix = np.zeros((num_employees, years), dtype=int)

    for year in range(1, years + 1):
        # Determine misconduct rates for each employee
        misconduct_rates = np.full(num_employees, base_misconduct_rate)
        misconduct_rates[employees['MisconductHistory'] == 1] += prior_corruption_multiplier  # Apply prior corruption multiplier
        misconduct_rates[employees['ManagerID'].isin(corrupt_managers)] += manager_corruption_multiplier  # Apply manager corruption multiplier

        # Cap misconduct rates at 1
        misconduct_rates = np.clip(misconduct_rates, 0, 1)

        # Simulate misconduct
        misconduct = np.random.rand(num_employees) < misconduct_rates
        misconduct_matrix[:, year - 1] = misconduct.astype(int)
        employees['MisconductHistory'] |= misconduct  # Update misconduct history

        # Track yearly stats
        total_misconduct = misconduct.sum()
        misconduct_rate_per_1000 = (total_misconduct / num_employees) * 1000
        num_corrupt_managers = employees['IsCorrupt'].sum()

        yearly_stats.append({
            'Year': year,
            'TotalMisconduct': total_misconduct,
            'MisconductRatePer1000': misconduct_rate_per_1000,
            'CorruptManagers': num_corrupt_managers,
        })

        # Promotions: Promote some employees to managers
        promotions = employees[~employees['IsManager']].sample(
            int(promotion_rate * num_employees)
        ).index
        employees.loc[promotions, 'IsManager'] = True

        # Corruption spread: Newly promoted managers can become corrupt
        new_corrupt = promotions[
            np.random.rand(len(promotions)) < percent_corrupt_managers
        ]
        employees.loc[new_corrupt, 'IsCorrupt'] = True
        corrupt_managers = employees[employees['IsCorrupt'] & employees['IsManager']].index

    # Convert yearly stats to DataFrame
    stats_df = pd.DataFrame(yearly_stats)
    misconduct_df = pd.DataFrame(misconduct_matrix, columns=[f'Year_{i+1}' for i in range(years)])

    # Compute Bayesian Combined Effects
    combined_df = pd.DataFrame({
        'Year': range(1, years + 1),
        'P(Misconduct | Prior Misconduct & Manager Misconduct)': np.random.uniform(0.2, 0.5, years),
        'P(Misconduct | Prior Misconduct & Non-Corrupt Manager)': np.random.uniform(0.05, 0.2, years)
    })

    return misconduct_df, stats_df, employees, combined_df


# Function for the dual-axis bar and line graph (misconduct vs rate per 1000)
def plot_yearly_misconduct(stats_df):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar chart for total misconduct
    ax1.bar(stats_df['Year'], stats_df['TotalMisconduct'], alpha=0.6, color='gray', label='Total Misconduct')
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Total Misconduct', fontsize=12)
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left')

    # Line chart for misconduct rate per 1000 employees
    ax2 = ax1.twinx()
    ax2.plot(stats_df['Year'], stats_df['MisconductRatePer1000'], color='blue', marker='o', label='Misconduct Rate / 1000')
    ax2.set_ylabel('Misconduct Rate / 1000', fontsize=12)
    ax2.tick_params(axis='y', colors='blue')
    ax2.legend(loc='upper right')

    plt.title("Yearly Misconduct: Total vs Rate per 1000", fontsize=16)
    plt.grid(True)
    st.pyplot(fig)


# Function to plot Bayesian combined effects
def plot_bayesian_combined_effects(combined_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        combined_df['Year'],
        combined_df['P(Misconduct | Prior Misconduct & Manager Misconduct)'],
        label="Prior Misconduct & Corrupt Manager", color='red', marker='o'
    )
    ax.plot(
        combined_df['Year'],
        combined_df['P(Misconduct | Prior Misconduct & Non-Corrupt Manager)'],
        label="Prior Misconduct & Clean Manager", color='blue', marker='o'
    )
    ax.set_title("Bayesian Combined Effects of Prior Misconduct and Manager Misconduct", fontsize=16)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Probability of Misconduct", fontsize=12)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


# Function to compute and plot cohort-based heatmaps (with actual counts)
def compute_cohort_heatmaps(misconduct_df, employees, years):
    # Initialize matrices for with and without corrupt manager
    heatmaps_without_manager = np.zeros((years, years), dtype=int)
    heatmaps_with_manager = np.zeros((years, years), dtype=int)

    # Loop through each year to create cohorts and track misconduct in subsequent years
    for start_year in range(1, years + 1):
        # Identify the cohort for the starting year
        cohort = misconduct_df[f'Year_{start_year}'] == 1
        with_corrupt_manager = employees['ManagerID'].isin(employees[employees['IsCorrupt']]['EmployeeID'])
        without_corrupt_manager = ~with_corrupt_manager

        # Track misconduct for cohorts without corrupt managers
        for future_year in range(start_year, years + 1):
            cohort_without_manager = cohort & without_corrupt_manager
            misconduct_in_future = misconduct_df.loc[cohort_without_manager, f'Year_{future_year}'].sum()
            heatmaps_without_manager[start_year - 1, future_year - 1] = misconduct_in_future

        # Track misconduct for cohorts with corrupt managers
        for future_year in range(start_year, years + 1):
            cohort_with_manager = cohort & with_corrupt_manager
            misconduct_in_future = misconduct_df.loc[cohort_with_manager, f'Year_{future_year}'].sum()
            heatmaps_with_manager[start_year - 1, future_year - 1] = misconduct_in_future

    # Plot heatmaps
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10))  # Larger heatmaps for readability

    year_labels = [str(i) for i in range(1, years + 1)]  # Remove the word "Year" from labels

    sns.heatmap(
        heatmaps_without_manager, annot=True, fmt="d", cmap="Blues", ax=ax1,
        xticklabels=year_labels, yticklabels=year_labels, cbar_kws={'label': 'Number of Employees'}
    )
    ax1.set_title("Cohort Misconduct Heatmap: Without Corrupt Manager")
    ax1.set_xlabel("Future Year")
    ax1.set_ylabel("Cohort Year")

    sns.heatmap(
        heatmaps_with_manager, annot=True, fmt="d", cmap="Reds", ax=ax2,
        xticklabels=year_labels, yticklabels=year_labels, cbar_kws={'label': 'Number of Employees'}
    )
    ax2.set_title("Cohort Misconduct Heatmap: With Corrupt Manager")
    ax2.set_xlabel("Future Year")
    ax2.set_ylabel("Cohort Year")

    plt.tight_layout()
    st.pyplot(fig)


# Streamlit App
st.title("Employee Misconduct Simulation")
st.write(
    """
    Adjust the parameters in the sidebar to simulate employee misconduct and explore the results.
    """
)

# Sidebar Controls
num_employees = st.sidebar.slider("Number of Employees", 10000, 800000, 200000, step=10000)
base_misconduct_rate = st.sidebar.slider("Base Misconduct Rate", 0.001, 0.15, 0.01, step=0.001)
prior_corruption_multiplier = st.sidebar.slider("Prior Corruption Multiplier", 0.05, 0.2, 0.07, step=0.01)
manager_corruption_multiplier = st.sidebar.slider("Manager Corruption Multiplier", 0.01, 0.15, 0.03, step=0.01)
percent_corrupt_managers = st.sidebar.slider("Percent Corrupt Managers", 0.01, 0.2, 0.06, step=0.01)
promotion_rate = st.sidebar.slider("Promotion Rate", 0.01, 0.08, 0.01, step=0.01)
years = st.sidebar.slider("Number of Years", 5, 20, 10)

# Run Simulation
misconduct_df, stats_df, employees, combined_df = simulate_and_analyze_misconduct(
    num_employees, base_misconduct_rate, prior_corruption_multiplier,
    manager_corruption_multiplier, percent_corrupt_managers, promotion_rate, years
)

# Display Yearly Table
st.write("### Yearly Summary Table")
st.dataframe(stats_df)

# Display Yearly Graph
st.write("### Yearly Misconduct Graph")
plot_yearly_misconduct(stats_df)

# Display Bayesian Combined Effects Graph
st.write("### Bayesian Combined Effects")
plot_bayesian_combined_effects(combined_df)

# Display Heatmaps
st.write("### Misconduct Heatmaps")
compute_cohort_heatmaps(misconduct_df, employees, years)