# Report: Predict Bike Sharing Demand with AutoGluon Solution
#### Clement Palfroy

## Initial Training
### What did you realize when you tried to submit your predictions? What changes were needed to the output of the predictor to submit your results?
The first submition has been rejected by Kaggle because some of the predictions were negatives.  
To solve this problem, I decided to apply a Relu function on the predictions.  

### What was the top ranked model that performed?
WeigthedEnsemble-L_3. A third level stack combination of different model.   
It scored 1.3958.

## Exploratory data analysis and feature creation
### What did the exploratory analysis find and how did you add additional features?
To predict bike-sharing demand, it seems obvious that time elements such as the hour of the day will be important.  
My first step was to decompose the daytime feature into the following categorical data: year, month, weekday (and not just the day! I think it is more important to know that it is Sunday that the 15th of the month), and hour.  
  
Because of their properties, the "season" and "weather" features were also transformed into categorical values.  
  
Finally, the float features "temp", "atemp", "humidity", and "windspeed" were standardize to ensure none of them will have too much weight in the model.  
  
### How much better did your model preform after adding additional features and why do you think that is?
Much better: it scored 0.46080.  
I think that to predict correctly the bike-sharing demand on a hourly timeframe, it was very important to know the hour of the day.

## Hyper parameter tuning
### How much better did your model preform after trying different hyper parameters?
It actually did worse: 0.75.  
I think imposing range of parameters to the models when we don't have a strong intuition of how it might the model performance is counterproductive.  

### If you were given more time with this dataset, where do you think you would spend more time?
I would spend more time creating new features. 
One aspect that might influence the bike-sharing demand is the weather the day BEFORE the actual date.  
People tend to plan their day and their locomotion way day(s) in advance, I would have consider creating features to capture this idea.  

### Create a table with the models you ran, the hyperparameters modified, and the kaggle score.
|model|time|num_bag_folds|score|score|
|--|--|--|--|--|
|initial|600|default|3|1.3|
|add_features|600|default|3|0.4|
|hpo|1200|5|2|0.7|


### Create a line plot showing the top model score for the three (or more) training runs during the project.


![model_train_score.png](img/model_train_score.png)

### Create a line plot showing the top kaggle score for the three (or more) prediction submissions during the project.


![model_test_score.png](img/model_test_score.png)

## Summary
For this Kaggle competition, we were provided with hourly rental data spanning two years. The training set is comprised of the first 19 days of each month, while the test set is the 20th to the end of the month.   
Our goal was to predict the total count of bikes rented during each hour covered by the test set, using only information available prior to the rental period.  

To solve this problem, I used the powerful framework AutoGluon which automatically investigate several model architectures and combinations.  

I have 2 main takeaways from this exercice. 

1) The default values of the predictor learning parameters seem quite optimized already. Given enough time, I have no doubts the algorithm will find at least one very acceptable solution.
2) The fact that we have now at our disposition such powerful and automated way to investigate state-of-the-art ML models increase the incentive to focus on improving data quality. In addition to basic improvement such as data cleaning/imputing/standardization, I do think the main source of performance enhancement lies in feature engineering. To come up with features ideas that might influence the target feature often required common sense or expert knowledge, which machines still struggle with (for now...).

