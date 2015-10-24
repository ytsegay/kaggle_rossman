##### Data cleaning
- Promo - one hot encoded
- date - broken int to date, month and year components
- open date and promo2Date - removed the year value and used a relative difference between a fixed date and  
- only promoInterval and competitions distance had missing values in training. Test?
- remove number of customers from training data as it is not available at prediction


##### First stab
- Random forest: unless tree depth is controlled to under 20 and estimators/trees are trimmed to under 300, this will cause quick oom in your machine. so tread with care. RMSPE=0.368
- Linear regression/svm linear, svm nu produces RMSPE of about 0.456
- GBM: ??

##### Why is predicting these prices so difficult?
Granted that the number of trees used is very small why is it difficult to get a decent accuracy with such a large volume of data? 
plots/ScoreDistrib.png shows that the skewed right distribution of the scores. It also shows that there are a bunch of stores whose sales are zero.
To address the closed stores issues we removed closed stores from training. If a store is closed it will not make any sales. TO address the issue of skewed scores distribution, we will take the log of the scores as their surrogate.

##### TODO:
- Consider adding a variable around whether the stores were closed for refurbishment
- Can we use number of customers here? perhaps as a intermediate output prior to getting to the sales for the day?
