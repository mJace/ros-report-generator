# Generate container CPU / Memory usage report for each container from ROS CSV file of OpenShift Cost Management Operator
![image](https://github.com/user-attachments/assets/153df075-7d90-487c-9076-bdddee322f90)

## Requirement
```
pip install pandas plotly
```

## Usage
1. Merge ROS CSV file
  - Put all of your ROS CSV file under same folder with scripts/merge.sh
  - Run merge.sh
  - Open merged.csv and sort column `interval_start` by ascending.  
3. Copy merged.csv as input.csv put it with `main.py`
4. Run `python3 main.py`
