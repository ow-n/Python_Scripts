"""
Script for the 'The Evolving Usage of GenAI by Computing Students' 2024 poster.
Generates comparison plots for the resource usage data from the survey results.

Student Resource Usage Visualizer
Usage:
    python plot_genai_usage_data.py [options]

Options:
    --horizontal    Create horizontal bar charts instead of vertical ones
    --no-numbers    Hide numbers on the bars in the charts
    --fixed-y INT   Set a fixed maximum for y-axis (or x-axis if horizontal)

Examples:
    py plot_data.py --horizontal
    py plot_data.py --no-numbers --fixed-y 50
    py plot_data.py --fixed-y 40  # using this one
"""

import argparse
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# ___CONSTANTS___ #
# COLOR_2023 = '#8884d8'      # purple
# COLOR_2024 = '#82ca9d'      # green
COLOR_2023 = '#ADD8E6'    # blue
COLOR_2024 = '#F08080'    # red
VERT_FIG_SIZE = (4, 6)  # default (10, 6)
HORI_FIG_SIZE = (12, 6)  # default (12, 6)
GENAI_PLOT_NAME = '(A) Generative AI Usage'
FRIENDS_PLOT_NAME = '(B) Friends Usage'
INSTRUCTOR_PLOT_NAME = '(C) Instructor Usage'

# Data for each resource  # hourly, daily, weekly, monthly, never
GENAI_2023 = [4, 7, 9, 11, 16][::-1]  # reverse order
GENAI_2024 = [0, 11, 27, 7, 3][::-1]
FRIENDS_2023 = [2, 13, 16, 10, 6][::-1]
FRIENDS_2024 = [0, 9, 26, 6, 7][::-1]
INSTRUCTOR_2023 = [1, 6, 14, 17, 9][::-1]
INSTRUCTOR_2024 = [0, 3, 18, 13, 14][::-1]


def main(args):
    # Create and save plots
    plots = [
        ('genai', GENAI_2023, GENAI_2024, GENAI_PLOT_NAME),
        ('friends', FRIENDS_2023, FRIENDS_2024, FRIENDS_PLOT_NAME),
        ('instructor', INSTRUCTOR_2023, INSTRUCTOR_2024, INSTRUCTOR_PLOT_NAME)
    ]

    for name, data_2023, data_2024, title in plots:
        # Calculate y_max for each plot individually if fixed-y is not set
        y_max = args.fixed_y if args.fixed_y is not None else None
        
        plot = create_comparison_plot(data_2023, data_2024, title, 
                                      horizontal=args.horizontal, 
                                      show_numbers=not args.no_numbers, 
                                      y_max=y_max)
        plot.savefig(f'{name}_usage.png')

    
    combine_plots()  # combines 3 plots into 1
    create_3plot_comparison(args)  # creates 3 plots as 1 (special formatting)
    create_2plot_comparison(args)  # remove (B) Friends usage chart

    print("Plots have been saved successfully.")


def create_comparison_plot(data_2023, data_2024, title, horizontal=False, show_numbers=True, y_max=None):
    categories = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Never'][::-1]  # reverse order
    
    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=HORI_FIG_SIZE if horizontal else VERT_FIG_SIZE)
    
    if horizontal:
        rects1 = ax.barh(x - width/2, data_2023, width, label='2023', color=COLOR_2023)
        rects2 = ax.barh(x + width/2, data_2024, width, label='2024', color=COLOR_2024)
        ax.set_xlabel('Number of Respondents')
        ax.set_yticks(x)
        ax.set_yticklabels(categories)
        if y_max is not None:
            ax.set_xlim(0, y_max)
    else:
        rects1 = ax.bar(x - width/2, data_2023, width, label='2023', color=COLOR_2023)
        rects2 = ax.bar(x + width/2, data_2024, width, label='2024', color=COLOR_2024)
        ax.set_ylabel('Number of Respondents')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        if y_max is not None:
            ax.set_ylim(0, y_max)

    ax.set_title(title)
    ax.legend()

    if show_numbers:
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    
    return fig


