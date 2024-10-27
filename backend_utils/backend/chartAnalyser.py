import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from groq import Groq
import json
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class ChartAnalyzer:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        
    def create_sample_data(self) -> pd.DataFrame:
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
        sales_data = {
            'Date': dates,
            'Sales': [120, 135, 150, 145, 160, 175, 190, 185, 200, 210, 205, 220],
            'Category': ['Electronics'] * 12
        }
        return pd.DataFrame(sales_data)

    def create_bar_chart(self, df: pd.DataFrame) -> go.Figure:
        fig = px.bar(
            df,
            x='Date',
            y='Sales',
            title='Monthly Sales Performance',
            template='plotly_white'  # Clean, professional look
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            showlegend=False
        )
        return fig

    def create_line_chart(self, df: pd.DataFrame) -> go.Figure:
        fig = px.line(
            df,
            x='Date',
            y='Sales',
            title='Sales Trend Analysis',
            template='plotly_white'
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            showlegend=False
        )
        return fig

    def calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """Calculate basic statistics to enhance LLM analysis"""
        stats = {
            'average_sales': df['Sales'].mean(),
            'max_sales': df['Sales'].max(),
            'min_sales': df['Sales'].min(),
            'growth_rate': ((df['Sales'].iloc[-1] - df['Sales'].iloc[0]) / df['Sales'].iloc[0]) * 100
        }
        return stats

    def get_chart_summary(self, df: pd.DataFrame, chart_type: str) -> str:
        # Calculate statistics
        stats = self.calculate_statistics(df)
        
        # Convert data to a more readable format
        data_summary = df.to_dict(orient='records')
        
        prompt = f"""
        As a data analyst, please analyze this {chart_type} chart data and provide insights:
        
        Key Statistics:
        - Average Sales: ${stats['average_sales']:.2f}
        - Maximum Sales: ${stats['max_sales']:.2f}
        - Minimum Sales: ${stats['min_sales']:.2f}
        - Overall Growth Rate: {stats['growth_rate']:.1f}%
        
        Raw Data:
        {json.dumps(data_summary, default=str)}
        
        Please provide a comprehensive analysis focusing on:
        1. Overall trends and patterns
        2. Notable peaks or dips
        3. Growth analysis
        4. Business recommendations
        
        Format the response in 3-4 clear, insightful sentences.
        """

        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768", 
            messages=[
                {"role": "system", "content": "You are a professional data analyst providing clear, actionable insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )
        
        return response.choices[0].message.content

def main():

    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("Please set the GROQ_API_KEY environment variable")
    
    analyzer = ChartAnalyzer(api_key)
    
    df = analyzer.create_sample_data()
    
    bar_chart = analyzer.create_bar_chart(df)
    line_chart = analyzer.create_line_chart(df)
    
    bar_chart.write_html("templates/sales_bar_chart.html")
    line_chart.write_html("templates/sales_trend_chart.html")

    
    print("\nAnalyzing Bar Chart...")
    bar_summary = analyzer.get_chart_summary(df, "bar")
    print(bar_summary)
    
    print("\nAnalyzing Line Chart...")
    line_summary = analyzer.get_chart_summary(df, "line")
    print(line_summary)

if __name__ == "__main__":
    main()
    