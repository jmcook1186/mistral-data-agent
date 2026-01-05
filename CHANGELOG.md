# Changelog

## Version 2.1 - Critique Agent & Reinforcement Learning Loop (2026-01-05)

### Major Features

#### Quasi-Reinforcement Learning System
Implemented a 5th agent (Critique) that creates a continuous improvement loop similar to reinforcement learning:

- **Critique Agent**: Audits all agent outputs for accuracy, clarity, code quality, and actionability
- **Round-wise Refinement**: Each pipeline execution improves agent performance for subsequent runs
- **Incremental Learning**: Learning materials accumulate across runs, never deleted—only appended
- **Adaptive Prompting**: Prompts automatically updated based on Critique's feedback

**How It Works:**
1. Pipeline executes: Whisper → Spec → Dev → Quant
2. Critique analyzes all prompts and outputs
3. Learning materials generated and appended to `outputs/agent_learning_materials/`
4. Whisper's prompt updated in `prompts/whisper_message.txt`
5. Next run: Agents load learning materials, incorporating feedback like RL reward signals
6. Continuous improvement: Knowledge accumulates with each iteration

**Key Components** (main.py):
- Lines 28-78: Helper functions for loading/saving learning materials
- Lines 226-240: Whisper loads learning materials for herself, Spec, and Quant
- Lines 335-401: Dev loads learning materials before execution
- Lines 567-827: Critique agent call, output parsing, and material extraction

### Implementation Details

1. **Learning Materials Management**
   - `load_learning_materials(agent_name)`: Loads existing learning materials if available
   - `format_learning_materials(materials)`: Formats materials for prompt inclusion
   - `save_learning_materials(agent_name, new_materials)`: Appends new materials to existing files
   - Materials separated by `---` delimiter for tracking iterations

2. **Agent Integration**
   - **Whisper**: Receives own learning materials + materials for Spec/Quant to incorporate when designing their prompts
   - **Dev**: Receives learning materials appended to prompt after data and specification
   - **Spec & Quant**: Receive prompts from Whisper that incorporate their learning materials
   - All agents benefit from accumulated knowledge across runs

3. **Critique Output Processing**
   - Extracts learning materials for all 4 agents using flexible heading markers (handles `##`, `###`, and `**bold**` formats)
   - Parses updated Whisper prompt and overwrites `prompts/whisper_message.txt`
   - Extracts Spec/Dev/Quant prompt suggestions and appends them to Whisper's prompt file
   - Comprehensive error handling for missing sections or malformed output

### Bug Fixes

1. **Dev Output Saving** (main.py, line 463)
   - **Issue**: TypeError when concatenating list to string in dev.md file writing
   - **Fix**: Added type checking to ensure all content is converted to string before concatenation

2. **Critique Content Parsing** (main.py, line 681)
   - **Issue**: TypeError when Critique returns content as list instead of string
   - **Fix**: Added type checking and conversion for all agent output content

3. **Learning Materials Parsing** (main.py, lines 696-731)
   - **Issue**: Could not find learning materials sections due to heading format variations
   - **Fix**: Implemented flexible pattern matching supporting multiple markdown heading formats

4. **Prompt Suggestions Extraction** (main.py, lines 738-821)
   - **Issue**: Failed to extract updated prompts when headings used bold markdown
   - **Fix**: Added support for `### **Heading**` and `### Heading` formats

### Files Modified
- `main.py` - Added Critique agent call, learning materials management, and integration (250+ lines added)
- `agents/agents.py` - Added Critique agent definition (lines 96-112)
- `prompts/critique_message.txt` - Created new file with Critique agent instructions
- `README.md` - Updated to reflect 5-agent architecture and RL loop
- `CHANGELOG.md` - This file

### Files Created
- `outputs/agent_learning_materials/` - Directory for storing learning materials
- `outputs/agent_learning_materials/whisper_learning.md` - Whisper's accumulated learning
- `outputs/agent_learning_materials/spec_learning.md` - Spec's accumulated learning
- `outputs/agent_learning_materials/dev_learning.md` - Dev's accumulated learning
- `outputs/agent_learning_materials/quant_learning.md` - Quant's accumulated learning
- `outputs/critique_out.md` - Critique agent's full output for each run

### Architecture Changes

**Before (Version 2.0):**
```
User Input → Whisper → Spec → Dev → Quant → Outputs
```

**After (Version 2.1):**
```
User Input → Whisper (+ learning materials) → Spec → Dev (+ learning materials) → Quant
           ↑                                                                      ↓
           └─────────────── Critique (generates learning materials) ←────────────┘
```

Each run creates a feedback loop where:
- Critique acts as the "reward function" providing human-interpretable feedback
- Learning materials act as "reward signals" guiding future agent behavior
- Prompts adapt automatically without manual engineering
- Knowledge accumulates across runs, improving quality over time

### Benefits

1. **Self-Improving System**: Agents learn from mistakes and successes automatically
2. **No Manual Tuning**: Prompts refine themselves based on Critique's feedback
3. **Interpretable Learning**: Unlike RL's numerical rewards, feedback is human-readable
4. **Cumulative Knowledge**: Each run builds on all previous runs' insights
5. **Quality Assurance**: Critique ensures code quality, analysis rigor, and insight actionability

### Reinforcement Learning Analogy

| RL Component | System Equivalent |
|--------------|-------------------|
| Agent | Whisper, Spec, Dev, Quant |
| Environment | Data analysis pipeline |
| Action | Prompts designed, code written, insights generated |
| Reward | Learning materials from Critique |
| Policy | Agent instructions + accumulated learning materials |
| Episode | Single pipeline execution |
| Training | Multiple runs accumulating knowledge |

