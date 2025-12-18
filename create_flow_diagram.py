import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
from matplotlib.path import Path
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Define colors
color_data = '#E8F4F8'
color_agent = '#FFE6CC'
color_output = '#E6F3E6'
color_process = '#F0E6FF'

# Title
ax.text(5, 11.5, 'Multi-Agent Data Analysis System Flow',
        ha='center', va='top', fontsize=18, fontweight='bold')

# 1. Data Source
data_box = FancyBboxPatch((0.5, 10.5), 2, 0.8, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(data_box)
ax.text(1.5, 10.8, 'CSV Data File\n(position_text)', ha='center', va='center', fontsize=9, fontweight='bold')

# 2. Analysis Pipeline
pipeline_box = FancyBboxPatch((0.5, 8.5), 2, 1.2, boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor=color_process, linewidth=2)
ax.add_patch(pipeline_box)
ax.text(1.5, 9.3, 'Analysis Pipeline\n(consensus_metrics.py)', ha='center', va='center', fontsize=9, fontweight='bold')
ax.text(1.5, 8.85, '• Embeddings\n• Clustering (K-means)\n• Topic Modeling (LDA)\n• Sentiment Analysis',
        ha='center', va='center', fontsize=7)

# Arrow from data to pipeline
arrow1 = FancyArrowPatch((1.5, 10.45), (1.5, 9.8),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow1)

# 3. Pipeline outputs (intermediate data)
output_data_box = FancyBboxPatch((3.5, 8.5), 2.5, 2, boxstyle="round,pad=0.1",
                                 edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(output_data_box)
ax.text(4.7, 9.8, 'Analysis Results', ha='center', va='center', fontsize=9, fontweight='bold')
ax.text(4.7, 9.35, '• clusters\n• reduced_embeddings\n• lda\n• sentiments\n• topic_string',
        ha='center', va='center', fontsize=7)

# Arrow from pipeline to output data
arrow2 = FancyArrowPatch((2.57, 9.1), (3.44, 9.1),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow2)

# 4. Whisper Prompt
whisper_prompt_box = FancyBboxPatch((0.5, 6.5), 2, 0.8, boxstyle="round,pad=0.1",
                                    edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(whisper_prompt_box)
ax.text(1.5, 6.9, 'Whisper Prompt\n(task description)', ha='center', va='center', fontsize=9, fontweight='bold')

# 5. Whisper Agent
whisper_box = FancyBboxPatch((0.5, 3.0), 2, 2, boxstyle="round,pad=0.1",
                            edgecolor='#FF8C00', facecolor=color_agent, linewidth=3)
ax.add_patch(whisper_box)
ax.text(1.5, 4.6, 'WHISPER AGENT', ha='center', va='center', fontsize=10, fontweight='bold', color='#FF8C00')
ax.text(1.5, 4.2, 'Role: Prompt Engineer', ha='center', va='center', fontsize=8)
ax.text(1.5, 3.85, 'Model: mistral-medium', ha='center', va='center', fontsize=7)
ax.text(1.5, 3.4, 'Designs optimized prompts\nfor Quant and Dev agents',
        ha='center', va='center', fontsize=7)

# Arrow from whisper prompt to whisper agent
arrow3 = FancyArrowPatch((1.5, 6.45), (1.5, 5.1),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow3)

# 6. Quant Agent
quant_box = FancyBboxPatch((3.5, 3), 2.5, 2, boxstyle="round,pad=0.1",
                          edgecolor='#0066CC', facecolor=color_agent, linewidth=3)
ax.add_patch(quant_box)
ax.text(4.75, 4.6, 'QUANT AGENT', ha='center', va='center', fontsize=10, fontweight='bold', color='#0066CC')
ax.text(4.75, 4.3, 'Role: Data Analyst', ha='center', va='center', fontsize=8)
ax.text(4.75, 4.05, 'Model: mistral-medium', ha='center', va='center', fontsize=7)
ax.text(4.75, 3.7, 'Tools: web-search, code_interpreter', ha='center', va='center', fontsize=7, style='italic')
ax.text(4.75, 3.4, '• Analyzes data & statistics\n• Generates detailed reports\n• Identifies key trends\n• Provides instructions for Dev',
        ha='center', va='center', fontsize=7)

# Arrow from whisper to quant (prompt) - now horizontal at center
arrow4 = FancyArrowPatch((2.57, 3.8), (3.42, 3.8),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#0066CC',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow4)
ax.text(3.0, 3.4, 'Quant\nPrompt', ha='center', va='center', fontsize=7, color='#0066CC', fontweight='bold')

# Arrow from analysis results to quant
arrow5 = FancyArrowPatch((4.75, 8.45), (4.75, 5.1),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow5)

# 7. Dev Agent
dev_box = FancyBboxPatch((7, 3), 2.5, 2, boxstyle="round,pad=0.1",
                        edgecolor='#009900', facecolor=color_agent, linewidth=3)
ax.add_patch(dev_box)
ax.text(8.25, 4.6, 'DEV AGENT', ha='center', va='center', fontsize=10, fontweight='bold', color='#009900')
ax.text(8.25, 4.3, 'Role: Software Developer', ha='center', va='center', fontsize=8)
ax.text(8.25, 4.05, 'Model: mistral-medium', ha='center', va='center', fontsize=7)
ax.text(8.25, 3.7, 'Tools: web-search, code_interpreter', ha='center', va='center', fontsize=7, style='italic')
ax.text(8.25, 3.4, '• Writes Python code\n• Creates visualizations\n• Implements recommendations\n• Tests & error handling',
        ha='center', va='center', fontsize=7)

# Arrow from whisper to dev (prompt) - routed above quant box with sharp corners
# Define waypoints: start from whisper, go up, across above quant, down to dev
waypoints = [
    (2.6, 4.0),    # Start: right edge of WHISPER box at center
    (3.0, 4.0),    # Move right a bit
    (3.0, 6.0),    # Go up above QUANT box (QUANT top is at 5.0, so go to 6.0)
    (6.5, 6.0),    # Go across above QUANT box (QUANT right edge is at 6.0)
    (6.5, 4.0),    # Go down to DEV center level
    (6.8, 4.0)     # End: left edge of DEV box at center
]

# Draw the path with line segments
for i in range(len(waypoints) - 1):
    ax.plot([waypoints[i][0], waypoints[i+1][0]],
            [waypoints[i][1], waypoints[i+1][1]],
            color='#009900', linewidth=2)

# Add arrowhead at the end
arrow6 = FancyArrowPatch((6.8, 4.0), (7.0, 4.0),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#009900',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow6)
ax.text(3.75, 6.3, 'Dev Prompt', ha='center', va='center', fontsize=7, color='#009900', fontweight='bold')

# Arrow from quant to dev (instructions) - horizontal at center
arrow7 = FancyArrowPatch((6.1, 3.8), (6.95, 3.8),
                        arrowstyle='->', mutation_scale=15, linewidth=2.5, color='#CC0000', linestyle='dashed',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow7)
ax.text(6.5, 3.4, 'Instructions\nfor Dev', ha='center', va='center', fontsize=7, color='#CC0000', fontweight='bold')

# Arrow from script to dev
arrow8 = FancyArrowPatch((6.10, 8.55), (8.0, 5.1),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black', linestyle='dotted',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow8)
ax.text(6.5, 6.8, 'Current Script\n(for reference)', ha='center', va='center', fontsize=7)

# 8. Outputs
whisper_output = FancyBboxPatch((0.5, 1.3), 2, 0.8, boxstyle="round,pad=0.1",
                               edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(whisper_output)
ax.text(1.5, 1.9, 'whisper_out.md\n(Prompts)', ha='center', va='center', fontsize=8, fontweight='bold')

quant_output = FancyBboxPatch((3.5, 1.3), 2.5, 0.8, boxstyle="round,pad=0.1",
                             edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(quant_output)
ax.text(4.75, 1.9, 'quant_out.md\n(Analysis Report)', ha='center', va='center', fontsize=8, fontweight='bold')

dev_output = FancyBboxPatch((7, 1.3), 2.5, 0.8, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(dev_output)
ax.text(8.25, 1.9, 'dev_out.md\n(Python Code)', ha='center', va='center', fontsize=8, fontweight='bold')

# Arrows to outputs
arrow9 = FancyArrowPatch((1.5, 2.9), (1.5, 2.3),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow9)

arrow10 = FancyArrowPatch((4.75, 2.9), (4.75, 2.3),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow10)

arrow11 = FancyArrowPatch((8.25, 2.9), (8.25, 2.3),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow11)

# Legend
legend_y = 0.5
ax.text(0.5, legend_y, 'Legend:', fontsize=9, fontweight='bold')

legend_items = [
    (color_data, 'Data/Input'),
    (color_process, 'Processing'),
    (color_agent, 'AI Agent'),
    (color_output, 'Output File')
]

for i, (color, label) in enumerate(legend_items):
    x_pos = 1.5 + i * 2
    legend_box = FancyBboxPatch((x_pos - 0.3, legend_y - 0.15), 0.4, 0.25,
                               boxstyle="round,pad=0.05", edgecolor='black',
                               facecolor=color, linewidth=1)
    ax.add_patch(legend_box)
    ax.text(x_pos + 0.3, legend_y, label, fontsize=7, va='center')

# Add flow notes
ax.text(5, 0.1, 'Information Flow: Data → Pipeline → Whisper (prompt engineering) → Quant (analysis) ⇄ Dev (code implementation) → Outputs',
        ha='center', va='center', fontsize=8, style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.7))

plt.tight_layout()

plt.savefig('/home/joe/Code/mistral-data-agent/system_flow_diagram.png', dpi=300, bbox_inches='tight')
print("Flow diagram saved as 'system_flow_diagram.png'")
