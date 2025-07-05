#!/usr/bin/env python3
"""
Script to plot evaluation results from cache/evaluation_results.json
"""

# %%
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib as mpl

def load_evaluation_results(file_path="cache/evaluation_results.json"):
    """Load evaluation results from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def extract_metrics(data):
    """Extract accuracy metrics from the evaluation results"""
    results = []
    
    for tool_combo, metrics in data.items():
        # Extract tool names
        tool1 = metrics.get('tool1_name', 'Unknown')
        tool2 = metrics.get('tool2_name', 'Unknown')
        
        # Extract accuracy
        accuracy = metrics.get('accuracy', 0)
        
        # Skip entries with 0 accuracy (likely failed evaluations)
        if accuracy > 0:
            results.append({
                'tool_combo': tool_combo,
                'tool1': tool1,
                'tool2': tool2,
                'accuracy': accuracy,
                'precision': metrics.get('precision', 0),
                'recall': metrics.get('recall', 0),
                'specificity': metrics.get('specificity', 0)
            })
    
    return pd.DataFrame(results)

def plot_accuracy_histogram(df, save_path="evaluation_accuracy_histogram.png"):
    """Create histogram of accuracies"""
    plt.style.use('seaborn-v0_8-poster')
    mpl.rcParams['axes.edgecolor'] = '#333F4B'
    mpl.rcParams['axes.linewidth'] = 1.5
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titleweight'] = 'bold'
    mpl.rcParams['xtick.labelsize'] = 18
    mpl.rcParams['ytick.labelsize'] = 18
    mpl.rcParams['legend.fontsize'] = 18
    mpl.rcParams['font.family'] = 'DejaVu Sans'

    plt.figure(figsize=(16, 10))
    n, bins, patches = plt.hist(
        df['accuracy'], bins=8, alpha=0.85, color='#4A90E2', edgecolor='#222', linewidth=3
    )

    # Add value labels on top of each bar
    for i in range(len(n)):
        plt.text(
            (bins[i] + bins[i+1]) / 2, float(n[i]) + 0.5, f"{int(n[i])}",
            ha='center', va='bottom', fontsize=18, fontweight='bold', color='#333'
        )

    mean_accuracy = df['accuracy'].mean()
    plt.axvline(50, color='#D7263D', linestyle='--', linewidth=3, label=f'Random accuracy')

    plt.xlabel('Accuracy (%)', fontsize=24, fontweight='bold', labelpad=15)
    plt.ylabel('Number of Tool Combinations', fontsize=24, fontweight='bold', labelpad=15)
    plt.title('Distribution of Tool Combination Accuracies', fontsize=32, fontweight='bold', pad=30)
    plt.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)

    # Remove top/right spines for a cleaner look
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_facecolor('#F7F7F7')

    # Add statistics box
    stats_text = (
        f"Total combinations: {len(df)}\n"
        f"Mean accuracy: {mean_accuracy:.2f}%\n"
        f"Std deviation: {df['accuracy'].std():.2f}%"
    )
    plt.text(
        0.02, 0.98, stats_text, transform=plt.gca().transAxes,
        verticalalignment='top', fontsize=18,
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FFD600', alpha=0.95, lw=2)
    )

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=False)
    plt.show()
    print(f"Histogram saved as {save_path}")

def plot_accuracy_line(df, save_path="evaluation_accuracy_line.png"):
    """Create a beautiful line plot of accuracies in original order for hackathon slides"""
    plt.style.use('seaborn-v0_8-poster')  # Modern, clean style
    mpl.rcParams['axes.edgecolor'] = '#333F4B'
    mpl.rcParams['axes.linewidth'] = 1.2
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.titleweight'] = 'bold'
    mpl.rcParams['xtick.labelsize'] = 16
    mpl.rcParams['ytick.labelsize'] = 16
    mpl.rcParams['legend.fontsize'] = 16
    mpl.rcParams['font.family'] = 'DejaVu Sans'

    plt.figure(figsize=(18, 9))
    df_original = df.reset_index(drop=True)
    x = range(len(df_original))
    y = df_original['accuracy']

    # Main line plot
    plt.plot(x, y, marker='o', markersize=10, color='#0072B2', linewidth=3, alpha=0.85, label='Accuracy')

    # Mean and median lines
    plt.axhline(50, color='#D7263D', linestyle='--', linewidth=3, label=f'Random accuracy')

    # Annotate top performers
    top_performers = df_original.nlargest(5, 'accuracy')
    offset = 25
    for idx, row in top_performers.iterrows():
        tool1 = row['tool1'].replace('load_', '').replace('_report', '')
        tool2 = row['tool2'].replace('load_', '').replace('_report', '')
        plt.annotate(f"{tool1}\n{tool2}",
                     xy=(idx, row['accuracy']), xytext=(0, offset),
                     textcoords='offset points', fontsize=16, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF9C4', edgecolor='#FFD600', alpha=0.95, lw=2),
                     arrowprops=dict(arrowstyle='->', color='#333F4B', lw=2, connectionstyle='arc3,rad=0.2', alpha=0.7))
        offset = -offset

    plt.xlabel('Order of Evaluation', fontsize=20, fontweight='bold', labelpad=15)
    plt.ylabel('Accuracy (%)', fontsize=20, fontweight='bold', labelpad=15)
    plt.title('Tool Combination Accuracies', fontsize=32, fontweight='bold', pad=30)
    plt.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
    plt.grid(True, alpha=0.25, linestyle='--')

    # Remove top/right spines for a cleaner look
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add a subtle background
    ax.set_facecolor('#F7F7F7')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=False)
    plt.show()
    print(f"Line plot saved as {save_path}")

def print_top_performers(df, n=10):
    """Print top performing tool combinations"""
    print(f"\n=== Top {n} Performing Tool Combinations ===")
    top_df = df.nlargest(n, 'accuracy')
    
    for i, (_, row) in enumerate(top_df.iterrows(), 1):
        print(f"{i:2d}. Accuracy: {row['accuracy']:6.2f}% | "
              f"{row['tool1'][:30]:30s} + {row['tool2'][:30]:30s}")

def print_statistics(df):
    """Print comprehensive statistics"""
    print("\n=== Evaluation Statistics ===")
    print(f"Total tool combinations evaluated: {len(df)}")
    print(f"Mean accuracy: {df['accuracy'].mean():.2f}%")
    print(f"Median accuracy: {df['accuracy'].median():.2f}%")
    print(f"Standard deviation: {df['accuracy'].std():.2f}%")
    print(f"Minimum accuracy: {df['accuracy'].min():.2f}%")
    print(f"Maximum accuracy: {df['accuracy'].max():.2f}%")
    
    # Count combinations above different thresholds
    print(f"\nCombinations with accuracy > 50%: {len(df[df['accuracy'] > 50])}")
    print(f"Combinations with accuracy > 60%: {len(df[df['accuracy'] > 60])}")
    print(f"Combinations with accuracy > 70%: {len(df[df['accuracy'] > 70])}")

# %%

def main():
    """Main function to run the plotting script"""
    # Load data
    print("Loading evaluation results...")
    data = load_evaluation_results()
    
    # Extract metrics
    df = extract_metrics(data)
    
    if df.empty:
        print("No valid evaluation results found!")
        return
    
    print(f"Loaded {len(df)} tool combinations with valid accuracy scores")
    
    # Print statistics
    print_statistics(df)
    
    # Print top performers
    print_top_performers(df)
    
    # Create plots
    print("\nCreating plots...")
    plot_accuracy_histogram(df)
    plot_accuracy_line(df)
    
    print("\nPlotting complete!")

if __name__ == "__main__":
    main() 
# %%
