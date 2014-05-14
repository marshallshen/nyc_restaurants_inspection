Introduction
=========================

NYC is full of restaurants, but are all the restaurants safe to eat at? We took a dive into NYC restaurants open data and retrieve indications of which restaurants are more likely give your stomach an unpleasant experience.

What did we find? Turns out large-sized restaurants in Manhattan are more likely to have food incidents than small-sized ones, and median-sized restaurants in NY have more food incidents around 2012 than small-sized ones. All of the claims above are purely based on present data. Let’s see how we reached the implications.

Using [NYC open data](https://nycopendata.socrata.com/), we first find the datasets of interests: dataset that describes the sidewalk cafes in the tri-state area, in addition to the dataset of food poisoning from Department of Health and Mental Hygiene. 

### Original dataset
There are two original datasets extracted from NYC open data:

[cafe.csv](https://data.cityofnewyork.us/Business/Sidewalk-Cafes/6k68-kc8u) include details on NYC restaurants (restaurant address, square footage, enclosed or unenclosed, etc.)

[food_poison.csv](https://data.cityofnewyork.us/Social-Services/food-poisoning/gjkf-etq5) include food poison records of NYC since 2012, note that food incidents transpire in various occasion, such as dining out in a restaurant, participating in a food catering event, etc. 

Given the two datasets of interest, we then process and combine the datasets to INTEGRATED-DATASET, this allows us to 

  - standardize data values across the files 
  - have one file from which we can retrieve indication rules from.

### Retrieve INTEGRATED-DATASET
Here we discuss how we get the INTEGRATED-DATASETS in details, some sample rows of INTEGRATED-DATASET looks like the following:

<table>
  <tr>
    <td>Restaurant/Bar/Deli/Bakery</td>
    <td>occasional incidents</td>
    <td>2 AVENUE</td>
    <td>fairly recent</td>
    <td>MANHATTAN</td>
    <td>Enclosed</td>
    <td>large</td>
    <td>2 AVENUE</td>
    <td>Street Match</td>
  </tr>
  <tr>
    <td>Restaurant/Bar/Deli/Bakery</td>
    <td>frequent incidents</td>
    <td>BROADWAY</td>
    <td>not recent</td>
    <td>MANHATTAN</td>
    <td>Enclosed</td>
    <td>arge</td>
    <td>BROADWAY</td>
    <td>Address Match</td>
  </tr>
</table>


We start by analyzing the schema of the original datasets and the integrated datasets. The table below is an overview of INTEGRATED-DATASET schema, followed by more detailed explanation for each field. Note that "standardized" indicates whether the data is further processed upon retrieval. Such process is necessary before we apply association rules because: 

  - we need to sanitize out any bad data entries 
  - we need to transform continuous attributes into categorical attributes 
  - some attributes are time sensitive and we need to process it dynamically to reflect its factual value based on current time 2014.

<table>
  <tr>
    <td>INTEGRATED DATASET attribute</td>
    <td>meaning of the attribute</td>
    <td>standardized?</td>
    <td>dependent food_poison.csv attribute</td>
    <td>dependent cafe.csv attribute</td>
  </tr>
  <tr>
    <td>Location Type</td>
    <td>Type of the restaurants</td>
    <td>No</td>
    <td>Location Type</td>
    <td>NA</td>
  </tr>
  <tr>
    <td>Incidents Frequency</td>
    <td>How often food incidents happen</td>
    <td>Yes</td>
    <td>Descriptor</td>
    <td>NA</td>
  </tr>
  <tr>
    <td>Street Name</td>
    <td>Street on which incidents transpire</td>
    <td>No</td>
    <td>Street Name</td>
    <td>Address Street Name</td>
  </tr>
  <tr>
    <td>Incident recentness</td>
    <td>How recent was the incident reported</td>
    <td>Yes</td>
    <td>Date</td>
    <td>NA</td>
  </tr>
  <tr>
    <td>Restaurant Size</td>
    <td>Restaurant size</td>
    <td>Yes</td>
    <td>NA</td>
    <td>Lic Area Sq Ft</td>
  </tr>
  <tr>
    <td>Borough</td>
    <td>Restaurant area</td>
    <td>No</td>
    <td>Park Borough</td>
    <td>No</td>
  </tr>
  <tr>
    <td>Street Address</td>
    <td>Restaurant street</td>
    <td>No</td>
    <td>NA</td>
    <td>Street Address</td>
  </tr>
  <tr>
    <td>Restaurant layout type</td>
    <td>Enclosed or Unenclosed </td>
    <td>No</td>
    <td>NA</td>
    <td>Sidewalk Cafe Type</td>
  </tr>
  <tr>
    <td>Match type</td>
    <td>Match Street or match Address</td>
    <td>Yes</td>
    <td>incident address</td>
    <td>street address</td>
  </tr>
</table>


The following described in detail how INTEGRATED-DATASET is retrieved.

**INTEGRATED-DATASET join operation**
The join is performed based on "Street Address" column of cafe.csv and “Incident Address” column of food_poison.csv. 
Because the "incident address" column of food_poson.csv sometimes include full address, and sometimes only street name. We categorize the matching using “Match Street” and “Match Address”. 
Pseudo-code:

  - if incident_address is :restaurant address: then join two rows, with label "address match"
  - if incident_address partially match restaurant address then join two rows, with label "street match"

**INTEGRATED-DATASET.location_type**
All possible types of restaurant are: "Soup Kitchen", "Restaurant Bar Deli Bakery", "Food Cart Vendor", "Catering Service". 
Restaurant type can be a significant indication factor for food incidents, for instance we can assume that restaurant of type "food cart vendor" is more likely to have food incident than that of “retaurant bar deli bakery”.

**INTEGRATED-DATASET.incidents_frequency**
It describes how often food incidents happen. ‘Descriptor" column from food_poison.csv has only two possible values (“1 or 2", “3 or More”). This attribute is one of the targeted attribute from which we want to draw indication rules from. We further processed incidents frequency using the following:

<table>
  <tr>
    <td>food_posion.csv</td>
    <td>INTEGRATED-DATASET.incidents_frequency</td>
  </tr>
  <tr>
    <td>1 or 2 (food poison happened 1 or 2 times)</td>
    <td>occasional incidents</td>
  </tr>
  <tr>
    <td>3 or More (food poison happened 3 or more times)</td>
    <td>frequent incidents</td>
  </tr>
</table>


**INTEGRATED-DATASET.street_name**
The main street on which the restaurant is located. This can be a significant indicator for food incidents, for instance,  we may retrieve indication that restaurants on Columbus Ave. appears to have more food incidents reported (It is totally hypothetically, we will let data speaks itself later on)

**INTEGRATED-DATASET.restaurant_size**
This attribute is retrieved from "Lic Area Sq Ft" column of “cafe.csv”. This categorized attributes includes 3 possible values: “small”, “median”, “large”. We transform the numerical values of square footage into a categorical value by comparing the square footages within the rows: sorted by square footage, the top 30% smallest restaurants are considered small, the next 30% restaurants are considered median, and the rest are considered large.  

**INTEGRATED-DATASET.incident_recentness**
This attribute is retrieved from "Created Date" column of food_poison.csv, the “Created Date” is the date which the food incident case upon the restaurant was first opened. Given a date, we further categorize them as follows:

<table>
  <tr>
    <td>Date on food_poison.csv</td>
    <td>INTEGRATED-DATASET.incident_recentness</td>
  </tr>
  <tr>
    <td>2014-01-01 - present</td>
    <td>recent</td>
  </tr>
  <tr>
    <td>2013-01-01 - 2013-12-31</td>
    <td>fairly recent</td>
  </tr>
  <tr>
    <td>before 2013/01/01</td>
    <td>not recent</td>
  </tr>
</table>



**INTEGRATED-DATASET.borough**
It is the neighborhood in which the restaurant is located. All possible values are: "BRONX", “BROOKLYN”, “MAHATTAN”, “QUEENS”, “STATEN ISLAND”
This is another targeted attribute from which we want to draw indication rules from, the value is directly retrieved from the "Park Borough" column of food_posion.csv

**INTEGRATED-DATASET.street_address**
Full street address of the restaurant, it is directly retrieved from "Street Address" column of cafe.csv

**INTEGRATED-DATASET.restaurant_layout_type**
Directly retrieved from column "Sidewalk Cafe Type" of cafe.csv, there are two possible values: “enclosed” and “unenclosed”. An enclosed area on the public sidewalk in front of the restaurant that is constructed predominantly of light materials such as glass.


Association Rule on INTEGRATED-DATASET
==================================
The assoication rule is based on the paper [Fast Algorithms for Mining Association Rules, Agrawal and Srikant](http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf). Two main concepts of association rules algorithm, extracted from the paper:

  1. Support of an itemset: given an items, what is the percentage of rows in the datasets that include every item in the itemset?
  2. Confidence of an association rules of an itemset: given all the rows that include every item on the left hand of the association rule, what is the probability that these rows also include the right hand side of the assocition rule?

Given 3343 rows of restaurant data, we treat the dataset as a historical transactions and each row as one transaction. Using association rule, we are trying to draw implications, for example:

````
  Food Cart Vendor, Broadway -> "recent", “occasional incidents”
````
Such an association can be interpreted as given a food cart along Broadway, it is more likely that a recent 1 or 2 food incident happened in those type of restaurants.

**Adjust minimum support and minimum confidence**

Take a close look at INTEGRATED-DATASET, we notice that the dataset is skewed by restaurant area: there are many more data on restaurants in Manhattan than any other neighborhoods. Therefore we must carefully calibrate minimum support and minimum confidence.

**Rules run and analysis**

**Run 1: min_support = 0.8, min_conf =0.8**

The result isn’t interesting because it doesn’t draw any interesting indication. "Street Match -> occasional incidents" or “occasional incidents -> Street Match” says that there are lots of data rows of food incidents with address that only includes a street name rather than a full address.

Note that :

````
['MANHATTAN'] support: 0.820520490577
['Restaurant Bar Deli Bakery'] support: 0.815734370326
['Unenclosed'] support: 0.804965599761
````

These frequent itemset confirms that the dataset is not evenly distributed: the majority rows are Manhattan restaurants (82% of data records), the majority of the restaurants are categorized as "Restaurant/Bar/Deli/Bakery" (81% of data records, and other options include “Food Cart Vendor”, “Delivery Service”), and the majority of the restaurants are unenclosed (80% of the data records).

Because we want to expose more interesting patterns, and the data is skewed, our strategy is to lower the support but maintain a high or even higher confidence rate: if the appearance of a certain set of traits is relatively slim but the traits are always tend to appear together, such set of traits are interesting to explore.

**Run 2: min_support = 0.5, min_conf =0.8 [INTERESTING FREQUENT ITEMSETS]**

Lowering the support gives us more frequent itemsets and rules. The following are a portion of outputs that appear to be interesting:

````
==Frequent itemsets (min_sup=0.5)
['occasional incidents', 'MANHATTAN', 'Unenclosed']    support: 0.615016452288
['not recent', 'Restaurant Bar Deli Bakery', 'MANHATTAN']  support: 0.504935686509


==High-confidence association rules (min_conf=0.8) 
return top 2 results..
['not recent', 'MANHATTAN', 'Street Match']) --> ['occasional incidents']
support: 0.56476218965 confidence: 0.939303482587

['not recent', 'MANHATTAN'])--> ['occasional incidents'] 
support: 0.613819922226 confidence: 0.936131386861
````

