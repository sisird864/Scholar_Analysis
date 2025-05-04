# Research Impact Analyzer

An interactive Streamlit app that scrapes a Google Scholar profile, visualizes citation trends, and answers your natural-language questions about a researcher’s publications.

## Features

- **Profile Scraping**  
  Fetches up to 20 publications (title, year, citation count) from any Google Scholar user ID using Selenium.

- **Citation Trend Plot**  
  Interactive scatter plot (citations vs. year) powered by Plotly Express.

- **Top Publications Table**  
  Displays the five most-cited papers in a sortable Streamlit DataFrame.

- **AI-Driven Q&A**  
  Ask free-form questions (e.g. “Which year has the highest average citations?”) powered by GPT-4o.

- **Year-Filter Slider**  
  Quickly narrow the dataset to a specific publication year.


## Installation & Configuration

```bash
# 1. Clone the repo
git clone https://github.com/your-username/research-impact-analyzer.git
cd research-impact-analyzer

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set OpenAI API key
export OPENAI_API_KEY="sk-..."

# 5. Download matching ChromeDriver and add to PATH
#    Tweak headless/browser settings in scholar_analysis.py if needed.

## Usage

streamlit run scholar_analysis.py

1. Enter a Google Scholar user ID in the sidebar
2. Wait for scraping to complete
3. Explore the citation trend plot, top-papers table, and AI Q&A box
