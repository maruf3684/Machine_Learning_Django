from django.shortcuts import render
from django.views import View
# Create your views here.
import pandas as pd
import pickle
import numpy as np
car = pd.read_csv('car/cleaned_car.csv')
model=pickle.load(open('car/LinearRegressionModel.pkl','rb'))






class NameView(View):
    def get(self, request, *args, **kwargs):
        companies = sorted(car['company'].unique())
        car_models = sorted(car['name'].unique())
        year = sorted(car['year'].unique(), reverse=True)
        fuel_type = car['fuel_type'].unique()

        # companies.insert(0, 'Select Company')


        dict={
            'companies': companies,
            'car_models': car_models,
            'year': year,
            'fuel_type': fuel_type,
        }


        return render(request,'index.html',dict)

    def post(self, request, *args, **kwargs):
        companies = sorted(car['company'].unique())
        car_models = sorted(car['name'].unique())
        year = sorted(car['year'].unique(), reverse=True)
        fuel_type = car['fuel_type'].unique()


        # companies.insert(0, 'Select Company')

        dict = {
            'companies': companies,
            'car_models': car_models,
            'year': year,
            'fuel_type': fuel_type,
        }

        company = request.POST.get('company')
        car_model = request.POST.get('car_models')
        year = request.POST.get('year')
        fuel_type = request.POST.get('fuel_type')
        driven = request.POST.get('kilo_driven')
        st='Open this select menu'

        if company not in car_model:
            dict = {
                'companies': companies,
                'car_models': car_models,
                'year': year,
                'fuel_type': fuel_type,
                'wrmodel':'YOY SELECT THE WRONG CAR MODEL'
            }
            return render(request, 'index.html', dict)

        elif(company !=st):
                if(company and car_model and year and fuel_type and driven):
                    prediction = model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                                                            data=np.array([car_model, company, year, driven, fuel_type]).reshape(1,5)))
                    prediction=str(np.round(prediction[0],2))
                    dict = {
                        'companies': companies,
                        'car_models': car_models,
                        'year': year,
                        'fuel_type': fuel_type,
                        'prediction': prediction
                    }

        return render(request,'index.html',dict)