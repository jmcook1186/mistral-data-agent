import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
from matplotlib.path import Path
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(16, 13))
ax.set_xlim(0, 10)
ax.set_ylim(0.5, 12.5)
ax.axis('off')

# Define colors
color_data = '#E8F4F8'
color_agent = '#FFE6CC'
color_output = '#E6F3E6'
color_process = '#F0E6FF'
color_critique = '#FFE6E6'  # Light red for critique agent
color_feedback = '#CC0066'  # Magenta for feedback loop

# Title
ax.text(5, 12.2, 'Multi-Agent Data Analysis System Flow (5-Agent Architecture with RL Loop)',
        ha='center', va='top', fontsize=16, fontweight='bold')

# 1. Data & Script Inputs
data_box = FancyBboxPatch((0.3, 9.8), 1.5, 0.7, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(data_box)
ax.text(1.05, 10.15, 'CSV Data File\n(position_text)', ha='center', va='center', fontsize=8, fontweight='bold')

script_box = FancyBboxPatch((4.5, 9.8), 2, 0.7, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=color_data, linewidth=2)
ax.add_patch(script_box)
ax.text(5.5, 10.15, 'Analysis Script\n(generated_code/\nconsensus_metrics.py)', ha='center', va='center', fontsize=7, fontweight='bold')

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

# 7. Critique Agent (positioned to show feedback loop)
critique_box = FancyBboxPatch((3.6, 2.2), 2.8, 1.5, boxstyle="round,pad=0.1",
                             edgecolor='#CC0066', facecolor=color_critique, linewidth=3)
ax.add_patch(critique_box)
ax.text(5.0, 3.45, 'CRITIQUE', ha='center', va='center', fontsize=10, fontweight='bold', color='#CC0066')
ax.text(5.0, 3.15, 'Quality Assurance & Learning', ha='center', va='center', fontsize=8)
ax.text(5.0, 2.9, 'mistral-medium', ha='center', va='center', fontsize=7)
ax.text(5.0, 2.65, 'Tools: web_search', ha='center', va='center', fontsize=6, style='italic')
ax.text(5.0, 2.4, 'Audits outputs & generates\nlearning materials (RL loop)',
        ha='center', va='center', fontsize=7)

# Arrow from whisper prompt to whisper agent
arrow1 = FancyArrowPatch((1.05, 7.95), (1.05, 7.35),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow1)

# Arrow from script to Spec (routed around)
# Script box bottom center: (5.5, 9.8), Spec box top center: (3.4, 7.3)
script_to_spec_waypoints = [
    (5.0, 9.68),     # Start: left side of script box
    (5.0, 8.5),     # Go down
    (3.4, 8.5),     # Go left above agents
    (3.4, 7.35)      # Go down to Spec top
]
for i in range(len(script_to_spec_waypoints) - 1):
    ax.plot([script_to_spec_waypoints[i][0], script_to_spec_waypoints[i+1][0]],
            [script_to_spec_waypoints[i][1], script_to_spec_waypoints[i+1][1]],
            color='black', linewidth=2)
arrow2 = FancyArrowPatch((3.4, 7.35), (3.4, 7.35),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black')
ax.add_patch(arrow2)
ax.text(4.2, 8.4, 'Script', ha='center', va='center', fontsize=7, fontweight='bold')

# Arrow from data to Dev (routed around boxes)
# Data box: (1.05, 9.8), Dev box: (5.9, 7.3)
data_to_dev_waypoints = [
    (1.95, 10.0),    # Start: right side of data box
    (2.0, 10.0),    # Go right
    (2.0, 8.0),     # Go down (between Whisper and Spec)
    (6.0, 8.0),     # Go right above Dev
    (6.0, 7.35)      # Go down to Dev top
]
for i in range(len(data_to_dev_waypoints) - 1):
    ax.plot([data_to_dev_waypoints[i][0], data_to_dev_waypoints[i+1][0]],
            [data_to_dev_waypoints[i][1], data_to_dev_waypoints[i+1][1]],
            color='black', linewidth=2, linestyle='dotted')
arrow3 = FancyArrowPatch((6.0, 7.35), (6.0, 7.35),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black')
ax.add_patch(arrow3)
ax.text(3.0, 8.1, 'Data', ha='center', va='center', fontsize=7, fontweight='bold')

# Arrow from script to Dev
arrow4 = FancyArrowPatch((5.9, 9.75), (5.9, 7.3),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow4)
ax.text(6.2, 8.8, 'Script', ha='center', va='center', fontsize=7, fontweight='bold')

# Arrow from Whisper to Spec (horizontal)
arrow5 = FancyArrowPatch((1.9, 6.4), (2.5, 6.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#9933CC',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow5)
ax.text(2.15, 6.75, 'Spec\nPrompt', ha='center', va='center', fontsize=7, color='#9933CC', fontweight='bold')

# Arrow from Spec to Dev (horizontal)
arrow6 = FancyArrowPatch((4.4, 6.4), (5.0, 6.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#CC0000',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow6)
ax.text(4.65, 6.75, 'Tech\nSpec', ha='center', va='center', fontsize=7, color='#CC0000', fontweight='bold')

# Arrow from Dev to Quant (horizontal)
arrow7 = FancyArrowPatch((6.9, 6.4), (7.5, 6.4),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='#006600',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow7)
ax.text(7.15, 6.75, 'Execution\nResults', ha='center', va='center', fontsize=7, color='#006600', fontweight='bold')

# Arrow from Whisper to Quant (routed above other agents)
# WHISPER box: (0.3, 5.5) with width=1.5, height=1.8, so top-right corner is at (1.8, 7.3)
# QUANT box: (7.5, 5.5) with width=1.8, height=1.8, so top edge center is at (8.4, 7.3)
waypoints = [
    (1.5, 7.4),    # Start: top-right corner of WHISPER box
    (1.5, 7.7),    # Go up
    (8.4, 7.7),    # Go across above all boxes
    (8.4, 7.3)    # Go down to just above QUANT top edge
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
ax.text(5.0, 7.9, 'Quant Prompt', ha='center', va='center', fontsize=7, color='#0066CC', fontweight='bold')

# 8. Outputs (moved down to make room for Critique)
whisper_output = FancyBboxPatch((0.3, 4.5), 1.5, 0.6, boxstyle="round,pad=0.1",
                               edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(whisper_output)
ax.text(1.05, 4.8, 'whisper_out.md\n(Prompts)', ha='center', va='center', fontsize=7, fontweight='bold')

spec_output = FancyBboxPatch((2.5, 4.5), 1.8, 0.6, boxstyle="round,pad=0.1",
                             edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(spec_output)
ax.text(3.4, 4.8, 'specification.md\n(Tech Spec)', ha='center', va='center', fontsize=7, fontweight='bold')

dev_output = FancyBboxPatch((5, 4.5), 1.8, 0.6, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(dev_output)
ax.text(5.9, 4.8, 'dev.md\n(Code & Results)', ha='center', va='center', fontsize=7, fontweight='bold')

quant_output = FancyBboxPatch((7.5, 4.5), 1.8, 0.6, boxstyle="round,pad=0.1",
                             edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(quant_output)
ax.text(8.4, 4.8, 'quant_out.md\n(Report)', ha='center', va='center', fontsize=7, fontweight='bold')

# Critique outputs
critique_output = FancyBboxPatch((3.6, 0.9), 1.3, 0.5, boxstyle="round,pad=0.05",
                                edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(critique_output)
ax.text(4.25, 1.15, 'critique_out.md\n(Audit)', ha='center', va='center', fontsize=6, fontweight='bold')

learning_output = FancyBboxPatch((5.1, 0.9), 1.3, 0.5, boxstyle="round,pad=0.05",
                                edgecolor='black', facecolor='#FFFFCC', linewidth=2)
ax.add_patch(learning_output)
ax.text(5.75, 1.15, 'Learning\nMaterials', ha='center', va='center', fontsize=6, fontweight='bold')

# Arrows to outputs (from agents)
arrow9 = FancyArrowPatch((1.05, 5.5), (1.05, 5.1),
                        arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                        connectionstyle="arc3,rad=0")
ax.add_patch(arrow9)

arrow10 = FancyArrowPatch((3.4, 5.5), (3.4, 5.1),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow10)

arrow11 = FancyArrowPatch((5.9, 5.5), (5.9, 5.1),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow11)

arrow12 = FancyArrowPatch((8.4, 5.5), (8.4, 5.1),
                         arrowstyle='->', mutation_scale=15, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow12)

# Arrows from agent outputs to Critique (routed with straight lines)
# Critique box: (3.6, 2.2) to (6.4, 3.7)

# Whisper output to Critique (route around left side)
whisper_to_critique_waypoints = [
    (1.05, 4.4),    # Start: bottom of whisper output
    (1.05, 4.0),    # Go down
    (3.5, 4.0),     # Go right
    (3.5, 3.7)      # Go down to Critique top
]
for i in range(len(whisper_to_critique_waypoints) - 1):
    ax.plot([whisper_to_critique_waypoints[i][0], whisper_to_critique_waypoints[i+1][0]],
            [whisper_to_critique_waypoints[i][1], whisper_to_critique_waypoints[i+1][1]],
            color=color_feedback, linewidth=1.5, linestyle='dashed')
arrow13 = FancyArrowPatch((3.5, 3.75), (3.5, 3.7),
                         arrowstyle='->', mutation_scale=12, linewidth=1.5, color=color_feedback)
ax.add_patch(arrow13)

# Spec output to Critique (almost straight down)
spec_to_critique_waypoints = [
    (3.4, 4.4),     # Start: bottom of spec output
    (3.4, 4.1),     # Go down
    (4.5, 4.1),     # Go right
    (4.5, 3.7)      # Go down to Critique top
]
for i in range(len(spec_to_critique_waypoints) - 1):
    ax.plot([spec_to_critique_waypoints[i][0], spec_to_critique_waypoints[i+1][0]],
            [spec_to_critique_waypoints[i][1], spec_to_critique_waypoints[i+1][1]],
            color=color_feedback, linewidth=1.5, linestyle='dashed')
arrow14 = FancyArrowPatch((4.5, 3.75), (4.5, 3.7),
                         arrowstyle='->', mutation_scale=12, linewidth=1.5, color=color_feedback)
ax.add_patch(arrow14)

# Dev output to Critique (almost straight down)
dev_to_critique_waypoints = [
    (5.9, 4.4),     # Start: bottom of dev output
    (5.9, 4.0),     # Go down
    (5.5, 4.0),     # Go left slightly
    (5.5, 3.7)      # Go down to Critique top
]
for i in range(len(dev_to_critique_waypoints) - 1):
    ax.plot([dev_to_critique_waypoints[i][0], dev_to_critique_waypoints[i+1][0]],
            [dev_to_critique_waypoints[i][1], dev_to_critique_waypoints[i+1][1]],
            color=color_feedback, linewidth=1.5, linestyle='dashed')
arrow15 = FancyArrowPatch((5.5, 3.75), (5.5, 3.7),
                         arrowstyle='->', mutation_scale=12, linewidth=1.5, color=color_feedback)
ax.add_patch(arrow15)

# Quant output to Critique (route around right side)
quant_to_critique_waypoints = [
    (8.4, 4.4),     # Start: bottom of quant output
    (8.4, 4.0),     # Go down
    (6.2, 4.0),     # Go left
    (6.2, 3.7)      # Go down to Critique top
]
for i in range(len(quant_to_critique_waypoints) - 1):
    ax.plot([quant_to_critique_waypoints[i][0], quant_to_critique_waypoints[i+1][0]],
            [quant_to_critique_waypoints[i][1], quant_to_critique_waypoints[i+1][1]],
            color=color_feedback, linewidth=1.5, linestyle='dashed')
arrow16 = FancyArrowPatch((6.2, 3.75), (6.2, 3.7),
                         arrowstyle='->', mutation_scale=12, linewidth=1.5, color=color_feedback)
ax.add_patch(arrow16)

# Arrows from Critique to its outputs
arrow17 = FancyArrowPatch((4.5, 2.1), (4.5, 1.4),
                         arrowstyle='->', mutation_scale=12, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow17)

arrow18 = FancyArrowPatch((5.5, 2.1), (5.5, 1.4),
                         arrowstyle='->', mutation_scale=12, linewidth=2, color='black',
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow18)

# Feedback loop: Learning Materials back to Whisper (RL loop)
# Create a curved arrow from learning materials back to Whisper
feedback_waypoints = [
    (5.5, 0.85),    # Start: left edge of learning materials
    (5.5, 0.6),    # Go down
    (0.05, 0.6),     # Go left
    (0.05, 6.5),      # Go up
    (0.2, 6.5)     # Go right to end
]

# Draw the feedback path
for i in range(len(feedback_waypoints) - 1):
    ax.plot([feedback_waypoints[i][0], feedback_waypoints[i+1][0]],
            [feedback_waypoints[i][1], feedback_waypoints[i+1][1]],
            color=color_feedback, linewidth=3, linestyle='solid')

# Add arrowhead at Whisper
arrow19 = FancyArrowPatch((0.18, 6.5), (0.2, 6.5),
                         arrowstyle='->', mutation_scale=20, linewidth=3, color=color_feedback,
                         connectionstyle="arc3,rad=0")
ax.add_patch(arrow19)

# Label for feedback loop
ax.text(1.2, 1.0, 'Learning\nMaterials\n(RL Feedback)', ha='center', va='center',
        fontsize=7, color=color_feedback, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color_feedback, linewidth=2))

# Legend (moved down)
legend_y = 11.5
ax.text(0.5, legend_y, 'Legend:', fontsize=8, fontweight='bold')

legend_items = [
    (color_data, 'Data/Input'),
    (color_agent, 'AI Agent'),
    (color_critique, 'QA Agent'),
    (color_output, 'Output File'),
    ('#FFFFCC', 'Learning')
]

for i, (color, label) in enumerate(legend_items):
    x_pos = 1.5 + i * 1.6
    legend_box = FancyBboxPatch((x_pos - 0.3, legend_y - 0.15), 0.4, 0.25,
                               boxstyle="round,pad=0.05", edgecolor='black',
                               facecolor=color, linewidth=1)
    ax.add_patch(legend_box)
    ax.text(x_pos + 0.3, legend_y, label, fontsize=7, va='center')

# Add flow notes
ax.text(5.5, 11.1, 'Forward Flow: Whisper (prompt engineering) → Spec (architecture) → Dev (executes all code) → Quant (analysis) → Outputs',
        ha='center', va='center', fontsize=7, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.7))

ax.text(5.5, 10.8, 'RL Feedback Loop: All agent outputs → Critique (quality assurance) → Learning Materials → Whisper (next iteration)',
        ha='center', va='center', fontsize=7, style='italic', color=color_feedback,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFE6F0', alpha=0.7, edgecolor=color_feedback))

plt.tight_layout()

plt.savefig('/home/joe/Code/mistral-data-agent/system_flow_diagram.png', dpi=300, bbox_inches='tight')
print("Flow diagram saved as 'system_flow_diagram.png'")
