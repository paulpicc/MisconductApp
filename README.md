# MisconductApp
model of misconduct with variable inputs (base rates, multipliers, employees)
---
interactive app available @      https://misconductappdec2024hbsil.streamlit.app/

---
---




### Overview of the Misconduct Model

The misconduct model simulates employee behavior over multiple years, focusing on how organizational factors like prior misconduct, manager corruption, and promotion policies influence acts of misconduct. By modeling interactions between employees, managers, and organizational dynamics, the simulation provides insights into the prevalence and progression of workplace misconduct under different scenarios.

---

### Input Variables

#### **1. Number of Employees**
- **Description**: This sets the total number of employees in the organization. 
- **Slider Functionality**: The user can adjust the organization size from 10,000 to 800,000 employees.
- **Impact**: Larger organizations generate more data, increasing both the absolute number of misconduct cases and the complexity of manager-employee interactions. This allows for scaling the simulation to small or large institutions.

#### **2. Base Misconduct Rate**
- **Description**: The baseline probability of any employee committing misconduct in a given year, assuming no external influences.
- **Slider Functionality**: Adjustable from 0.001 (0.1%) to 0.15 (15%) misconduct likelihood.
- **Impact**: This variable reflects the inherent risk of misconduct in the organization. A higher base rate creates more misconduct across all employees, amplifying the effects of other factors like prior misconduct or corrupt managers.

#### **3. Prior Corruption Multiplier**
- **Description**: The increase in misconduct likelihood for employees with a history of prior misconduct.
- **Slider Functionality**: Ranges from 0.05 to 0.2, representing a 5% to 20% boost to the base misconduct rate.
- **Impact**: This variable models the tendency for repeat misconduct by individuals with a history of bad behavior. A higher multiplier intensifies the role of past behavior in predicting future misconduct.

#### **4. Manager Corruption Multiplier**
- **Description**: The increase in misconduct likelihood for employees reporting to a corrupt manager.
- **Slider Functionality**: Adjustable from 0.01 to 0.15, representing a 1% to 15% boost to the base misconduct rate.
- **Impact**: Employees under corrupt managers are more likely to commit misconduct. This variable captures how leadership behavior influences employee behavior and organizational culture.

#### **5. Percent Corrupt Managers**
- **Description**: The percentage of managers in the organization who are corrupt.
- **Slider Functionality**: Adjustable from 0.01 (1%) to 0.2 (20%) of all managers.
- **Impact**: A higher percentage of corrupt managers increases the likelihood of employees being exposed to corrupt leadership, amplifying misconduct throughout the organization.

#### **6. Promotion Rate**
- **Description**: The annual percentage of non-managers promoted to managerial positions.
- **Slider Functionality**: Ranges from 0.01 (1%) to 0.08 (8%).
- **Impact**: This variable influences the spread of corruption as newly promoted managers may adopt corrupt behaviors or carry forward positive or negative cultural influences. A higher promotion rate accelerates changes in leadership dynamics.

#### **7. Number of Years**
- **Description**: The duration of the simulation in years.
- **Slider Functionality**: Adjustable between 5 and 20 years.
- **Impact**: A longer simulation period allows for observing how misconduct trends evolve over time, including the compounding effects of prior misconduct, manager corruption, and organizational growth.

---

### Summary

This misconduct model is a powerful tool for exploring how workplace dynamics and organizational policies shape employee behavior over time. By adjusting key input variables, users can simulate a wide range of scenarios to understand the interplay between individual behavior, leadership influence, and systemic factors. The model not only highlights the importance of ethical leadership and effective policies but also provides actionable insights for mitigating misconduct and fostering a healthier organizational culture.
