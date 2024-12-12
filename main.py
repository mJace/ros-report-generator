import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import subprocess

def generate_container_report(df, container_name, namespace):
    """
    Generate an HTML report for a specific container
    """
    # Create a subplot figure with two charts
    fig = make_subplots(rows=2, cols=1, 
                        subplot_titles=(f'{container_name} - CPU Usage Metrics', 
                                        f'{container_name} - Memory Usage Metrics'),
                        vertical_spacing=0.1)

    # CPU Metrics Line Chart
    fig.add_trace(
        go.Scatter(x=df['interval_start'], 
                   y=df['cpu_usage_container_avg'], 
                   mode='lines', 
                   name='CPU Usage (Avg)'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df['interval_start'], 
                   y=df['cpu_request_container_avg'], 
                   mode='lines', 
                   name='CPU Request'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df['interval_start'], 
                   y=df['cpu_limit_container_avg'], 
                   mode='lines', 
                   name='CPU limit'),
        row=1, col=1
    )

    # Memory Metrics Line Chart
    fig.add_trace(
        go.Scatter(x=df['interval_start'], 
                   y=df['memory_usage_container_avg'] / (1024 * 1024), 
                   mode='lines', 
                   name='Memory Usage (Avg) MB'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['interval_start'], 
                   y=df['memory_request_container_avg'] / (1024 * 1024), 
                   mode='lines', 
                   name='Memory Request MB'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['interval_start'], 
                   y=df['memory_limit_container_avg'] / (1024 * 1024), 
                   mode='lines', 
                   name='Memory Limit MB'),
        row=2, col=1
    )

    # Update layout for better readability
    fig.update_layout(height=800, 
                      title_text=f'Container Resource Usage Report - {container_name}',
                      showlegend=True)
    
    # Remove x-axis titles and tick labels
    fig.update_xaxes(
        title_text='', 
        showticklabels=False,  # Hide x-axis tick labels
        row=1, col=1
    )
    fig.update_xaxes(
        title_text='', 
        showticklabels=False,  # Hide x-axis tick labels
        row=2, col=1
    )
    
    # Update y-axis titles
    fig.update_yaxes(title_text='CPU Usage', row=1, col=1)
    fig.update_yaxes(title_text='Memory Usage (MB)', row=2, col=1)

    # Generate summary text
    summary_text = f"""
    <h2>Resource Usage Summary for {container_name}</h2>
    <h3>Monitoring Period</h3>
    <ul>
        <li>Start Time: {df['interval_start'].min()}</li>
        <li>End Time: {df['interval_start'].max()}</li>
    </ul>
    <h3>CPU Usage</h3>
    <ul>
        <li>Average CPU Usage: {df['cpu_usage_container_avg'].mean():.6f}</li>
        <li>CPU Request (Avg): {df['cpu_request_container_avg'].max():.6f}</li>
        <li>CPU Limit (Avg): {df['cpu_limit_container_avg'].max():.6f}</li>
    </ul>
    <h3>Memory Usage</h3>
    <ul>
        <li>Average Memory Usage: {df['memory_usage_container_avg'].mean() / (1024 * 1024):.2f} MB</li>
        <li>Memory Request (Avg): {df['memory_request_container_avg'].min() / (1024 * 1024):.2f} MB</li>
        <li>Memory Limit (Avg): {df['memory_request_container_avg'].max() / (1024 * 1024):.2f} MB</li>
    </ul>
    """

    # Combine plot and summary
    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Container Resource Usage Report - {container_name}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        </style>
    </head>
    <body>
        {summary_text}
        <div id="plotly-chart"></div>
        <script>
            var plotlyChart = {fig.to_json()};
            Plotly.newPlot('plotly-chart', plotlyChart.data, plotlyChart.layout);
        </script>
    </body>
    </html>
    """

    return html_report

def generate_reports(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file, parse_dates=True)

    # Create output directory if it doesn't exist
    os.makedirs('container_reports', exist_ok=True)

    # Group by namespace and container_name
    grouped = df.groupby(['namespace', 'container_name'])

    # Generate reports for each unique container
    for (namespace, container_name), group_df in grouped:
        # Create a safe filename
        safe_filename = f"{namespace}_{container_name}_report.html".replace('/', '_').replace(' ', '_')
        report_path = os.path.join('container_reports', safe_filename)

        # Generate and save the report
        report = generate_container_report(group_df, container_name, namespace)
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"Generated report for {namespace}/{container_name}: {report_path}")

def main():
    # Run the merged_sort_csv.sh script
    try:
        subprocess.run(['bash', 'merged_sort_csv.sh'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing merged_sort_csv.sh: {e}")
        return
    except FileNotFoundError:
        print("merged_sort_csv.sh script not found in the current directory.")
        return
    
    # Use the sorted_merged.csv as the default input
    input_file = 'sorted_merged.csv'

    # Generate reports
    generate_reports(input_file)

if __name__ == '__main__':
    main()