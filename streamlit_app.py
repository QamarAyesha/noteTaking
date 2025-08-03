import streamlit as st

st.title("📝 Simple Note Taking App")

# Initialize notes list in session state
if "notes" not in st.session_state:
    st.session_state.notes = []

# Input for new note
with st.form("note_form", clear_on_submit=True):
    note_text = st.text_area("Write your note here:", height=100)
    submitted = st.form_submit_button("Add Note")
    if submitted and note_text.strip():
        st.session_state.notes.append(note_text.strip())
        st.success("Note added!")

st.markdown("---")
st.header("📒 Your Notes")

# Display notes
if st.session_state.notes:
    for i, note in enumerate(st.session_state.notes):
        with st.expander(f"Note {i+1}"):
            st.write(note)
            if st.button("Delete", key=f"del_{i}"):
                st.session_state.notes.pop(i)
                st.rerun()
else:
    st.info("No notes yet. Start writing above!")

