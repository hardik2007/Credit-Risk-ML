import os
import pandas as pd
import mysql.connector

DB_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password': os.getenv("DB_PASSWORD"),
    'database':'credit_risk_db'
}

def getConnection():
    return mysql.connector.connect(**DB_config)

def analyzeRisk():
    conn = getConnection()
    print("\n INSIGHT 1: Risk by Job Category")
    query1 = """
    SELECT c.Job,COUNT(l.loan_id) AS Total_Loans,
    ROUND(SUM(CASE WHEN l.Risk = 'bad' THEN 1 ELSE 0 END)/COUNT(l.loan_id)*100,2)as default_rate_perc 
    FROM customers c JOIN loans l ON c.customer_id=l.customer_id 
    GROUP BY c.Job 
    ORDER BY default_rate_perc DESC;
    """
    d1=pd.read_sql(query1,conn)
    print(d1)

    print("\n INSIGHT 2: Avg Loan Amount by Age Group & Risk")
    query2 = """
    SELECT
    CASE
    WHEN c.Age < 25 THEN 'Young (<25)'
    WHEN c.Age BETWEEN 25 AND 40 THEN 'Mid (25-40)'
    ELSE 'Senior (>40)'
    END as age_group,
    l.risk,
    AVG(l.Credit_amount) as avg_loan_amount
    FROM customers c
    JOIN loans l ON c.customer_id=l.customer_id
    GROUP BY age_group,l.Risk
    ORDER BY age_group;
    """
    d2 = pd.read_sql(query2,conn)
    print(d2)

    print("\n INSIGHT 3: Default Rates by Loan Purpose")
    query3 = """
    SELECT
    l.Purpose,
    COUNT(*) as total_loans,
    ROUND(SUM(CASE WHEN l.Risk = 'bad' THEN 1 ELSE 0 END)/COUNT(*)*100,2)as default_rate_perc
    FROM loans l
    GROUP BY l.Purpose
    HAVING total_loans > 20
    ORDER BY default_rate_perc DESC    
    LIMIT 5;
    """
    d3 = pd.read_sql(query3, conn)
    print(d3)

    print("\n INSIGHT 4: Default Rate by Gender")
    query4 = """
    SELECT 
        c.Sex,
        COUNT(*) as total_loans,
        ROUND(SUM(CASE WHEN l.Risk = 'bad' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as default_rate_perc
    FROM customers c JOIN loans l ON c.customer_id = l.customer_id
    GROUP BY c.Sex;
    """
    d4 = pd.read_sql(query4, conn)
    print(d4)

    print("\n INSIGHT 5: Risk by Housing Status")
    query5= """
    SELECT 
        c.Housing,
        COUNT(*) as total_loans,
        ROUND(SUM(CASE WHEN l.Risk = 'bad' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as default_rate_perc
    FROM customers c JOIN loans l ON c.customer_id = l.customer_id
    GROUP BY c.Housing ORDER BY default_rate_perc DESC;
    """
    d5 = pd.read_sql(query5, conn)
    print(d5)

    print("\n INSIGHT 6: Risk by Checking Account Status")
    query6 = """
    SELECT 
        c.Checking_account,
        COUNT(*) as total_loans,
        ROUND(SUM(CASE WHEN l.Risk = 'bad' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as default_rate_perc
    FROM customers c JOIN loans l ON c.customer_id = l.customer_id
    GROUP BY c.Checking_account ORDER BY default_rate_perc DESC;
    """
    d6 = pd.read_sql(query6, conn)
    print(d6)

    print("\n INSIGHT 7: Risk by Savings Account Wealth")
    query7 = """
    SELECT 
        c.Saving_accounts,
        COUNT(*) as total_loans,
        ROUND(SUM(CASE WHEN l.Risk = 'bad' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as default_rate_perc
    FROM customers c JOIN loans l ON c.customer_id = l.customer_id
    GROUP BY c.Saving_accounts ORDER BY default_rate_perc DESC;
    """
    d7 = pd.read_sql(query7, conn)
    print(d7)

    print("\n INSIGHT 8: Risk by Loan Duration (Short vs Long)")
    query8 = """
    SELECT 
        CASE 
            WHEN l.Duration <= 12 THEN 'Short Term (< 1 Year)'
            WHEN l.Duration BETWEEN 13 AND 36 THEN 'Medium Term (1-3 Years)'
            ELSE 'Long Term (> 3 Years)'
        END as loan_duration_group,
        COUNT(*) as total_loans,
        ROUND(SUM(CASE WHEN l.Risk = 'bad' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as default_rate_perc
    FROM loans l
    GROUP BY loan_duration_group ORDER BY default_rate_perc DESC;
    """
    d8 = pd.read_sql(query8, conn)
    print(d8)
    
    conn.close()

if __name__ == "__main__":
    analyzeRisk()