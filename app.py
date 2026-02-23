import streamlit as st
from services.transcript import get_transcript_from_url, TranscriptError
from services.chunker import chunk_text_by_tokens, count_tokens
from services.summarizer import summarize_chunk, merge_summaries
from concurrent.futures import ThreadPoolExecutor

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter Password", type="password", key="password", on_change=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Password", type="password", key="password", on_change=password_entered)
        st.error("Incorrect password")
        return False
    else:
        return True

if not check_password():
    st.stop()

st.set_page_config(page_title="YouTube Notes Generator",layout="wide")
st.title("📘 YouTube Structered Notes Generator")
st.write("Generate dynamically structered tehcnical documentation from subtitle-enabled videos")

url = st.text_input("Entire YouTube URL")

if st.button("Generate Notes..."):
    if not url.strip():
        st.warning("Please enter a valid YouTube URL.")
    else:
            try:
                # Fetch Transcript
                transcript = get_transcript_from_url(url)
                # Chunk transcript
                chunks = chunk_text_by_tokens(transcript, max_tokens=2000)
                # Parallel chunk summaries
                with st.spinner("Generating structured notes...."):
                    with ThreadPoolExecutor(max_workers=5) as executor:
                         chunk_summaries = list(
                              executor.map(summarize_chunk,chunks)
                         )
                
                # Final Streaming Merge
                st.markdown("---")
                st.subheader("Final Structured Notes")

                final_placeholder = st.empty()
                full_response=""
                
                for token in merge_summaries(chunk_summaries):
                    full_response+=token
                    final_placeholder.markdown(full_response)

                #Download option
                st.markdown("---")
                st.download_button(label="Download as markdown",data=full_response,file_name="structered_notes.md",mime="text/markdown")

            except TranscriptError as e:
                st.error(str(e))
            except Exception:
                st.error("Something unexpected went wrong.")