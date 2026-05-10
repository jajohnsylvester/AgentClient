import streamlit as st
import requests
import time

# --- Configuration ---
# Replace this with your actual Render service URL
RENDER_URL = "https://multiagent-ktzu.onrender.com/research"

st.set_page_config(page_title="Multi-Agent Research Lab", page_icon="🔬", layout="wide")

st.title("🔬 Multi-Agent Research Lab")
st.markdown("""
We use a **Sequential Agent** pipeline to conduct deep research. 
1. **Researcher Agent**: Scans technical data and facts.
2. **Synthesizer Agent**: Compiles findings into an executive report.
""")

# --- Sidebar ---
st.sidebar.header("Configuration")
target_url = st.sidebar.text_input("Render API URL", value=RENDER_URL)
st.sidebar.info("Ensure your Render service is 'Active' before running.")

# --- Main Interface ---
topic = st.text_area("What topic should we research?", 
                     placeholder="e.g., Impact of Generative AI on Indian Financial Markets 2026")

if st.button("Generate Research Report"):
    if not topic:
        st.warning("Please enter a topic first.")
    else:
        with st.status("Orchestrating Agents...", expanded=True) as status:
            st.write("📡 Sending request to Researcher...")
            
            try:
                # Payload for our FastAPI endpoint
                payload = {"topic": topic}
                
                # Timing the request
                start_time = time.time()
                response = requests.post(target_url, json=payload, timeout=120)
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    status.update(label=f"Research Complete! ({round(end_time - start_time, 2)}s)", state="complete", expanded=False)
                    
                    st.subheader("Final Research Report")
                    st.markdown("---")
                    # Displaying the report returned from the Synthesizer
                    st.markdown(result.get("report", "No content received."))
                    
                    st.download_button(
                        label="Download Report as Text",
                        data=result.get("report", ""),
                        file_name="research_report.txt",
                        mime="text/plain"
                    )
                else:
                    status.update(label="Error in Pipeline", state="error")
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                status.update(label="Request Timed Out", state="error")
                st.error("The research pipeline took too long. Render's free tier may need a moment to warm up.")
            except Exception as e:
                status.update(label="Connection Failed", state="error")
                st.error(f"Could not connect to the agent service: {e}")

# --- Footer ---
st.divider()
st.caption("Developed using Google ADK & Streamlit | Collaborative Intelligence Pipeline")