def combine_plots():
    # Open the three images
    genai_img = Image.open('genai_usage.png')
    friends_img = Image.open('friends_usage.png')
    instructor_img = Image.open('instructor_usage.png')

    # Get the dimensions of the images
    width, height = genai_img.size

    # Create a new image with the combined size
    combined_img = Image.new('RGB', (width * 3, height))
    combined_img.paste(genai_img, (0, 0))
    combined_img.paste(friends_img, (width, 0))
    combined_img.paste(instructor_img, (width * 2, 0))

    # Save the combined image
    combined_img.save('combined_usage.png')
    print("Combined plot has been saved as 'combined_usage.png'")


def create_3plot_comparison(args):
    FIG_SIZE = (10, 5)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=FIG_SIZE, sharey=True)
    axes = [ax1, ax2, ax3]
    plots = [
        (GENAI_2023, GENAI_2024, GENAI_PLOT_NAME),
        (FRIENDS_2023, FRIENDS_2024, FRIENDS_PLOT_NAME),
        (INSTRUCTOR_2023, INSTRUCTOR_2024, INSTRUCTOR_PLOT_NAME)
    ]

    categories = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Never'][::-1]  # reverse order
    x = np.arange(len(categories))
    width = 0.35

    for i, (ax, (data_2023, data_2024, title)) in enumerate(zip(axes, plots)):
        rects1 = ax.bar(x - width/2, data_2023, width, label='2023', color=COLOR_2023)
        rects2 = ax.bar(x + width/2, data_2024, width, label='2024', color=COLOR_2024)
        
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        if i == 0:  # Only for GenAI plot
            ax.set_ylabel('Number of Respondents')
            ax.yaxis.set_tick_params(labelleft=True)
        else:
            ax.yaxis.set_tick_params(labelleft=False)  # Remove y-axis numbers for other plots
        
        # Add numbers on all bars for all plots
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        
        if args.fixed_y is not None:
            ax.set_ylim(0, args.fixed_y)

    # Add a single legend for all subplots
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)  # Adjust bottom spacing for legend
    plt.savefig('3plot_comparison.png', bbox_inches='tight')


def create_2plot_comparison(args):
    FIG_SIZE = (8, 5)  # Adjusted figure size for two plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_SIZE, sharey=True)
    plots = [
        (GENAI_2023, GENAI_2024, 'Self-reported Usage'),
        (INSTRUCTOR_2023, INSTRUCTOR_2024, 'Perceived Instructor Usage')
    ]

    categories = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Never'][::-1]  # reverse order
    x = np.arange(len(categories))
    width = 0.35

    for i, (ax, (data_2023, data_2024, title)) in enumerate(zip([ax1, ax2], plots)):
        rects1 = ax.bar(x - width/2, data_2023, width, label='2023', color=COLOR_2023)
        rects2 = ax.bar(x + width/2, data_2024, width, label='2024', color=COLOR_2024)
        
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)  # Removed rotation
        
        if i == 0:  # Only for GenAI plot
            ax.set_ylabel('Number of Respondents')
            ax.yaxis.set_tick_params(labelleft=True)
        else:
            ax.yaxis.set_tick_params(labelleft=False)  # Remove y-axis numbers for other plots
        
        # Add numbers on all bars for all plots
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        
        if args.fixed_y is not None:
            ax.set_ylim(0, args.fixed_y)

    # Add a single legend for all subplots
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)  # Adjust bottom spacing for legend
    plt.savefig('2plot_comparison.png', bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create resource usage comparison plots')
    parser.add_argument('--horizontal', action='store_true', help='Create horizontal bar charts')
    parser.add_argument('--no-numbers', action='store_true', help='Hide numbers on bars')
    parser.add_argument('--fixed-y', type=int, help='Set a fixed maximum for y-axis (or x-axis if horizontal)')
    args = parser.parse_args()
    
    main(args)
