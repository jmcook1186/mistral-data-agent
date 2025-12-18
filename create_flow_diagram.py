import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
from matplotlib.path import Path
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(0, 10)
ax.set_ylim(1.5, 11.5)
ax.axis('off')

# Define colors
color_data = '#E8F4F8'
color_agent = '#FFE6CC'
color_output = '#E6F3E6'
color_process = '#F0E6FF'

# Title
ax.text(5, 11.2, 'Multi-Agent Data Analysis System Flow (4-Agent Architecture)',
        ha='center', va='top', fontsize=16, fontweight='bold')

# 1. Data & Script Inputs
data_box = FancyBboxPatch((0.3, 9.8), 1.5, 0.7, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(data_box)
ax.text(1.05, 10.15, 'CSV Data File\n(position_text)', ha='center', va='center', fontsize=8, fontweight='bold')

script_box = FancyBboxPatch((4.5, 9.8), 2, 0.7, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(script_box)
ax.text(5.5, 10.15, 'Analysis Script\n(consensus_metrics.py)', ha='center', va='center', fontsize=8, fontweight='bold')

# 2. Whisper Prompt
whisper_prompt_box = FancyBboxPatch((0.3, 8), 1.5, 0.7, boxstyle="round,pad=0.1",
                                    edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(whisper_prompt_box)
ax.text(1.05, 8.35, 'Whisper Prompt\n(task description)', ha='center', va='center', fontsize=8, fontweight='bold')

# 3. Whisper Agent
whisper_box = FancyBboxPatch((0.3, 5.5), 1.5, 1.8, boxstyle="round,pad=0.1",
                            edgecolor='#FF8C00', facecolor=color_agent, linewidth=3)
ax.add_patch(whisper_box)
ax.text(1.05, 6.9, 'WHISPER', ha='center', va='center', fontsize=10, fontweight='bold', color='#FF8C00')
ax.text(1.05, 6.55, 'Prompt Engineer', ha='center', va='center', fontsize=8)
ax.text(1.05, 6.25, 'mistral-medium', ha='center', va='center', fontsize=7)
ax.text(1.05, 5.85, 'Designs prompts\nfor Spec & Quant',
        ha='center', va='center', fontsize=7)

# 4. Spec Agent
spec_box = FancyBboxPatch((2.5, 5.5), 1.8, 1.8, boxstyle="round,pad=0.1",
                          edgecolor='#9933CC', facecolor=color_agent, linewidth=3)
ax.add_patch(spec_box)
ax.text(3.4, 6.9, 'SPEC', ha='center', va='center', fontsize=10, fontweight='bold', color='#9933CC')
ax.text(3.4, 6.55, 'Software Architect', ha='center', va='center', fontsize=8)
ax.text(3.4, 6.25, 'mistral-medium', ha='center', va='center', fontsize=7)
ax.text(3.4, 6.0, 'Tools: web_search', ha='center', va='center', fontsize=6, style='italic')
ax.text(3.4, 5.75, 'Creates technical\nspecifications',
        ha='center', va='center', fontsize=7)

# 5. Dev Agent
dev_box = FancyBboxPatch((5, 5.5), 1.8, 1.8, boxstyle="round,pad=0.1",
                        edgecolor='#009900', facecolor=color_agent, linewidth=3)
ax.add_patch(dev_box)
ax.text(5.9, 6.9, 'DEV', ha='center', va='center', fontsize=10, fontweight='bold', color='#009900')
ax.text(5.9, 6.55, 'Software Engineer', ha='center', va='center', fontsize=8)
ax.text(5.9, 6.25, 'mistral-medium', ha='center', va='center', fontsize=7)
ax.text(5.9, 6.0, 'Tools: code_interpreter', ha='center', va='center', fontsize=6, style='italic')
ax.text(5.9, 5.75, 'Executes all code\n& generates results',
        ha='center', va='center', fontsize=7)

# 6. Quant Agent
quant_box = FancyBboxPatch((7.5, 5.5), 1.8, 1.8, boxstyle="round,pad=0.1",
                          edgecolor='#0066CC', facecolor=color_agent, linewidth=3)
ax.add_patch(quant_box)
ax.text(8.4, 6.9, 'QUANT', ha='center', va='center', fontsize=10, fontweight='bold', color='#0066CC')
ax.text(8.4, 6.55, 'Data Analyst', ha='center', va='center', fontsize=8)
ax.text(8.4, 6.25, 'mistral-medium', ha='center', va='center', fontsize=7)
ax.text(8.4, 6.0, 'Tools: web_search', ha='center', va='center', fontsize=6, style='italic')
ax.text(8.4, 5.75, 'Analyzes results\n& generates reports',
        ha='center', va='center', fontsize=7)

# Arrow from whisper prompt to whisper agent
arrow1 = FancyArrowPatch((1.05, 8.0), (1.05, 7.3),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow1)

# Arrow from script to Spec
arrow2 = FancyArrowPatch((4.8, 9.8), (3.4, 7.3),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow2)
ax.text(4.2, 8.5, 'Script', ha='center', va='center', fontsize=7, fontweight='bold')

# Arrow from data to Dev
arrow3 = FancyArrowPatch((1.5, 9.7), (5.5, 7.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black', linestyle='dotted',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow3)
ax.text(3.0, 8.7, 'Data', ha='center', va='center', fontsize=7, fontweight='bold')

# Arrow from script to Dev
arrow4 = FancyArrowPatch((5.8, 9.8), (5.9, 7.3),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow4)
ax.text(6.2, 8.5, 'Script', ha='center', va='center', fontsize=7, fontweight='bold')

# Arrow from Whisper to Spec (horizontal)
arrow5 = FancyArrowPatch((1.8, 6.4), (2.5, 6.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#9933CC',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow5)
ax.text(2.15, 6.75, 'Spec\nPrompt', ha='center', va='center', fontsize=7, color='#9933CC', fontweight='bold')

# Arrow from Spec to Dev (horizontal)
arrow6 = FancyArrowPatch((4.3, 6.4), (5.0, 6.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#CC0000',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow6)
ax.text(4.65, 6.75, 'Tech\nSpec', ha='center', va='center', fontsize=7, color='#CC0000', fontweight='bold')

# Arrow from Dev to Quant (horizontal)
arrow7 = FancyArrowPatch((6.8, 6.4), (7.5, 6.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#006600',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow7)
ax.text(7.15, 6.75, 'Execution\nResults', ha='center', va='center', fontsize=7, color='#006600', fontweight='bold')

# Arrow from Whisper to Quant (routed above other agents)
# WHISPER box: (0.3, 5.5) with width=1.5, height=1.8, so top-right corner is at (1.8, 7.3)
# QUANT box: (7.5, 5.5) with width=1.8, height=1.8, so top edge center is at (8.4, 7.3)
waypoints = [
    (1.87, 7.3),    # Start: top-right corner of WHISPER box
    (1.87, 7.8),    # Go up
    (8.4, 7.8),    # Go across above all boxes
    (8.4, 7.35)    # Go down to just above QUANT top edge
]

# Draw the path with line segments
for i in range(len(waypoints) - 1):
    ax.plot([waypoints[i][0], waypoints[i+1][0]],
            [waypoints[i][1], waypoints[i+1][1]],
            color='#0066CC', linewidth=2)

# Add arrowhead at the end pointing down to QUANT top edge
arrow8 = FancyArrowPatch((8.4, 7.35), (8.4, 7.3),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#0066CC',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow8)
ax.text(5.0, 8.7, 'Quant Prompt', ha='center', va='center', fontsize=7, color='#0066CC', fontweight='bold')

# 7. Outputs
whisper_output = FancyBboxPatch((0.3, 3.8), 1.5, 0.6, boxstyle="round,pad=0.1",
                               edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(whisper_output)
ax.text(1.05, 4.1, 'whisper_out.md\n(Prompts)', ha='center', va='center', fontsize=7, fontweight='bold')

spec_output = FancyBboxPatch((2.5, 3.8), 1.8, 0.6, boxstyle="round,pad=0.1",
                             edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(spec_output)
ax.text(3.4, 4.1, 'specification.md\n(Tech Spec)', ha='center', va='center', fontsize=7, fontweight='bold')

dev_output = FancyBboxPatch((5, 3.8), 1.8, 0.6, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(dev_output)
ax.text(5.9, 4.1, 'dev.md\n(Code & Results)', ha='center', va='center', fontsize=7, fontweight='bold')

quant_output = FancyBboxPatch((7.5, 3.8), 1.8, 0.6, boxstyle="round,pad=0.1",
                             edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(quant_output)
ax.text(8.4, 4.1, 'quant_out.md\n(Report)', ha='center', va='center', fontsize=7, fontweight='bold')

# Arrows to outputs
arrow9 = FancyArrowPatch((1.05, 5.5), (1.05, 4.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow9)

arrow10 = FancyArrowPatch((3.4, 5.5), (3.4, 4.4),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow10)

arrow11 = FancyArrowPatch((5.9, 5.5), (5.9, 4.4),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow11)

arrow12 = FancyArrowPatch((8.4, 5.5), (8.4, 4.4),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow12)

# Legend
legend_y = 2.8
ax.text(0.5, legend_y, 'Legend:', fontsize=8, fontweight='bold')

legend_items = [
    (color_data, 'Data/Input'),
    (color_agent, 'AI Agent'),
    (color_output, 'Output File')
]

for i, (color, label) in enumerate(legend_items):
    x_pos = 1.5 + i * 2.2
    legend_box = FancyBboxPatch((x_pos - 0.3, legend_y - 0.15), 0.4, 0.25,
                               boxstyle="round,pad=0.05", edgecolor='black',
                               facecolor=color, linewidth=1)
    ax.add_patch(legend_box)
    ax.text(x_pos + 0.3, legend_y, label, fontsize=7, va='center')

# Add flow notes
ax.text(5, 2.0, 'Information Flow: Whisper (prompt engineering) → Spec (architecture + script review) → Dev (executes all code: script + enhancements) → Quant (analysis) → Outputs',
        ha='center', va='center', fontsize=7, style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.7))

plt.tight_layout()

plt.savefig('/home/joe/Code/mistral-data-agent/system_flow_diagram.png', dpi=300, bbox_inches='tight')
print("Flow diagram saved as 'system_flow_diagram.png'")
