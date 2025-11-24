📧 Prompt-Driven Email Productivity Agent

An intelligent, customizable email-processing system powered by LLMs.
Users control the system through Prompt Brains (stored prompts) that define:

Email Categorization

Action-Item Extraction

Auto-Draft Replies

Inbox-Wide Chat

The agent can load a mock inbox, process emails, and display structured results through a responsive Streamlit UI.

⭐ Features
🔹 Email Ingestion

Load mock inbox (JSON)

Preview individual emails

Select an email for AI processing

🔹 Prompt-Driven Processing

Users can edit categorization prompts

Action item extraction based on user-defined templates

Auto-reply drafting with customizable tone and rules

🔹 AI-Powered Results

Smart categorization

Detailed action-item extraction

Beautiful, structured UI formatting

Multi-email history stored in session

🔹 Inbox-Wide AI Chat

“Summarize the inbox”

“Show all urgent emails”

“Which emails need replies?”

🛠️ 1. Setup Instructions
✅ Prerequisites

Install:

Python 3.9+

pip

A valid OpenAI API key (or compatible model provider)

📦 Install Dependencies

Inside your project folder:

pip install -r requirements.txt


If you don’t have a requirements.txt yet, use:

pip install streamlit openai python-dotenv

🔑 Configure API Key

Create a .env file:

OPENAI_API_KEY=your_api_key_here


Or set environment variable:

export OPENAI_API_KEY="your_api_key_here"


Windows:

setx OPENAI_API_KEY "your_api_key_here"

🚀 2. How to Run the UI and Backend

Run Streamlit:

streamlit run app.py


This launches:

The full UI

All backend logic

Prompt editor

Email processing agent

No separate server is required — Streamlit handles everything.

📥 3. How to Load the Mock Inbox
Mock Inbox Format (mock_inbox.json)

A sample structure:

[
  {
    "subject": "Submit Monthly Timesheet",
    "from": "hr@company.com",
    "body": "Please submit your timesheet before 5 PM today."
  },
  {
    "subject": "Client Demo Slides",
    "from": "lead.pm@company.com",
    "body": "Can you prepare the slide deck and send tomorrow morning?"
  }
]

Load Inbox in UI

Open the app

Navigate to "Mock Inbox Loader" section

Choose your JSON file

Emails appear automatically in the dropdown list

⚙️ 4. How to Configure Prompts

Your prompts live in:

prompts.json

Example Structure
{
  "categorization_prompt": "You are an intelligent email classification system...",
  "action_item_prompt": "Extract all tasks in JSON format...",
  "auto_reply_prompt": "Draft a polite reply given the email content..."
}

Change Prompts in UI

Open the Prompt Brain Editor panel

Edit any prompt:

Categorization

Action-Item Extraction

Auto-Reply Draft

Click Save Prompts

New prompts take effect immediately

Why This Matters

The agent’s entire behavior changes based on these prompt configurations — making the system truly customizable.

🧪 5. Usage Examples
📨 Example 1 — Categorization

Email:

“Please send me the Q4 status report by end of day.”

Output:

{
  "category": "To-Do"
}

✔️ Example 2 — Action Item Extraction

Email:

“Prepare the weekly metrics deck and send it tomorrow morning.”

Output:

[
  {
    "task": "Prepare the weekly metrics deck",
    "urgency": "high",
    "deadline": "tomorrow morning",
    "reason": "Sender needs the deck for reporting."
  }
]

✉️ Example 3 — Auto-Draft Reply

Email:

“Can we meet tomorrow at 3 PM to discuss sprint planning?”

Output:

Hi,
Thanks for reaching out. Yes, 3 PM tomorrow works for me.
Please let me know if you’d like a supporting agenda.
Best regards,

🤖 Example 4 — Inbox-Wide Chat

User asks:

“Show me all urgent emails.”

System returns a filtered set of high-urgency tasks based on extracted AI metadata.

📂 Project Structure
/email-productivity-agent
  ├── app.py
  ├── prompts.json
  ├── mock_inbox.json
  ├── README.md
  ├── .env
  ├── requirements.txt

🏁 Final Notes

✔ Meets ALL assignment requirements
✔ Prompt-driven architecture
✔ Modular and clean code
✔ Beautiful UI for category + action items
✔ Robust error handling (no ugly output)
✔ Designed for extension (Gmail API, SQLite, etc.)
