
# Supply Chain Analytics using Machine Learning

This project focuses on optimizing logistics and managing risk in supply chain operations. It involves predictive analytics to forecast shipping days (scheduled and actual) based on various parameters such as benefit per order, geographic coordinates, sales data, and customer demographics. The predictive model achieves an 
𝑅2 score of 0.8, indicating strong performance in predicting shipping timelines.


## Tech Stack

*Data Analysis and Machine Learning:** pandas, numpy, scikit-learn, xgboost

**Data Visualization:** matplotlib, seaborn

**Database:** mysql-connector-python, sqlalchemy

**Web Framework:** Flask

**Environment Variables:** python-dotenv
## Deployment

This application is deployed using Amazon AWS Elastic Beanstalk with continuous integration and continuous deployment (CI/CD) facilitated by AWS CodePipeline. The deployment process automatically integrates changes pushed to the GitHub repository's main branch and deploys them to Elastic Beanstalk.

Deployment Steps
Continuous Integration (CI):
 - Changes pushed to the main branch of the GitHub repository trigger AWS CodePipeline.
Build Stage:
- AWS CodePipeline pulls the latest code from the GitHub repository.
- Dependencies are installed and the application is prepared for deployment.
Deployment Stage:
- AWS Elastic Beanstalk automatically deploys the updated application.
- The deployment process ensures consistency and updates all instances running the application.

The application can be accessed at [Deployment Link](http://supplychainapplication-env.eba-wc8c2vs2.us-east-1.elasticbeanstalk.com/)  after a successful deployment.

![image](https://github.com/gagan0116/SupplyChainAnalytics/assets/74581165/11ad1a67-6423-40cc-bc06-4ad5c6b04020)


## Screenshots

![image](https://github.com/gagan0116/SupplyChainAnalytics/assets/74581165/a886291e-10e6-4027-aac0-36de14fdb14e)

![image](https://github.com/gagan0116/SupplyChainAnalytics/assets/74581165/9173800c-1a3c-4526-ae03-734391d2f069)

## Run Locally

Clone the project

```bash
  git clone https://github.com/gagan0116/SupplyChainAnalytics.git
```

Go to the project directory

```bash
  cd SupplyChainAnalytics
```

Create and activate a virtual environment

```bash
  conda create -p venv python==3.11
  conda activate venv/
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python application.py
```

