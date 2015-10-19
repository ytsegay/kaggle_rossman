## 15-10:

Creating a placeholder. 

## 17-10:
##### Data cleaning
- Promo - one hot encoded
- date - broken int to date, month and year components
- open date and promo2Date - removed the year value and used a relative difference between a fixed date and  
- only promoInterval and competitions distance had missing values in training. Test?

##### First stab
At this point compared linear regression (default), GBT and RF and RF is coming out over the top with flying colors. Below are the results of 5-fold cv for RMSPE

RF:

- 0.0709996403407
- 0.069714528619
- 0.0695215732334
- 0.0699926320844
- 0.0702853714225

GBT:

- 0.14665822165

LinearRegression:

- 2.50492007018

Here we forgot to remove customers from the data. This field is only available in training data.

##### TODO:
- Consider adding a variable around whether the stores were closed for refurbishment
- Can we use number of customers here? perhaps as a intermediate output prior to getting to the sales for the day?