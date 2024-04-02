# Bouldering Project Data Engineer coding exercise

The following are the instructions for the Bouldering Project Data Engineer coding exercise.

## Introduction

Bouldering Project's mission is to foster meaningful human connection with the most inspiring and inclusive climbing, movement, and community spaces. We care deeply about humans. We’re driven by the pursuit of better. We create joyful places and pathways for climbing, fitness, yoga, and social experiences that inspire people to challenge themselves and engage in a lifestyle centered around health, friendship, and purpose.

As a Data Engineer at Bouldering Project, you will be responsible for building out a data warehouse from the ground up using a modern data stack. You will drive a culture of data-driven decision making by developing tools that allow local managers and other business leaders to self-serve key performance metrics and reporting. As the expert on all BP data, you will work closely with our Finance, Accounting, Marketing, and Growth teams to ask and answer complex questions about our business. If you are curious and entrepreneurial and excited about an opportunity to lead greenfield data projects, we want to talk to you!

## Instructions and Guidelines

You are meant to spend about 1 hour total on this exercise.

Questions 1 and 2 are meant to take ~10 minutes each. Question 3 is significantly more complex and we do not expect that you finish the exercise in the time allotted. That's ok! Please submit what you have completed (more details below).

We may invite you to a follow up call to review all three exercises.

Please clone this repo, push it to your own **private** repo, and then share austin.wu@boulderingproject.com as a collaborator:
```sh
git clone git@github.com:bouldering-project/data-engineer-24.git
cd data-engineer-24
git remote set-url origin git@github.com:austinwu/bp-takehome.git # replace with your own private repo
git push --set-upstream origin main
```

## Exercises

### Exercise 1: SQL Query (5-10 minutes)

Given the data sources [transactions](data-sources/transactions.csv) and [order items](data-sources/order-items.csv), write and submit a SQL query that identifies and **groups the total amount refunded by location and month**.

The following database hosts the same data/schema if you'd like to debug your SQL in a running environment. The database is running MySQL 8.

```txt
Hostname: bp-data-engineer-exercise.ccotljdz9gac.us-east-1.rds.amazonaws.com
Port: 3306
Username: applicant
Password: bouldering
Database: bp_data_exercise
```

### Exercise 2: Data Modeling (10-15 minutes)

Select any business process related to (climbing) gyms, or yoga/fitness studios if you are more familiar with those, and design a fact table that models that process. You should also include at least one dimension related to the facts.

Examples business processes may include:
- Checking in to the gym
- Purchasing a membership

If you're near one of our [Bouldering Project locations](https://boulderingproject.com/all-locations/) and want to visit a gym to get a better feel of our business for this exercise, please reach out to austin.wu@boulderingproject.com and we'll get you set up with a free day pass. The visit is totally optional, especially if you're already relatively familiar with climbing gyms.

Alternatively, you can also visit our [Portal](https://boulderingproject.portal.approach.app) to browse our offerings online.

### Exercise 3: Messy Data Cleanup (40+ minutes)

You are welcome to complete the following exercise in any language you prefer. At BP we mostly use Python and JS.

Given the datasets [table history](data-sources/table-history.csv) and [status changes](data-sources/status-changes.csv), create a new dataset that shows the start and end of each membership. Your output will look something like:

| customer_id | start_date | end_date | end_reason |
| --- | --- | --- | --- |
| 1618630 | 2020-07-15 | 2020-08-16 | expire |
| 1618630 | 2021-03-22 | 2021-05-23 | expire |
| 1634015 | 2021-08-07 | 2021-11-01 | freeze |
| 1634015 | 2021-11-24 | 2022-02-01 | freeze |
| 1634015 | 2022-04-01 | 2022-07-01 | cancel |
| 1634015 | 2022-09-26 | 2022-11-01 | cancel |

The table history dataset holds a ledger of attribute mutations, formatted as
```txt
${attribute}-^!^!^-${oldValue}-^!^!^-${newValue}@#@#@#
```

The status changes table records scheduled status changes. For example:
```csv
status_id,customer_id,postdate,status,start_date
2259134,1670321,"2019-10-31 16:01:06",FREEZE,"2019-11-01 00:00:00"
```
Means that the customer `1670321` requested their membership to be frozen starting `2019-11-01` (this would be their membership end date). The request was put in on `2019-10-31`.

Some additional context that will be useful:

- `customer_type`
    - "GUEST" = not a member/no membership
    - "MEMBER" = holds an active membership
    - "PUNCH CARD" = not a member/no membership, uses a multi-visit pass

- `current_status`
    - "OK" = neutral status; if `customer_type` is "MEMBER" then active member
    - "FROZEN" = membership has ended and a "freeze" or pause has started
    - "TERMINATED" = membership has ended through cancellation or expiration

- `membership_form_of_payment`
    - "NONE" = free OR does not have a membership
    - "PREPAID" = non-recurring membership that expires on the `membership_end_date`; these memberships end in expiration
    - "BILLME" = recurring membership; these memberships end in cancellation or a freeze

As previously mentioned, it's acceptable and expected that you may not finish this exercise in the time allotted. You should submit whatever code you've completed in the time allotted; with this in mind, it is best if you submit a script that may be non-functioning but still outlines the general structure of how you would answer the question. In line comments and a paragraph explaining your approach are also encouraged. If you have any questions on how to interpret the dataset, you may email austin.wu@boulderingproject.com.
