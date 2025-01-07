import logging
import os
import uuid
from datetime import datetime
import time

class SessionLogger:
    def __init__(self):
        # Create session ID with updated format (MMM-DD-YYYY-MM-SS)
        current_time = datetime.now()
        self.session_id = current_time.strftime("%b-%d-%Y-%M-%S")
        
        # Create log directories if they don't exist
        self.log_dir = 'logs'
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Create regular log file
        log_file = f"{self.log_dir}/businessIGen1-{self.session_id}.log"
        
        # Create timing log file
        self.timing_log_file = f"{self.log_dir}/timing-{self.session_id}.log"
        
        # Configure main logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(f"Session-{self.session_id}")
        
        # Configure timing logger
        self.timing_logger = logging.getLogger(f"Timing-{self.session_id}")
        timing_handler = logging.FileHandler(self.timing_log_file)
        timing_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.timing_logger.addHandler(timing_handler)
        self.timing_logger.setLevel(logging.INFO)
        
        # Initialize timing dictionary
        self.timing_data = {}
        self.session_start_time = time.time()
    
    def log_agent_input(self, agent_name, input_data):
        self.logger.info(f"Agent: {agent_name} - Input: {input_data}")
        # Start timing for this agent
        self.timing_data[agent_name] = {'start': time.time()}
    
    def log_agent_output(self, agent_name, output_data):
        self.logger.info(f"Agent: {agent_name} - Output: {output_data}")
        # End timing for this agent and log it
        if agent_name in self.timing_data:
            end_time = time.time()
            start_time = self.timing_data[agent_name]['start']
            duration = end_time - start_time
            self.timing_logger.info(f"Agent: {agent_name} - Duration: {duration:.2f} seconds")
            self.timing_data[agent_name]['duration'] = duration
    
    def get_session_duration(self):
        """Get the total duration of the session so far"""
        return time.time() - self.session_start_time
    
    def get_agent_timings(self):
        """Get a dictionary of all agent timings"""
        return {agent: data.get('duration', 0) for agent, data in self.timing_data.items()} 