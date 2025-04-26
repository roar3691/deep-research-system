# deep_research_system/app.py
import streamlit as st
from main import run_deep_research, TAVILY_API_KEY, OPENROUTER_API_KEY

st.set_page_config(page_title="Deep Research AI System", page_icon="🔍")

st.title("Deep Research AI System")
st.markdown("Enter a query to perform deep research using AI agents powered by Tavily and OpenRouter.")

# Check API keys
if not TAVILY_API_KEY:
    st.error("TAVILY_API_KEY is not set. Please add it to the .env file.")
    st.stop()
if not OPENROUTER_API_KEY:
    st.error("OPENROUTER_API_KEY is not set. Please add it to the .env file.")
    st.stop()

# Input query
query = st.text_input("Enter your research query:", placeholder="e.g., What are the latest advancements in AI for healthcare?")
if st.button("Run Research"):
    if query:
        with st.spinner("Researching... This may take a moment."):
            try:
                result = run_deep_research(query)
                
                # Display final answer
                st.subheader("Final Answer")
                st.write(result["final_answer"])
                
                # Display research data
                st.subheader("Research Data")
                for data in result["research_data"]:
                    with st.expander(f"Source: {data['url']}"):
                        st.markdown(f"**Summary**: {data['summary']}")
                        st.markdown(f"**Content**: {data['content'][:500]}... [Read more]({data['url']})")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a query.")