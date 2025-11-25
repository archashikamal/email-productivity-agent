import json
import streamlit as st
from openai import OpenAI



# -------------------------
# Helper to fix broken JSON
# -------------------------
def force_json_fix(text):
    import json, re

    # 1. Direct JSON
    try:
        return json.loads(text)
    except:
        pass

    # 2. Extract JSON-like part
    match = re.search(r"\{.*\}|\[.*\]", text, re.S)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    # 3. Final fallback
    return {"error": "Invalid JSON", "raw": text}


# -----------------------------------------
# GLOBAL CSS (UI Polish)
# -----------------------------------------
st.set_page_config(page_title="Email Productivity Agent", layout="wide")

st.markdown("""
<style>

    .section-card {
        padding: 20px; 
        border-radius: 12px;
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .stButton>button {
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        background: linear-gradient(90deg, #4F8BF9, #7AB6FF);
        color: white;
        border: none;
    }

    .stButton>button:hover { opacity: 0.9; }

    div[data-testid="stExpander"] > details {
        border-radius: 10px;
        border: 1px solid #333;
        padding: 6px;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# OPENAI
# -----------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------------------
# LOAD/SAVE PROMPTS
# -----------------------------------------
def load_prompts(path="data/prompts.json"):
    with open(path, "r") as f:
        return json.load(f)

def save_prompts(prompts, path="data/prompts.json"):
    with open(path, "w") as f:
        json.dump(prompts, f, indent=4)

# -----------------------------------------
# LOAD EMAILS
# -----------------------------------------
def load_emails(path="data/mock_inbox.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------------------
# LLM CALLER
# -----------------------------------------
def run_llm(system_prompt, email_body):
    wrapped_body = f"EMAIL CONTENT:\n{email_body}\n\nNow follow the above instructions."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": wrapped_body},
        ],
    )

    return response.choices[0].message.content

# -----------------------------------------
# STREAMLIT APP
# -----------------------------------------
def main():

    st.title("Email Productivity Agent")
    st.write("Inbox + Prompt Brain + AI Processing + Agent + Drafts 🎉")

    # -----------------------------------------
    # SIDEBAR
    # -----------------------------------------
    st.sidebar.title("🧠 Prompt Brain")
    prompts = load_prompts()

    categorization_input = st.sidebar.text_area(
        "Categorization Prompt", prompts["categorization_prompt"], height=120
    )
    action_input = st.sidebar.text_area(
        "Action Item Prompt", prompts["action_item_prompt"], height=120
    )
    auto_reply_input = st.sidebar.text_area(
        "Auto-Reply Prompt", prompts["auto_reply_prompt"], height=120
    )

    if st.sidebar.button("Save Prompts"):
        save_prompts({
            "categorization_prompt": categorization_input,
            "action_item_prompt": action_input,
            "auto_reply_prompt": auto_reply_input
        })
        st.sidebar.success("Prompts Updated ✔️")

    # -----------------------------------------
    # TABS
    # -----------------------------------------
    inbox_tab, agent_tab, drafts_tab = st.tabs(
        ["📥 Inbox", "🤖 Agent", "✉️ Drafts"]
    )

    # ==================================================
    # TAB 1 — INBOX
    # ==================================================
    with inbox_tab:

        st.markdown("<div class='section-title'>📥 Inbox Loader</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)

        if st.button("Load Mock Inbox"):
            st.session_state["emails"] = load_emails()
            st.success(f"Loaded {len(st.session_state['emails'])} emails 🌟")
        else:
            st.info("Click to load inbox.")

        # Show emails
        if "emails" in st.session_state:
            st.write("### Emails")
            for email in st.session_state["emails"]:
                with st.expander(f"{email['subject']} — from {email['sender']}"):
                    st.write(f"**From:** {email['sender']}")
                    st.write(f"**Subject:** {email['subject']}")
                    st.write(f"**Time:** {email['timestamp']}")
                    st.write(email["body"])

        st.markdown("</div>", unsafe_allow_html=True)

        # --------------------------
        # AI PROCESSOR — one email at a time
        # --------------------------
        st.write("---")
        st.subheader("🤖 AI Email Processing")

        if "emails" not in st.session_state:
            st.info("Load the inbox first.")
        else:

            email_labels = [
                f"{i+1}. {e['subject']} — {e['sender']}"
                for i, e in enumerate(st.session_state["emails"])
            ]

            selected_label = st.selectbox(
                "Choose an email to process:",
                email_labels,
                key="process_one"
            )

            selected_index = email_labels.index(selected_label)
            selected_email = st.session_state["emails"][selected_index]

            with st.expander("Preview Email"):
                st.write(f"**Subject:** {selected_email['subject']}")
                st.write(f"**From:** {selected_email['sender']}")
                st.write(selected_email["body"])

            if st.button("Process Selected Email With AI"):
                prompts = load_prompts()

                if "processed" not in st.session_state:
                    st.session_state["processed"] = []

                with st.spinner("AI Thinking..."):
                    progress = st.progress(0)

                    try:
                        c = run_llm(prompts["categorization_prompt"], selected_email["body"])
                        progress.progress(50)

                        a = run_llm(prompts["action_item_prompt"], selected_email["body"])
                        progress.progress(100)

                        st.session_state["processed"].append({
                            "email": selected_email,
                            "category": force_json_fix(c),
                            "actions": force_json_fix(a),

                        })
                        st.success("Processing Complete ✔️")

                    except Exception as e:
                        st.error(f"AI Error: {e}")

    # -------------------------------
    # 📊 AI Results (clean formatted output)
    # -------------------------------
    if "processed" in st.session_state and st.session_state["processed"]:
        st.subheader("📊 Processed Emails")

        import json

        for item in st.session_state["processed"]:
            email = item["email"]

            with st.expander(f"{email['subject']} — Results"):

                # -----------------------------
                # Category (pretty formatted)
                # -----------------------------
                st.write("### 🏷️ Category")

                try:
                    category_json = json.loads(item["category"])
                    st.json(category_json)
                except Exception:
                    st.code(item["category"])

                st.write("")

                # -----------------------------
                # Action Items (beautiful UI)
                # -----------------------------
                st.write("### 📝 Action Items")

                try:
                    actions_json = json.loads(item["actions"])

                    # Case 1: action items list
                    if isinstance(actions_json, list):

                        if len(actions_json) == 0:
                            st.info("No action items found for this email.")

                        for action in actions_json:
                            st.markdown(
                                f"""
                                <div style="
                                    background-color:#0d1117;
                                    padding:15px;
                                    border-radius:10px;
                                    margin-bottom:12px;
                                    border:1px solid #30363d;
                                    font-size:14px;
                                    line-height:1.5;
                                ">
                                    <b>📝 Task:</b> {action.get("task")}<br>
                                    <b>⏱️ Urgency:</b> {action.get("urgency")}<br>
                                    <b>📅 Deadline:</b> {action.get("deadline")}<br>
                                    <b>💡 Reason:</b> {action.get("reason")}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    # Case 2: JSON but not list
                    else:
                        st.json(actions_json)

                except Exception:
                    st.code(item["actions"])

                st.write("")

    else:
        st.info("No processed emails yet.")

    # ==================================================
    # TAB 2 — AGENT
    # ==================================================
    with agent_tab:

        st.subheader("💬 Email Agent Chat")

        if "processed" not in st.session_state:
            st.info("Process at least 1 email first.")
        else:

            # pick email
            subjects = [item["email"]["subject"] for item in st.session_state["processed"]]
            selected_subject = st.selectbox(
                "Select email:",
                subjects,
                key="agent_email"
            )

            selected_email = next(
                item for item in st.session_state["processed"]
                if item["email"]["subject"] == selected_subject
            )

            st.write("### Email Content")
            st.write(selected_email["email"]["body"])

            user_query = st.text_input(
                "Ask something about this email:", 
                key="agent_query"
            )

            if st.button("Ask Email Agent"):

                prompts = load_prompts()

                agent_prompt = f"""
You are an advanced, context-aware Email Intelligence Assistant.

Your goals:
- Understand the sender’s intent
- Explain tone, urgency, meaning
- Identify risks or spam signals
- Extract tasks when asked
- Give human-quality reasoning
- Avoid JSON unless user asks
- Provide intelligent, descriptive answers

EMAIL:
{selected_email["email"]["body"]}

QUESTION:
{user_query}

Respond with the clearest, most helpful explanation.
"""

                try:
                    answer = run_llm(agent_prompt, selected_email["email"]["body"])
                    st.write("### 🤖 Agent Response")
                    st.write(answer)

                except Exception as e:
                    st.error(f"AI Error: {e}")

        # -------------------------
        # INBOX WIDE CHAT
        # -------------------------
        st.write("---")
        st.subheader("🧠 Inbox-Wide AI Chat")

        if "processed" not in st.session_state:
            st.info("Process emails first.")
        else:

            inbox_query = st.text_input(
                "Ask something about the *entire inbox*:",
                key="inbox_query"
            )

            if st.button("Ask Inbox AI"):

                all_emails_text = ""
                for item in st.session_state["processed"]:
                    e = item["email"]
                    all_emails_text += f"""
SUBJECT: {e['subject']}
FROM: {e['sender']}
BODY: {e['body']}

"""

                inbox_prompt = f"""
You are an Inbox Analysis Assistant.

User question:
{inbox_query}

All emails:
{all_emails_text}

Give helpful, smart insights about the entire inbox.
"""

                try:
                    answer = run_llm(inbox_prompt, all_emails_text)
                    st.write("### 🤖 Inbox AI Response")
                    st.write(answer)

                except Exception as e:
                    st.error(f"AI Error: {e}")

    # ==================================================
    # TAB 3 — DRAFTS
    # ==================================================
    with drafts_tab:

        st.subheader("✉️ Draft Email Reply")

        if "processed" not in st.session_state:
            st.info("Process emails first.")
        else:

            subjects = [item["email"]["subject"] for item in st.session_state["processed"]]

            draft_subject = st.selectbox(
                "Select email to reply to:",
                subjects,
                key="draft_email"
            )

            draft_email = next(
                item["email"]
                for item in st.session_state["processed"]
                if item["email"]["subject"] == draft_subject
            )

            st.write("### Email Content")
            st.write(draft_email["body"])

            if st.button("Draft Reply"):
                prompts = load_prompts()

                draft_prompt = f"""
Write a polite, concise reply using this rule:
{prompts["auto_reply_prompt"]}

Email:
{draft_email["body"]}
"""

                try:
                    reply = run_llm(draft_prompt, draft_email["body"])
                    st.session_state["current_draft"] = {
                        "subject": f"Re: {draft_email['subject']}",
                        "body": reply
                    }
                    st.success("Draft generated!")
                except Exception as e:
                    st.error(f"AI Error: {e}")

            if "current_draft" in st.session_state:
                st.write("### 📝 Edit Draft")

                subject_edit = st.text_input(
                    "Subject",
                    st.session_state["current_draft"]["subject"]
                )
                body_edit = st.text_area(
                    "Draft Body",
                    st.session_state["current_draft"]["body"],
                    height=200
                )

                if st.button("Save Draft"):
                    if "saved_drafts" not in st.session_state:
                        st.session_state["saved_drafts"] = []

                    st.session_state["saved_drafts"].append(
                        {"subject": subject_edit, "body": body_edit}
                    )
                    st.success("Draft Saved ✔️")

        # Saved drafts display
        st.write("---")
        st.subheader("📂 Saved Drafts")

        if "saved_drafts" in st.session_state:
            for i, d in enumerate(st.session_state["saved_drafts"]):
                with st.expander(f"Draft {i+1}: {d['subject']}"):
                    st.write(d["body"])
        else:
            st.info("No drafts saved yet.")

# -----------------------------------------
# RUN APP
# -----------------------------------------
if __name__ == "__main__":
    main()
