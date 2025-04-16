from django.shortcuts import render,redirect
from admins.models import *
from django.contrib import messages

# Create your views here.

def pc_login(request):
    return render(request,"purecheck/pc_login.html")

def pc_logout(request):
    messages.info(request,"Purecheck Logout Successful")
    return redirect("/")

def pc_reg(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        mobile_no=request.POST['mobile_number']
        department=request.POST['department']
        registration(name=name,email=email,mobile_no=mobile_no,department=department).save()
        messages.info(request,"Purecheck Registration successful")
        return redirect('/pc_login/')
    else:
        return render(request,'purecheck/pc_reg.html')
    
def pc_validate_login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            data = registration.objects.get(email=email, password=password, department="Purecheck")
            if data.accept:
                messages.info(request, "Purecheck Login Successful")
                return redirect("/pc_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, "purecheck/pc_login.html")
        except:
            messages.info(request, "Wrong Credentials")
            return render(request, "purecheck/pc_login.html")
    return render(request, "purecheck/pc_login.html")

def pc_home(request):
    return render(request, "purecheck/pc_home.html")

def pc_req(request):
    obj = fluorine_files.objects.all()
    return render(request,"purecheck/pc_req.html",{"obj":obj})

def pc_analyze(request):
    obj = fluorine_files.objects.all()
    return render(request,"purecheck/pc_analyze.html", {"obj":obj})




#Machine Learning

import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from django.shortcuts import redirect
from django.contrib import messages
from admins.models import fluorine_files

def pc_analyze_process(request, project_id):
    # Fetch data from the Django model
    con = fluorine_files.objects.get(project_id=project_id)
    fluorine_mg = con.fluorine_mg
    energy_req = con.energy_req
    fr_recovered = con.fr_recovered

    # Load the dataset
    dataset_path = 'E:\\Project Breaking Down of Forever Chemicals V\\Project Breaking Down of Forever Chemicals V\\01_BDFC\\Dataset\\pc.csv'
    dataset = pd.read_csv(dataset_path)

    # Print column names to debug
    print("Dataset columns:", dataset.columns.tolist())

    # Standardize column names if necessary
    dataset.columns = dataset.columns.str.strip().str.lower()

    # Rename columns to match the expected names
    rename_map = {
        'fluorine_mg': 'fluorine_mg',
        'energy_req': 'energy_req',
        'fr_recovered': 'fr_recovered',
        'pure_per': 'pure_per'
    }
    
    # Check for missing columns and rename if present with a different name
    for original_name, expected_name in rename_map.items():
        if expected_name not in dataset.columns:
            # Try to find a matching column with a different case or formatting
            matches = [col for col in dataset.columns if col.lower() == original_name.lower()]
            if matches:
                dataset.rename(columns={matches[0]: expected_name}, inplace=True)

    # Verify that the required columns are in the dataset
    required_columns = set(rename_map.values())
    if not required_columns.issubset(dataset.columns):
        missing_cols = required_columns - set(dataset.columns)
        messages.error(request, f"The dataset is missing the following columns: {', '.join(missing_cols)}")
        return redirect("/pc_analyze/")

    # Use the data from the dataset
    X = dataset[['fluorine_mg', 'energy_req', 'fr_recovered']]
    y = dataset['pure_per']

    # Train a Decision Tree Regressor on the entire dataset
    decision_tree_regressor = DecisionTreeRegressor(random_state=42)
    decision_tree_regressor.fit(X, y)

    # Create a DataFrame with input data for prediction
    input_data = pd.DataFrame([[fluorine_mg, energy_req, fr_recovered]],
                              columns=['fluorine_mg', 'energy_req', 'fr_recovered'])

    # Make predictions using the trained model
    predictions = decision_tree_regressor.predict(input_data)

    # Update the Django model instance with the prediction result
    con.pure_per = predictions[0]  # Access the first value in the predictions array
    con.pc_scan = True
    con.status = "Purecheck Analyzed Successfully"
    con.save()

    # Inform the user that the analysis was successful
    messages.info(request, f"Purecheck Analyzed Successfully for {project_id}")
    return redirect("/pc_analyze/")





def pc_report(request):
    obj = fluorine_files.objects.filter(pc_scan = True)
    return render(request,"purecheck/pc_report.html",{"obj":obj})


    
