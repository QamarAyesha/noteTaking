import streamlit as st
import json
import os

NOTES_FILE = "notes.json"

# Load or initialize notes
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

# Initialize session state
if "notes" not in st.session_state:
    st.session_state.notes = load_notes()

st.title("🗂️ Advanced Note Taking App")

# --- ADD NEW NOTE ---
with st.form("add_note_form"):
    st.subheader("➕ Add a New Note")
    title = st.text_input("Title")
    content = st.text_area("Content", height=100)
    category = st.selectbox("Category", ["General", "Work", "Personal", "Ideas", "Other"])
    submitted = st.form_submit_button("Save Note")
    if submitted and content.strip():
        st.session_state.notes.append({
            "title": title.strip() or "Untitled",
            "content": content.strip(),
            "category": category
        })
        save_notes(st.session_state.notes)
        st.success("Note saved!")

# --- SEARCH & FILTER ---
st.markdown("---")
st.subheader("🔍 Search & Filter")
search_query = st.text_input("Search notes")
selected_category = st.selectbox("Filter by category", ["All"] + sorted({n["category"] for n in st.session_state.notes}))

# --- DISPLAY NOTES ---
st.markdown("---")
st.subheader("📓 Your Notes")

filtered_notes = []
for i, note in enumerate(st.session_state.notes):
    matches_query = search_query.lower() in note["content"].lower() or search_query.lower() in note["title"].lower()
    matches_category = selected_category == "All" or note["category"] == selected_category
    if matches_query and matches_category:
        filtered_notes.append((i, note))

if filtered_notes:
    for i, note in filtered_notes:
        with st.expander(f"{note['title']} [{note['category']}]"):
            st.markdown(note["content"])
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 Edit", key=f"edit_{i}"):
                    st.session_state.edit_index = i
            with col2:
                if st.button("❌ Delete", key=f"delete_{i}"):
                    st.session_state.notes.pop(i)
                    save_notes(st.session_state.notes)
                    st.rerun()
else:
    st.info("No notes match your search/filter.")

# --- EDIT NOTE ---
if "edit_index" in st.session_state:
    edit_idx = st.session_state.edit_index
    note_to_edit = st.session_state.notes[edit_idx]
    
    st.markdown("---")
    st.subheader("✏️ Edit Note")
    new_title = st.text_input("Edit Title", note_to_edit["title"], key="edit_title")
    new_content = st.text_area("Edit Content", note_to_edit["content"], height=100, key="edit_content")
    new_category = st.selectbox("Edit Category", ["General", "Work", "Personal", "Ideas", "Other"], 
                                index=["General", "Work", "Personal", "Ideas", "Other"].index(note_to_edit["category"]))

    if st.button("✅ Update Note"):
        st.session_state.notes[edit_idx] = {
            "title": new_title,
            "content": new_content,
            "category": new_category
        }
        save_notes(st.session_state.notes)
        del st.session_state["edit_index"]
        st.success("Note updated!")
        st.rerun()


