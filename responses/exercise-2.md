# Exercise 2

## Business Process Description

A fact table and dimension table that describes the gym boulders.


The tables hold the boulder and the date it was set.
The boulder dimension describes the boulder's attributes, which allows the setters to know the distribution of grades, style, color, brand, and setters.
The time dimension describes the time the boulder was set, which allows the setters to know which boulder have been up the longest and need to be reset.
## Fact Table

| Column Name | Type     | Description                                             |
|-------------|----------|---------------------------------------------------------|
| boulder_id  | UUID     | The Primary Key that is unique to a boulder that is set |
| set_key     | UUID     | Foreign key that points to the Time Dimension           |

## Dimension

### Boulder Dimension
| Column Name    | Type    | Description                                                           |
|----------------|---------|-----------------------------------------------------------------------|
| boulder_id     | UUID    | The Primary Key that is unique to a boulder that is set               |
| boulder_grade  | int      | Grade of the boulder                                    |
| boulder_setter | varchar  | The setter of the boulder                               |
| boulder_color  | varchar | Color of the boulder                                                  |
| hold_brand     | varchar | Brand of the climbing holds                                           |
| boulder_style  | array   | Distinguishes what type of climb it is, dynamic, static, overhang, etc |

### Time Dimension
| Column Name      | Type     | Description                  |
|------------------|----------|------------------------------|
| set_key          | UUID     | UUID for the Date time       |
| boulder_set_date | Datetime | The date the boulder was set |
