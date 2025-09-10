#!/usr/bin/env python
import os
import sys
import warnings
import io
from contextlib import redirect_stderr
from datetime import datetime

# Suppress all warnings before importing any modules
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

from coder.crew import Coder

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

assignment = 'Write a python program to calculate the first 10,000 terms \
    of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + ...'

def run():
    """
    Run the crew.
    """
    inputs = {
        'assignment': assignment,
    }
    
    # Redirect stderr to suppress warnings during execution
    with redirect_stderr(io.StringIO()):
        result = Coder().crew().kickoff(inputs=inputs)
    print(result.raw)




