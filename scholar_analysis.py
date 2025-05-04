import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class ScholarAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key) # use your own API key for testing
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.data = None
        
    def get_paper_data(self, scholar_id):
        driver = webdriver.Chrome(options=self.chrome_options)
        url = f'https://scholar.google.com/citations?user={scholar_id}&hl=en'
        papers_data = []
        
        try:
            driver.get(url)
            papers = driver.find_elements(By.CLASS_NAME, 'gsc_a_tr')
            for paper in papers[:20]:
                title_elem = paper.find_element(By.CLASS_NAME, 'gsc_a_at')
                title = title_elem.text
                citations = paper.find_element(By.CLASS_NAME, 'gsc_a_ac').text
                year = paper.find_element(By.CLASS_NAME, 'gsc_a_y').text
                papers_data.append({
                    'title': title,
                    'year': year,
                    'citations': int(citations) if citations.isdigit() else 0
                })
        finally:
            driver.quit()
            
        self.data = pd.DataFrame(papers_data)
        return self.data
        
    def answer_query(self, query):
        if self.data is None:
            return "Please analyze a profile first"
            
        context = f"Publications data: {self.data.to_string()}\nAnalyze based on query: {query}"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": context}]
        )
        return response.choices[0].message.content

def main():
    st.title("Research Impact Analyzer")
    scholar_id = st.text_input("Enter Google Scholar ID")
    
    if scholar_id:
        api_key = st.secrets["OPENAI_API_KEY"]
        analyzer = ScholarAnalyzer(api_key)
        
        with st.spinner("Analyzing research impact..."):
            df = analyzer.get_paper_data(scholar_id)
            
            st.subheader("Citation Trends")
            fig = px.scatter(df, x='year', y='citations', hover_data=['title'])
            st.plotly_chart(fig)
            
            st.subheader("Most Cited Papers")
            st.dataframe(df.nlargest(5, 'citations'))
            
            st.subheader("Ask Questions")
            query = st.text_input("What would you like to know about this researcher?")
            if query:
                response = analyzer.answer_query(query)
                st.write(response)
            
            year_filter = st.slider("Filter by Year", 
                                  min_value=int(df['year'].min()),
                                  max_value=int(df['year'].max()))
            filtered_df = df[df['year'] == str(year_filter)]
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main()

    