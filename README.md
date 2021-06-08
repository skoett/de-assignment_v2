# Data Engineering Assignment : Small File Problem

## Introduction
When interviewing a data-minded candidate and potential future colleague of ours, we believe that an interview based on a handed-out task is often more open, more relevant and more interesting for both parties.

It is important to emphasize that the task at hand should not be interpreted as having a right or wrong answer, but merely acts as a basis for a discussion and a way for us to get a glimpse of how you as a candidate choose to go about it. It is not a requirement to implement all parts of the specified tasks - use it as a guidance and implement the solution the way you feel is right.

## The Objective
The assignment focuses on solving a variant of the small files problem. 
You are given access to a S3 bucket with many small csv files that have various data structures in them. 
Your goal is to perform a series of ETL steps that demonstrate your ability to work with simple data. It would be preferred if you use Python for you solution, but you can use whatever language you decide for :) You can use Scala, Python or R to solve the problem.

## Access
The generated data files needed for the assignment is located in the data folder of this repos

## Input
You are given input files with the naming convention : <craft>_<planet>_<date>_<time>.csv :

<craft> : [‘rocket’, ‘lander’]
<planet> : [‘venus’, ‘saturn’]
<date>_<time> has the following format : ‘yyyyMMdd_HHmmss’

There is four different file formats :


