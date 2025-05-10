questionnaire_instruct_prompt_template = """
Here is the context of the employee {full_name} and their project involvement, current and targeted competencies, and goals.

Name: {full_name}
Title: {title}
Current and targeted competencies descriptions: {current_and_targeted_competencies}
Development goals: {development_goals}

Project Name: {project_name}
Project Description: {project_description}
Project Goal: {project_goal}
Employee\'s Project role: {project_role}
Employee\'s responsibilities within the project: {project_responsibilities}

Please generate a feedback questionnaire based on that information that teammates can fill out according to the instructions. 
"""

questionnaire_instruct_input_variables = ["full_name", "title", "current_and_targeted_competencies", "development_goals", "project_name", "project_description", "project_goal", "project_role", "project_responsibilities"]
