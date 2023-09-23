from flask import Flask, render_template, request, redirect, url_for, request, flash, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64
from werkzeug.utils import secure_filename 
import os
from io import StringIO
import tempfile
import csv



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'c:/Users/hp user/Desktop/Hamoye/Kahuna Project2/expense tracker app (skeleton)/upload_folder'
app.config['SECRET_KEY'] ='you will never guess'

# Sample expenses data (replace this with a database later)
expenses = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/input', methods=['GET', 'POST'])
def input_expense():
    if request.method == 'POST':
        # Extract data from the form and append it to the expenses list
        # Hint: Use request.form to get the form data
        # Hint: Convert amount to float before appending
        Date = request.form.get('date')
        Category = request.form.get('category')
        Amount = request.form.get('amount')
        Amount = float(Amount)
        expenditures = {'Date':Date, 'Category':Category, 'Amount':Amount}
        expenses.append(expenditures)
        

        return redirect(url_for('summary'))
    return render_template('input.html')





@app.route('/summary')
def summary():
    #TODO Calculate total expenses for the month  

    df = pd.DataFrame(expenses)

    total_expenses = 0
    for expense in expenses:
        print('Total expense incurred:',total_expenses)
        total_expenses += df['Amount'].sum()

    num_days = set()
    for expense in expenses:
        if 'Date' in expense:
            num_days.add(expense['Date'])
            len_days = len(num_days)
            print('Number of days:',len_days)

    avg_expenses_per_day = 0  
    for expense in expenses:
        avg_expenses_per_day += total_expenses / len_days
        print('Average expenses per day:',avg_expenses_per_day)

    avg_expenses_per_transaction = 0  
    num_of_transactions = len(expenses)
    for expense in expenses:
        avg_expenses_per_transaction += total_expenses / num_of_transactions
        print('Average expenses per transaction:',avg_expenses_per_transaction)

    #  # Calculate the distribution of expenses across categories
    category_distribution = df.groupby('Category')['Amount'].sum()

    #  # Generate a pie chart for category distribution
    categories = []
    amounts = []
    for expense in expenses:
        categories.append(expense['Category'])
        amounts.append(expense['Amount'])

        # plot pie chart  
    plt.figure(figsize=(8, 6))
    plt.pie(category_distribution, labels=category_distribution.index, startangle=90, explode=None, shadow=True, colors=['red', 'green', 'blue', 'yellow'],autopct='%1.1f%%')
    plt.title('Category Distribution')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    # encoding image
    image_base64 = base64.b64encode(buf.getvalue()).decode()
    buf.close()
    
    # #TODO Generate a line chart for spending trends over time
    # #Get dates and amounts from expense list
    #use plt.plot, rotate xlabel by 45 degrees
    amounts = []
    dates=[]
    #Getting chart data.
    for expense in expenses:
            amounts.append(expense['Amount'])
            dates.append(expense['Date'])
    #Plotting the linechart.
    img = BytesIO()

    plt.figure(figsize=(8, 6))
    plt.plot(dates, amounts)
    plt.title('Spending trend over time')
    plt.xlabel('Date')
    plt.xticks(rotation= 45)
    plt.ylabel('Amount')
    plt.savefig(img, format='png')

    #Converting the BytesIO object to base64 string.
    img_b64 = base64.b64encode(img.getvalue()).decode()
    buf.close()


    # Calculate monthly summaries
    monthly_summary = {}  # Dictionary to store monthly summaries

    for expense in expenses:
        date_parts = expense['Date'].split('-')
        year_month = f"{date_parts[0]}-{date_parts[1]}"
        
        if year_month in monthly_summary:
            monthly_summary[year_month] += expense['Amount']
        else:
            monthly_summary[year_month] = expense['Amount']

    #TODO input the write variables into the render_template function
    return render_template('summary.html', expenses=expenses, total=total_expenses, 
                           avg_per_day=avg_expenses_per_day, avg_per_transaction=avg_expenses_per_transaction,
                           monthly_summary=monthly_summary, image_base64 = image_base64, img_b64=img_b64)


   
# files that can be uploaded
ALLOWED_EXTENSIONS = {'csv','xlsm'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


# Upload functionality
@app.route('/upload', methods=['GET','POST'])
def upload():
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            # flash(message='Your file has been Uploaded.')

            tempfile_path = tempfile.NamedTemporaryFile().name
            file.save(tempfile_path)
            df = pd.read_csv(tempfile_path)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.dropna()
            # convert dataa types
            
           
        
        total_expenses = 0
        for expense in df:
            sum_expenses = df['Amount']
            total_expenses += sum_expenses.sum()

        num_days = set()
        for expense in df:
                date = 'Date'
                num_days.add(date)
                len_days = len(num_days)
                

        avg_expenses_per_day = 0  
        for expense in df:
            avg_expenses_per_day += total_expenses / len_days
            print('Average expenses per day:',avg_expenses_per_day)

        avg_expenses_per_transaction = 0  
        num_of_transactions = len(df)
        for expense in df:
            avg_expenses_per_transaction += total_expenses / num_of_transactions
            print('Average expenses per transaction:',avg_expenses_per_transaction)

        #  # Calculate the distribution of expenses across categories
        category_distribution = df.groupby('Category')['Amount'].sum()

        #  # Generate a pie chart for category distribution
        categories = []
        amounts = []
        for expense in df:
            categories.append(df['Category'])
            amounts.append(df['Amount'])

            # plot pie chart  
        plt.figure(figsize=(8, 6))
        plt.pie(category_distribution, labels=category_distribution.index, startangle=90, explode=None, shadow=True, colors=['red', 'green', 'blue', 'yellow'],autopct='%1.1f%%')
        plt.title('Category Distribution')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        # encoding image
        image_base64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        
        # #TODO Generate a line chart for spending trends over time
        # #Get dates and amounts from expense list
        #use plt.plot, rotate xlabel by 45 degrees
        amounts = []
        dates=[]
        #Getting chart data.
        for expense in df:
                amounts.append(df['Amount'])
                dates.append(df['Date'])
        #Plotting the linechart.
        img = BytesIO()

        plt.figure(figsize=(8, 10))
        plt.plot(dates, amounts)
        plt.title('Spending trend over time')
        plt.xlabel('Date')
        plt.xticks(rotation= 45)
        plt.ylabel('Amount')
        plt.savefig(img, format='png')

        #Converting the BytesIO object to base64 string.
        img_b64 = base64.b64encode(img.getvalue()).decode()
        buf.close()

        
        # Calculate monthly summaries
        monthly_summary = {}  # Dictionary to store monthly summaries
        
    
        for expense in df:
            date_parts = df['Date'].astype(str).str.split('-')
            year_month = f"{date_parts[0]}-{date_parts[1]}"
            
            if year_month in monthly_summary:
                monthly_summary[year_month] += df['Amount']
            else:
                monthly_summary[year_month] = df['Amount']

        #TODO input the write variables into the render_template function
        return render_template('summary.html', expenses=df, total=total_expenses, 
                            avg_per_day=avg_expenses_per_day, avg_per_transaction=avg_expenses_per_transaction,
                            monthly_summary=monthly_summary, image_base64 = image_base64, img_b64=img_b64)

            

            # return redirect(url_for('download_file', name=filename))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
