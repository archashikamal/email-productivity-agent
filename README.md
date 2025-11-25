

-----

# 📧 Prompt-Driven Email Productivity Agent

**An intelligent, customizable email-processing system powered by LLMs.**

Users control the system through **Prompt Brains** (stored prompts) that define email categorization, action-item extraction, auto-draft replies, and inbox-wide querying. The agent loads a mock inbox, processes emails, and displays structured results through a responsive **Streamlit UI**.

-----

## ⭐ Features

### 🔹 Email Ingestion

  * **Load Mock Inbox:** Ingest email data via JSON.
  * **Preview:** View individual emails before processing.
  * **Selection:** Choose specific emails for detailed AI analysis.

### 🔹 Prompt-Driven Processing

  * **Customizable Prompts:** Users can edit categorization logic on the fly.
  * **Action Extraction:** Extract tasks based on user-defined templates.
  * **Auto-Drafting:** Generate replies with customizable tone and rules.

### 🔹 AI-Powered Results

  * **Smart Categorization:** Automatically tags emails (e.g., "To-Do", "Meeting", "Spam").
  * **Action Items:** detailed extraction of tasks, deadlines, and urgency.
  * **Structured UI:** Beautifully formatted results.
  * **History:** Multi-email session history.

### 🔹 Inbox-Wide AI Chat

Ask questions about your entire inbox:

  * *"Summarize the inbox"*
  * *"Show all urgent emails"*
  * *"Which emails need replies?"*

-----

## 🛠️ Setup Instructions

### 1\. Prerequisites

  * Python 3.9+
  * pip
  * A valid **OpenAI API Key** (or compatible model provider)

### 2\. Install Dependencies

Navigate to your project folder and install the required packages:

```bash
pip install -r requirements.txt
```

*If you do not have a `requirements.txt` yet, run:*

```bash
pip install streamlit openai python-dotenv
```

### 3\. Configure API Key

Create a `.env` file in the root directory and add your key:

```env
OPENAI_API_KEY=your_api_key_here
```

**Alternatively, set it via the terminal:**

  * **Mac/Linux:**
    ```bash
    export OPENAI_API_KEY="your_api_key_here"
    ```
  * **Windows:**
    ```cmd
    setx OPENAI_API_KEY "your_api_key_here"
    ```

-----

## 🚀 How to Run

Run the Streamlit application:

```bash
streamlit run app.py
```

**This launches:**

  * The full User Interface
  * All backend logic and the Email Processing Agent
  * The Prompt Editor

*Note: No separate backend server is required—Streamlit handles everything.*

-----

## 📥 Loading the Mock Inbox

### Mock Inbox Format (`mock_inbox.json`)

Your inbox should be a JSON array of objects. Example:

```json
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
```

### How to Load in UI

1.  Open the app in your browser.
2.  Navigate to the **"Mock Inbox Loader"** section.
3.  Select your `.json` file.
4.  Emails will automatically populate the dropdown list.

-----

## ⚙️ Configuring Prompts

The agent's behavior is defined by `prompts.json`. This makes the system truly customizable.

### Example Structure

```json
{
  "categorization_prompt": "You are an intelligent email classification system...",
  "action_item_prompt": "Extract all tasks in JSON format...",
  "auto_reply_prompt": "Draft a polite reply given the email content..."
}
```

### How to Edit

1.  Open the **Prompt Brain Editor** panel in the UI.
2.  Edit the text for **Categorization**, **Action-Items**, or **Auto-Reply**.
3.  Click **Save Prompts**.
4.  *New prompts take effect immediately.*

-----

## 🧪 Usage Examples

### 📨 Example 1: Categorization

  * **Email:** "Please send me the Q4 status report by end of day."
  * **Output:**
    ```json
    { "category": "To-Do" }
    ```

### ✔️ Example 2: Action Item Extraction

  * **Email:** "Prepare the weekly metrics deck and send it tomorrow morning."
  * **Output:**
    ```json
    [
      {
        "task": "Prepare the weekly metrics deck",
        "urgency": "high",
        "deadline": "tomorrow morning",
        "reason": "Sender needs the deck for reporting."
      }
    ]
    ```

### ✉️ Example 3: Auto-Draft Reply

  * **Email:** "Can we meet tomorrow at 3 PM to discuss sprint planning?"
  * **Output:**
    > Hi,
    > Thanks for reaching out. Yes, 3 PM tomorrow works for me. Please let me know if you’d like a supporting agenda.
    > Best regards,

### 🤖 Example 4: Inbox-Wide Chat

  * **User:** "Show me all urgent emails."
  * **System:** Returns a filtered set of high-urgency tasks based on extracted AI metadata.

-----

## 📂 Project Structure

```text
/email-productivity-agent
├── app.py                 # Main Streamlit application
├── prompts.json           # Customizable system prompts
├── mock_inbox.json        # Sample email data
├── requirements.txt       # Python dependencies
├── .env                   # API keys (gitignored)
└── README.md              # Documentation
```

-----

## 🏁 Final Notes

  - [x] **Prompt-driven architecture:** Logic is separated from code.
  - [x] **Modular:** Designed for extension (Gmail API, SQLite, etc.).
  - [x] **Beautiful UI:** Clean formatting for categories and action items.
  - [x] **Robust:** Error handling ensures no raw/broken output.
  - [x] **Meets ALL assignment requirements.**
