import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from businessIdeaGen.agents.clarity_agent import get_business_clarity
from businessIdeaGen.agents.niche_agent import identify_niche
from businessIdeaGen.agents.action_agent import create_action_plan
from businessIdeaGen.agents.strategy_agent import create_business_strategy
from businessIdeaGen.utils.logger import SessionLogger
import time

st.title("Business Idea Generator & Planner")

# Add custom CSS for blue download link
st.markdown("""
    <style>
    .stDownloadButton {
        color: #0066cc !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing responses
if 'strategy_response' not in st.session_state:
    st.session_state.strategy_response = None
if 'download_content' not in st.session_state:
    st.session_state.download_content = None
if 'timing_info' not in st.session_state:
    st.session_state.timing_info = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = None

# User input section
user_input = st.text_area("Describe your business goals and current situation:", 
                         height=150,
                         help="What type of online business do you want to start? What are your goals?")

if st.button("Generate Business Plan"):
    if user_input:
        # Create new session logger for each submission
        session_logger = SessionLogger()
        
        with st.spinner("Analyzing your business idea..."):
            try:
                # Store the session ID at the start
                st.session_state.session_id = session_logger.session_id
                
                # Run all agents but only store strategy response
                clarity_response = get_business_clarity(
                    user_input, 
                    session_logger
                )
                
                niche_response = identify_niche(
                    clarity_response,
                    session_logger
                )
                
                action_response = create_action_plan(
                    clarity_response,
                    niche_response,
                    session_logger
                )
                
                # Get final strategy and store it
                st.session_state.strategy_response = create_business_strategy(
                    clarity_response,
                    niche_response,
                    action_response,
                    session_logger
                )
                
                # Get timing information
                agent_timings = session_logger.get_agent_timings()
                total_session_time = session_logger.get_session_duration()
                
                # Store timing information
                st.session_state.timing_info = {
                    'agent_timings': agent_timings,
                    'total_time': total_session_time
                }
                
                # Create and store downloadable content
                st.session_state.download_content = f"""Business Strategy Plan
Generated on: {datetime.now().strftime('%B %d, %Y %H:%M:%S')}
Session ID: {st.session_state.session_id}

{st.session_state.strategy_response}

Processing Time: {agent_timings.get('StrategyAgent', 0):.2f} seconds
Total Session Time: {total_session_time:.2f} seconds
"""
                
            except Exception as e:
                st.error(f"Error generating business plan: {str(e)}")
    else:
        st.warning("Please enter your business goals and situation")

# Display results if they exist
if st.session_state.strategy_response:
    # Add download button at the top
    st.download_button(
        label="Download Business Strategy",
        data=st.session_state.download_content,
        file_name=f"business_strategy_{st.session_state.session_id}.txt",
        mime="text/plain"
    )
    
    # Display strategy results
    st.markdown("### Business Strategy")
    st.write(st.session_state.strategy_response)
    
    # Display timing information for strategy agent
    if st.session_state.timing_info:
        if 'StrategyAgent' in st.session_state.timing_info['agent_timings']:
            st.info(f"Strategy processing time: {st.session_state.timing_info['agent_timings']['StrategyAgent']:.2f} seconds")
    
    # Display session ID and total time
    st.info(f"Session ID: {st.session_state.session_id}")
    if st.session_state.timing_info:
        st.success(f"Total session time: {st.session_state.timing_info['total_time']:.2f} seconds") 