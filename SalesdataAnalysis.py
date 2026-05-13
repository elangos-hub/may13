import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

FILE_PATH = r"D:\Home\Documents\project\salesDataAnalysis\sales_data.csv"
OUTPUT_DIR = "Sales_Reports"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_and_preprocess(path):
    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])

    df['Month_Year'] = df['Date'].dt.to_period('M').astype(str)
    df['Day_of_Week'] = df['Date'].dt.day_name()

    if 'Cost' in df.columns:
        df['Profit'] = df['Net_Revenue'] - df['Cost']
        df['Margin_Pct'] = (df['Profit'] / df['Net_Revenue']) * 100
        
    return df
def run_sales_dashboard(df):
    sns.set_theme(style="whitegrid", palette="muted")
    fig = plt.figure(figsize=(16, 10))
    plt.subplot(2, 2, 1)
    monthly_sales = df.groupby('Month_Year')['Net_Revenue'].sum().reset_index()
    sns.lineplot(data=monthly_sales, x='Month_Year', y='Net_Revenue', marker='o', linewidth=2.5, color='#008080')
    plt.title('Sales Velocity (Monthly Revenue)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.subplot(2, 2, 2)
    product_performance = df.groupby('Product')['Net_Revenue'].sum().sort_values(ascending=True).tail(10)
    product_performance.plot(kind='barh', color='#87CEEB')
    plt.title('Top 10 High-Contribution Products', fontsize=14, fontweight='bold')
    plt.xlabel('Revenue ($)')
    plt.subplot(2, 2, 3)
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_sales = df.groupby('Day_of_Week')['Net_Revenue'].mean().reindex(order)
    sns.barplot(x=day_sales.index, y=day_sales.values, palette='magma', hue=day_sales.index, legend=False)
    plt.title('Average Sales Intensity by Weekday', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.subplot(2, 2, 4)
    cat_col = 'Category' if 'Category' in df.columns else 'Product'
    category_data = df.groupby(cat_col)['Net_Revenue'].sum().sort_values(ascending=False).head(5)
    plt.pie(category_data, labels=category_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title(f'Revenue Concentration by {cat_col}', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/Executive_Sales_Dashboard.png", dpi=300)
    plt.show()
def print_business_metrics(df):
    total_revenue = df['Net_Revenue'].sum()
    total_orders = len(df)
    avg_order_value = total_revenue / total_orders
    monthly = df.groupby('Month_Year')['Net_Revenue'].sum()
    if len(monthly) > 1:
        growth = ((monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2]) * 100
    else:
        growth = 0

    print("\n" + "="*50)
    print("             SALES INTELLIGENCE REPORT            ")
    print("="*50)
    print(f"Total Gross Revenue:     ${total_revenue:,.2f}")
    print(f"Total Units Processed:   {total_orders:,}")
    print(f"Average Order Value:     ${avg_order_value:,.2f}")
    print(f" Month-over-Month Growth: {growth:.2f}%")
    
    if 'Profit' in df.columns:
        print(f"💵 Total Net Profit:        ${df['Profit'].sum():,.2f}")
        print(f"🎯 Avg Profit Margin:       {df['Margin_Pct'].mean():.1f}%")
    
    print("-" * 50)
    print(f"💡 STRATEGY: Focus marketing on {df.groupby('Day_of_Week')['Net_Revenue'].mean().idxmax()}s.")
    print(f"📂 Report and charts saved to: {os.path.abspath(OUTPUT_DIR)}")
    print("="*50 + "\n")
if __name__ == "__main__":
    sales_df = load_and_preprocess(FILE_PATH)
    run_sales_dashboard(sales_df)
    print_business_metrics(sales_df)