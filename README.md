
---

# LangChain + Groq URL Summarizer

A Streamlit web app to **summarize content from YouTube videos or websites** using LangChain with Groq's `llama3-70b-8192` model. This app dynamically loads video transcripts or webpage text, then generates concise summaries using a customizable prompt. It also optionally integrates LangSmith tracing for enhanced observability.



## Features

* Input a **YouTube** or **any website URL** to extract content dynamically.
* Use **Groq's LLM** via `langchain_groq.ChatGroq` for advanced summarization.
* Summarize content in under **300 words** using a customizable prompt.
* Optional **LangSmith tracing** integration for detailed logging and monitoring.
* Responsive **Streamlit UI** for easy interaction.
* User-friendly error handling and input validation.



## Demo Screenshot

### App Demo
<img width="1416" alt="image" src="https://github.com/user-attachments/assets/bb068cc0-20ec-482c-a991-8b80e5e00732" />

### Langsmith Demo
<img width="1691" alt="image" src="https://github.com/user-attachments/assets/581efb2f-99c0-4fec-8951-0f1fe6d06c7a" />
<br>
<img width="1695" alt="image" src="https://github.com/user-attachments/assets/37c0e4aa-6c66-4563-9c45-4b2d7cb10ef3" />
<br>
<img width="1688" alt="image" src="https://github.com/user-attachments/assets/8563473a-52be-4a12-baae-1c6d05b41c59" />

### Groq Cloud Demo
<img width="1708" alt="image" src="https://github.com/user-attachments/assets/2f56c75e-fe46-463d-bd27-9d22982fbbc2" />
<br>
<img width="1692" alt="image" src="https://github.com/user-attachments/assets/e89b1cbf-eab4-4463-90eb-7f70f2cc0e73" />
<br>
<img width="1696" alt="image" src="https://github.com/user-attachments/assets/65b0ffa3-3099-4a84-8bd5-504060e00720" />








## Getting Started

### Prerequisites

* Python 3.8+
* [Groq API key](https://groq.ai/) (sign up required)
* Optional: LangSmith API key for tracing (sign up at [LangSmith](https://langsmith.langchain.com/))

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/langchain-groq-url-summarizer.git
   cd langchain-groq-url-summarizer
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional for tracing
   LANGSMITH_PROJECT=yt_url_summary                # Optional LangSmith project name
   LANGSMITH_RUN_NAME=yt_or_web_summary            # Optional LangSmith run name
   ```

---

## Usage

Run the Streamlit app locally:

```bash
streamlit run app.py
```

### Using the App

* Enter a **valid YouTube or Website URL** in the input field.
* Ensure your **Groq API key** is set (via `.env` or sidebar input).
* Optionally enable **LangSmith tracing** using the sidebar checkbox.
* Click **"Summarize the Content"** to start.
* View the generated summary below the button.

---

## How it Works

1. **URL Input & Validation:**

   * The app accepts URLs and validates their format.
   * Recognizes YouTube URLs separately for transcript extraction.

2. **Content Loading:**

   * For YouTube URLs, it uses `YoutubeLoader` from `langchain_community` to fetch video transcripts and metadata.
   * For other URLs, it uses `UnstructuredURLLoader` to scrape webpage content with custom headers.

3. **Language Model Setup:**

   * Uses Groq's LLM (`llama3-70b-8192`) through `ChatGroq` with the provided API key.

4. **Summarization Chain:**

   * Constructs a summarization prompt requesting a concise, informative summary under 300 words.
   * Uses LangChain’s `load_summarize_chain` with the "stuff" method for simple context concatenation.

5. **LangSmith Tracing (Optional):**

   * If enabled, sets environment variables and attempts to trace the chain execution.
   * Warns if `wrap_chain` is unavailable in the installed LangSmith package.

6. **Display:**

   * Shows progress spinner during loading and summarization.
   * Outputs the final summary or error messages.

---

## Dependencies

* `streamlit`
* `python-dotenv`
* `validators`
* `langchain`
* `langchain_groq`
* `langchain_community`
* `langsmith` (optional)
* `requests` (indirect via loaders)

---

## Environment Variables

| Variable             | Description                               | Required |
| -------------------- | ----------------------------------------- | -------- |
| `GROQ_API_KEY`       | API key for Groq LLM access               | Yes      |
| `LANGSMITH_API_KEY`  | API key for LangSmith tracing             | No       |
| `LANGSMITH_PROJECT`  | LangSmith project name for grouping runs  | No       |
| `LANGSMITH_RUN_NAME` | LangSmith run name for this summarization | No       |

---

## Customization

* **Prompt**: Modify the `prompt_template` in the code to change the summary style or length.
* **Model**: Change the `model` parameter in `ChatGroq()` to use other Groq models.
* **Loaders**: Extend or replace loaders to support other content types or formats.
* **UI**: Enhance Streamlit frontend for richer user experience or additional features.

---

## Troubleshooting

* **Invalid API Key**: Ensure `GROQ_API_KEY` is valid and set in `.env` or sidebar.
* **Content Loading Issues**: Some websites might block scrapers or require additional headers.
* **LangSmith Tracing Errors**: Make sure `langsmith` package is installed and up to date.
* **Performance**: Large web pages or very long transcripts may slow summarization.

