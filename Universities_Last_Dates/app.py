import os
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Specify the relative path to the CSV file
csv_file_path = os.path.join(os.getcwd(), 'college_deadlines.csv')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        college_name = request.form.get('college')
        
        if college_name:
            try:
                # Read the CSV file
                df = pd.read_csv(csv_file_path)
                
                # Ensure case-insensitive search for partial matches
                matched_college = df[df['college_name'].str.contains(college_name, case=False, na=False)]
                
                if not matched_college.empty:
                    # Get the last date and application link for the matched college
                    last_date = matched_college.iloc[0]['last_date']
                    application_link = matched_college.iloc[0]['application_link']
                    program_type = matched_college.iloc[0]['program_type']
                    
                    # Render result.html inside the 'results' folder
                    return render_template('results/result.html', 
                                           college_name=matched_college.iloc[0]['college_name'], 
                                           last_date=last_date, 
                                           program_type=program_type, 
                                           application_link=application_link)
                else:
                    return "College not found in the database."
            except Exception as e:
                return f"Error fetching data: {e}"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
