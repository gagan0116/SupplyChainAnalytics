from flask import Flask, request, render_template
from src.pipelines.predict_pipeline import CustomData, PredictPipeline
from src.logger import logging

application = Flask(__name__)
#application is the route

@application.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        data = CustomData(
            Benefit_per_order=float(request.form.get('BenefitPerOrder')),
            Latitude=float(request.form.get('Latitude')),
            Longitude=float(request.form.get('Longitude')),
            Order_Item_Discount_Rate=float(request.form.get('DiscountRate')),
            Order_Item_Profit_Ratio=float(request.form.get('ProfitRatio')),
            Order_Item_Quantity=int(request.form.get('Quantity')),
            Sales=float(request.form.get('Sales')),
            Product_Price=float(request.form.get('ProductPrice')),
            order_year=int(request.form.get('order_year')),
            order_month=int(request.form.get('order_month')),
            order_day=int(request.form.get('Order Day')),
            Type=str(request.form.get('type')),
            Department_Name=str(request.form.get('deptname')),
            Order_Region=str(request.form.get('order_region')),
            Order_Status=str(request.form.get('order_status')),
            Customer_Segment=str(request.form.get('cust_segment')),
            Shipping_Mode=str(request.form.get('shipping_mode')),
            Product_Name=str(request.form.get('prod_name')),
            Category_Name=str(request.form.get('cat_name')),
            Order_City=str(request.form.get('ord_city')),
            Order_Country=str(request.form.get('ord_cntry')),
            Customer_Zipcode=str(request.form.get('cust_zip')),
        )

        pred_df = data.get_data_as_dataframe()

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        logging.info(f"Shape of result is: {results.shape}")
        return render_template('index.html', result1 = results[0][0], result2 = results[0][1])


if __name__ == "__main__": 
    application.run(host = "0.0.0.0")