Unlike traditional RL:
- "Rewards" are qualitative feedback (strengths, improvements, resources)
- "Policy updates" are prompt refinements (human-interpretable)
- No gradient descent—learning via natural language feedback
- Immediate applicability without extensive training episodes

---

## Version 2.0 - Large File Support (2025-12-23)

### Major Features

#### Three-Tier Data Handling System
Implemented automatic file size detection and adaptive data passing to handle CSV files of any size:

- **Full Data Mode (< 50KB)**: Complete dataset embedded in agent prompts
- **Random Sampling Mode (50KB - 500KB)**: Random sample of 500 rows for better statistical representation
- **Summary Statistics Mode (> 500KB)**: Comprehensive summary stats, sample texts, and value counts

**Configuration** (lines 11-23 in `main.py`):
```python
FULL_DATA_THRESHOLD = 50000      # < 50KB: pass full dataset
SAMPLE_DATA_THRESHOLD = 500000   # 50KB - 500KB: use random sample
SAMPLE_SIZE = 500                # Number of rows in sample
RANDOM_SEED = 42                 # For reproducible sampling
```

### Improvements

1. **Better Sampling Strategy**
   - Changed from sequential sampling (`head(100)`) to random sampling (`sample(500, random_state=42)`)
   - Random sampling provides better statistical representation of the full dataset
   - Increased default sample size from 100 to 500 rows
   - Reproducible results via fixed random seed

2. **Enhanced Error Handling**
   - Comprehensive error handling throughout `main.py`
   - Detailed status reporting with checkmarks (✓) and warnings (⚠)
   - Type-safe parsing of agent responses
   - Graceful handling of missing or malformed outputs

3. **Configurable Thresholds**
   - All data handling thresholds exposed as constants at top of `main.py`
   - Easy to adjust for specific use cases or larger API limits
   - Clear documentation of what each threshold controls

### Bug Fixes

1. **Dev Agent Tools Configuration** (agents/agents.py, line 67-70)
   - **Issue**: Duplicate "type" keys in tools dictionary prevented code_interpreter from working
   - **Fix**: Separated into two distinct tool objects
   ```python
   # Before (broken):
   tools=[{"type": "web_search", "type": "code_interpreter"}]

   # After (fixed):
   tools=[
       {"type": "web_search"},
       {"type": "code_interpreter"}
   ]
   ```

2. **API Input Size Limit Error**
   - **Issue**: SDKError "Failed to persist entries" when passing large CSV files
   - **Fix**: Implemented three-tier data handling to keep prompts under API limits
   - Now handles files of any size without API errors

3. **Remote Sandbox File Access** (agents/agents.py, lines 60-64)
   - **Issue**: Files saved by Dev agent to sandbox were inaccessible locally
   - **Fix**: Updated Dev agent instructions to print all results to stdout
   - Results now properly captured in execution output and passed to Quant agent

4. **Type Safety in Quant Input** (main.py, line 398)
   - **Issue**: TypeError when joining quant_input_parts (non-string items in list)
   - **Fix**: Explicitly convert all items to strings before joining
   ```python
   quant_input_parts = [str(part) for part in quant_input_parts]
   ```

### Documentation

1. **LARGE_FILES.md** (new file)
   - Comprehensive guide for handling large CSV files
   - Explains all three data modes with examples
   - Configuration options and tradeoffs
   - Best practices and troubleshooting
   - Future improvement strategies (local embedding generation, chunk-based processing)

2. **README.md Updates**
   - Added "Recent Updates" section documenting v2.0 changes
   - Added "Handling Large CSV Files" section in Configuration
   - Added comprehensive "Limitations" section covering API, data, and architectural constraints
   - Added "Future Improvements" section with 14 prioritized enhancements
   - Added "Contributing" section highlighting key areas for community involvement
   - Updated project structure to include new documentation files

3. **CHANGELOG.md** (this file)
   - Detailed record of all changes in v2.0
   - Easy reference for what changed and why

### Technical Changes

#### main.py
- Lines 11-23: Added configuration constants
- Lines 45-136: Implemented three-tier data handling logic
- Lines 250-310: Updated Dev agent prompt construction for different data modes
- Throughout: Added comprehensive error handling and status reporting

#### agents/agents.py
- Lines 60-64: Updated Dev agent instructions for remote sandbox
- Lines 67-70: Fixed tools configuration

### Files Modified
- `main.py` - Core orchestration script (major refactor)
- `agents/agents.py` - Agent configurations (bug fixes and instruction updates)
- `README.md` - Documentation updates (new sections added)

### Files Created
- `LARGE_FILES.md` - Large file handling guide
- `CHANGELOG.md` - This file

---

## Version 1.0 - Initial 4-Agent System (2025-12-20)

### Features
- Four-agent collaborative pipeline: Whisper → Spec → Dev → Quant
- Core analysis pipeline: embeddings, clustering, topic modeling, sentiment analysis
- Mistral AI agent integration with code_interpreter and web_search tools
- Automatic output saving to markdown files
- System flow diagram visualization

### Components
- `main.py` - Multi-agent orchestration
- `agents/agents.py` - Agent initialization
- `consensus_metrics.py` - Core analysis script
- `prompts/whisper_message.txt` - Initial prompt for Whisper agent
- `create_flow_diagram.py` - System architecture visualization
