import streamlit as st
from services.transcript import get_transcript_from_url, TranscriptError
from services.chunker import chunk_text_by_tokens, count_tokens
from services.summarizer import summarize_chunk, merge_summaries
from services.pdf_generator import generate_pdf
from services.prompt_builder import merge_prompt, chunk_prompt
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="YouTube Notes Generator",layout="wide")
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

h1, h2, h3 {
    font-weight: 600;
}

.sidebar .sidebar-content {
    padding-top: 1.5rem;
}

div.stButton > button {
    border-radius: 8px;
    height: 3em;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)
with st.sidebar:
     st.header("⚙️ Input parameters")
     url = st.text_input("YouTube URL")

     detail_level = st.selectbox("Detail Level",["Concise","Standard","In-depth"])

     tone = st.selectbox("Tone", ["Professional","Academic","Beginner Friendly"])

     include_breakdown=st.checkbox("Include technical breakdown",value=True)

     max_sections = st.slider("Maximum Major Sections",min_value=1,max_value=10,value=5)

     generate = st.button("Generate Notes",use_container_width=True)
     st.divider()

st.title("📘 YouTube Technical Notes Generator")
st.write("Generate dynamically structered tehcnical documentation from video transcripts")

st.divider()

if generate and url:
    if not url.strip():
        st.warning("Please enter a valid YouTube URL.")
    else:
            try:
                # Fetch Transcript
                transcript = get_transcript_from_url(url)
                # Chunk transcript
                chunks = chunk_text_by_tokens(transcript, max_tokens=2000)
                chunk_messages =[chunk_prompt(chunk) for chunk in chunks]
                # Parallel chunk summaries
                with st.spinner("Generating structured notes...."):
                    with ThreadPoolExecutor(max_workers=5) as executor:
                         chunk_summaries = list(
                              executor.map(summarize_chunk,chunk_messages)
                         )
                
                # Final Streaming Merge

                final_placeholder = st.empty()
                full_response=""

                merge_messages = merge_prompt("\n\n".join(chunk_summaries),
                                              detail_level,
                                              tone,
                                              include_breakdown,
                                              max_sections)
                
                for token in merge_summaries(merge_messages):
                    full_response+=token
                    final_placeholder.markdown(full_response)

                #Download option
                st.markdown("---")
                pdf_file =generate_pdf(full_response)
                st.download_button(label="📄 Download as PDF",data=pdf_file,file_name="structered_notes.pdf",mime="application/pdf")

            except TranscriptError as e:
                st.error(str(e))
            except Exception as e:
                st.exception(e)