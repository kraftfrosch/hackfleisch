import subprocess
import sys
import os

def start_video_agent(survey_prompt: str, survey_id: str):
    """
    Start the video agent with the given survey prompt and ID as a background process.
    
    Args:
        survey_prompt (str): The prompt for the survey
        survey_id (str): The ID for the survey
    """
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to video_agent.py
    video_agent_path = os.path.join(current_dir, "src", "external_agents", "video_agent.py")
    
    # Get conda environment path
    if sys.platform == "win32":
        conda_python = os.path.expanduser("C:/Users/vishw/.conda/envs/cdtmhack/python.exe")
        if not os.path.exists(conda_python):
            conda_python = os.path.expanduser("C:/Users/vishw/.conda/envs/cdtmhack/python.exe")
    else:
        conda_python = os.path.expanduser("~/anaconda3/envs/cdtmhack/bin/python")
        if not os.path.exists(conda_python):
            conda_python = os.path.expanduser("~/miniconda3/envs/cdtmhack/bin/python")
    
    if not os.path.exists(conda_python):
        raise Exception(f"Could not find Python in conda environment 'cdtmhack'. Please ensure the environment exists.")
    
    # Set environment variables for the survey
    env = os.environ.copy()
    env["SURVEY_PROMPT"] = survey_prompt
    env["SURVEY_ID"] = survey_id
    
    # Create the command to run
    command = [
        conda_python,
        video_agent_path,
        "start"  # The command for the video agent
    ]
    
    try:
        # Start the process in the background
        if sys.platform == "win32":
            # On Windows, use CREATE_NEW_PROCESS_GROUP to run in background
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
            )
        else:
            # On Unix-like systems, use nohup to run in background
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
                start_new_session=True
            )
        
        print("Video agent started in background")
        
    except Exception as e:
        print(f"Failed to start video agent: {str(e)}")

if __name__ == "__main__":
    # Example usage
    survey_prompt = "You are supposed to conduct a survey on CDTM."
    survey_id = "1"
    start_video_agent(survey_prompt, survey_id)
