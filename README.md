# Yoshi RL

## Overview
Yoshi RL is a reinforcement learning project aimed at training an agent to complete a level in Yoshi's Island: Super Mario Advance 3.

## Installation

### Prerequisites
- Python 3.x
- Required Python packages specified in `requirements.txt`
- ROM of Yoshi's Island: Super Mario Advance 3
- mGBA Python bindings, available at https://github.com/hanzi/libmgba-py

### Steps
1. Clone the repository:

   ```
   git clone https://github.com/jerrystamm/yoshi-rl.git
   ```

2. Navigate to the project directory:

   ```
   cd yoshi-rl
   ```

3. Download the mGBA Python bindings:

   - Visit https://github.com/hanzi/libmgba-py and follow the instructions to set up the mGBA          bindings for Python.
   - Once set up, copy the mGBA binding directory into the `yoshi-rl` directory.

4. Prepare the Yoshi ROM and save state:

   - Drag your Yoshi ROM into the `yoshi-rl` directory.
   - Place save state, for the start of the level, in the `yoshi-rl` directory as well.

5. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

6. Train an agent:

   ```
   python train.py
   ```
   

## Acknowledgment
I would like to acknowledge the original Python mGBA wrapper created by the user dvruette, to which I made minor modifications for this project.
