# In this example, we will demonstrate how
import os
import streamlit as st  
from helper_functions.utility import check_password  
from helper_functions import llm 
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool

st.set_page_config(
    layout="centered",
    page_title="Specfications Drafter"
)

st.title("Specifications Drafter")

# Check if the password is correct.  
if not check_password():  
    st.stop()

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

# Create a new instance of the WebsiteSearchTool
# Set the base URL of a website, e.g., "https://example.com/", so that the tool can search for sub-pages on that website
tool_websearch = WebsiteSearchTool("https://www.gebiz.gov.sg/ptn/opportunity/BOListing.xhtml?origin=menu")


# Creating Agents
agent_assembler = Agent(
    role="Information Assembler",
    goal="Collate factually accurate content on {topic}",
    backstory="""You are responsible to source for information relevant to the {topic}. You should collect the information in the document name "specifications", "SOR" or "SOW" from the website on {topic}.""",
 
    allow_delegation=False, # <-- This is now set to False
	verbose=True,
)

agent_analyst = Agent(
    role="Analyst",
    goal="Conduct in-depth research on the item: {topic}",
    backstory="""You provide in-depth analyse of the information compiled by the Information Assembler.""",

     allow_delegation=False,
    verbose=True,
)

agent_writer = writer = Agent(
    role="Specifications Writer",
    goal="Write a factually accurate specifications to purchase the item: {topic}",
    backstory="""You're working on a writing the specification about the item: {topic}. You base your writing on the report prepared by the Analyst.""",
    
    allow_delegation=False,
    verbose=True,
)


# <---------------------------------- Creating Tasks ---------------------------------->
task_assemble = Task(
    description="""\
    1. Source for information relevant to the {topic}.
    2. Identify the technical information and key performance indicator.
    3. Develop a detailed specfication outline, including background and key points.""",

    expected_output="""\
    A comprehensive specifications outline with a Contract Duration, Contracting Authority, Background Information, Scope of Work (Includes Performance Indicators), delivery schedule (in table form), payment milestones (in table form) and contact person.""",
    agent=agent_assembler,
    tools=[tool_websearch],

    async_execution=True # Will be executed asynchronously [NEW]
)

task_analyse = Task(
    description="""\
    1. Conduct in-depth analysis on the {topic}.
    2. Provide the Specifications Writer with a succinct report based on the information gathered by the Information Assembler.
    3. Provide additional insights and resources to enhance the report.""",
   
    expected_output="""\
    A detailed report with a Contract Duration, Contracting Authority, Background Information, Scope of Work (Includes Performance Indicators), delivery schedule (in table form), payment milestones (in table form) and contact person.""",

    agent=agent_analyst,
    
    async_execution=True # Will be executed asynchronously [NEW]
)

task_write = Task(
    description="""\
    1. Use the detailed report to craft a comprehensive specifcations to purchase {topic}.
    2. Sections are properly named and annotated in bold.
    3. Ensure the doucment is written in a clear and direct manner.
    4. Proofread for grammatical errors and alignment the common style used in business report.
    5. You MUST check with human users to get their feedback on the content, and incorporate the suggestion to revise the content.""",

    expected_output="""
    A well-written specifications "in markdown.markdown format, ready for publication, each section should have 1 or 2 paragraphs.""",
    agent=agent_writer,
    # human_input=True, # Remove user input for this task [NEW]

    context=[task_assemble, task_analyse], # Will wait for the output of the two tasks to be completed,
)


# <---------------------------------- Creating the Crew ---------------------------------->
crew = Crew(
    agents=[agent_assembler, agent_analyst, agent_writer],
    tasks=[task_assemble, task_analyse, task_write],
    verbose=True
)

# <---------------------------------- Running the Crew ---------------------------------->
if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = crew.kickoff(inputs={"topic":f"User Input Submitted - {user_prompt}"})
    st.write(response) 
    print(f"User Input is {user_prompt}")