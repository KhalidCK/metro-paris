# Parisian metro


## Problematic introduction

In Paris the metro is a daily necessity for most of us.

The Parisian metro has 14 majors lines and has around 220 km of railroad. One original fact, compared to other European subway, is that stops are quite close : on average, the inter-distance between 2 station is 550m.

Lately I had a discussion and we tried to figure out when you should take the Parisian metro to avoid rush hours.

Common wisdom will say :

* in the morning : between 8 to 9h
* in the evening : between 17 to 19h

Make sense from my personal experience, however I was wondering, is there is any data that can tackle this question ?


## Getting the data


After some googling there is not that many data regarding the number of people that get in and out, on a fine grain, of a metro station.

[iledefrance-mobilites](https://www.iledefrance-mobilites.fr/) published 2017 multiple dataset regarding the number of traveler that get into a station.

There are two kinds of dataset that are available, the first one describe the number of daily traveler that validated their ticket at a specific stop.
The other is an *hourly ticket validation percentage per hour*, built according to some homemade profile, the methodology used is not described anywhere.

<!-- Explain insight* -->

Let's get a sense of the number of traveler that get every month on the metro

![monthly traveler in millions](img/monthly-traveler.png)

There is an expected deep in august when public holidays occurs.

An interesting insight, is to check how they are distributed across lines

![daily passenger distribution](img/daily-passenger-distribution.png)

Each point represents the daily number of travelers 

We'll now dive into the second dataset regarding pre-built profile.

There are 5 profiles defined :

- Working day outside of public school holidays
- Saturdays outside of public school holidays
- Working day during public school holidays
- Saturdays during public school holidays
- Sundays and public holidays(Christmas,...)


The hourly percentage is defined as : the number of daily validation to a specific station divided by the daily validation, therefore percentage on a given day sum-up to 100

Hereafter an overview

![average-metro-user-per-hour](img/average-metro-user-per-hour.png)

And for each profile

![facet-profile](img/facet-grid-user-per-hour.png)


<!--Conclusion-->

Looks like common wisdom is correct on average, however distribution is not the same for all stop, and according to your stop it can make sense to go or leave on different hour. You can explore more with the interactive plot [here](https://)
