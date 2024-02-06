# Beer Distribution Management Database
## Project Details
Type: MS, team project <br />
Course Name: Applied Statistics Data Science (STAT 5405) <br />
Date : 08-28-2023 ~ 12-08-2023  <br />

## Project Description
The project aims to evaluate and compare two distinct statistical modeling approaches – ordinal categorical response modeling and binary logit modeling – in the context of predicting fetal health. The ordinal model is chosen for its ability to account for the natural order of the categories in the fetal health data, which includes three levels. Conversely, the binary model simplifies the problem by converting these levels into a binary format (0 and 1), potentially losing some nuanced information but potentially gaining in model simplicity and interpretability. We aim to understand which model provides more accurate and reliable predictions. This comparison will not only help in determining the best approach for this specific dataset but will also contribute to broader knowledge in the field of medical statistics, particularly in prenatal health care. <br/>

**Methodology** <br/>
Data Pre-processing <br/>
- Detect and address missing values, outliers, and ensure data quality.
- Convert 3 level response to binary for the binary model by eliminating 'suspect'
- Handling data imbalance if any. <br/>

Model Development <br/>
- Implement Logistic Regression to establish a baseline model for fetal health classification.
- Apply Classification and Regression Trees (CART) to explore non-linear relationships and decision boundaries.
- Employ the Random Forest algorithm to harness power of ensemble learning and enhance model robustness.
- Utilize XGBoost A state-of-the-art Gradient boosting algorithm, to further improve predictive performance.
- Use ordinal logistic regression that respects the order of the categories. <br/>

Model Evaluation<br/>
- The findings can assist healthcare professionals in better understanding and predicting fetal health, leading to improved prenatal care.
- Determine which model (ordinal or binary) performs better in terms of accuarcy, reliability, and prediction error rates.
- Understand how simplifying the categories affects the predictive power and interpretability of the model.

## Project Skill Set
- Language: R
- models: Logistic Regression, Random Forest, CART, XGBoost, Ordinal Model