The frequency items indicate that there are many occasional food incidents took place in Manhattan, and many food incidents in Manhattan are not recent.

The indication rules aren’t that interesting: a food incident in Manhattan that is not recent indicates it is an occasional incidents. This indication reflects the nature of the data as 91% of the food poison cases were reported as "occasional".

**Run 3: min_support = 0.2, min_conf = 0.8 [INTERESTING ASSOCIATION RULES ]**

As the minimum support dropped, we see more interesting rules emerge, below are some retrieved interesting patterns:

````
==Interesting High-confidence association rules (min_conf=0.8)
['large', 'MANHATTAN'])-->['occasional incidents'] 
support: 0.273107986838 confidence: 0.939300411523

['smalll', 'MANHATTAN']-->['occasional incidents'] 
support: 0.22913550703 confidence: 0.902237926973
````

The comparison of the two rules above indicates that a large restaurant in Manhattan is more likely to have food incidents happen than a small one (93.9% confidence vs. 90.2% confidence)

````
['not recent', 'median']-->['occasional incidents'] 
support: 0.237810349985 confidence: 0.914844649022

['not recent', 'smalll'] -->['occasional incidents']
support: 0.220161531558 confidence: 0.904176904177
````

The comparison of the two rules above indicates that a median restaurant in NYC area has more occasional incidents happen in the past (2 years ago).

