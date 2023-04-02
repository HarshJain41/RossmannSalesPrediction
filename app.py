import streamlit as st
import joblib 
import pickle
import pandas as pd

# Load the model from disk
model = joblib.load('rf.sav')
# Load the model from disk
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

st.title('Rossman Sales Prediction App')

st.write('This app takes in the several input parameters and predict the sales for a particular day of a 1115 rossman stores.')


store = int(st.number_input('Store Number (select between 1-1115)', step=1, min_value=1, max_value=1115))
# st.write('Store Number is', store)

week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
week_days_mapping = {'Monday':1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4, 'Friday':5, 'Saturday':6, 'Sunday':7}

week_days_input = st.selectbox('Select the day of the week', week_days)

# st.write(week_days_input)

col1, col2 = st.columns(2)


with col1:
    promo = ['yes', 'no']
    promo_map = {'yes':1, 'no':0}

    promo_or_not = st.selectbox('Promotion was opted or not?', promo)

with col2:
    school_holiday = ['yes', 'no']
    school_map = {'yes':1, 'no':0}

    school_holiday_or_not = st.selectbox('Is there a School Holiday?', school_holiday)


col3, col4 = st.columns(2)

with col3:
    year = st.number_input('Enter the year:',step=1, min_value=1973, max_value=2025)
    

with col4:
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
              'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


    select_month = st.selectbox('Select the month', months)


days = st.number_input('Enter the day number for which you want to predict:', step=1, min_value=1, max_value=31)


stores_type = ['a', 'b', 'c', 'd']
stores_type_input = st.selectbox('Select the type of store', stores_type)

assortment_type = ['basic', 'extra', 'extended']
assortment_type_map = {'basic':'a', 'extra':'b', 'extended':'c'}
assortment_type_input = st.selectbox('Select the assortment type (variations in the product)', assortment_type)

customers = st.number_input('Enter the expected number of customers', step=5, min_value=5)
comp_distance = st.number_input('Enter the distance in meters to the nearest competitor store', step=1)
comp_open_since_month = float(st.number_input('The month is which the nearest competitor store was opened (1-12)', step=1, min_value=1, max_value=12))
comp_open_since_year = float(st.number_input('The year in which the nearest competitor store was opened', step=1, min_value=1973, max_value=2025))


competition_open = (12* (year-comp_open_since_year)) + (month_map[select_month] - (comp_open_since_month))

if stores_type_input == 'a':
    store_type_value_b = 0
    store_type_value_c = 0
    store_type_value_d = 0

if stores_type_input == 'b':
    store_type_value_b = 1
    store_type_value_c = 0
    store_type_value_d = 0

if stores_type_input == 'c':
    store_type_value_b = 0
    store_type_value_c = 1
    store_type_value_d = 0

if stores_type_input == 'd':
    store_type_value_b = 0
    store_type_value_c = 0
    store_type_value_d = 1

if assortment_type_input == 'basic':
    assortment_b = 0
    assortment_c = 0

if assortment_type_input == 'extra':
    assortment_b = 1
    assortment_c = 0

if assortment_type_input == 'extended':
    assortment_b = 0
    assortment_c = 1





if st.button('Predict Sales'):

    try:
        final_dict = {'Store':store, 'day_of_week':week_days_mapping[week_days_input], 
                    'promotion':promo_map[promo_or_not], 'school holiday':school_map[school_holiday_or_not],
                    'year':year, 'month':month_map[select_month], 'day':days, 'store b':store_type_value_b,
                    'store c':store_type_value_c, 'store d':store_type_value_d, 'assortment b':assortment_b,
                    'assortment c':assortment_c, 'customers':customers, 'Comp Dist':comp_distance,
                    'Comp_open': competition_open}


        final_df = pd.DataFrame([final_dict])
        final_df_scaled = scaler.transform(final_df)
        # st.write(final_df_scaled)
        st.write(final_df)

        sales = model.predict(final_df_scaled)
        st.write('The sales for this particular day of the store you selected is:', sales[0])

    except Exception as e:
        st.error('There is something wrong, please enter the correct inputs', e)




