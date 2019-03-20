# Data Analysis of Real Production Data

## Table of Contents
[Introduction](#introduction)

[Procedure](#procedure)

## <a id="introduction"></a> Introduction

## <a id="procedure"></a> Procedure
1. for each file, extract the following columns and store them inside a (now smaller) CSV file:
    - machine_nr
    - begin_time
    - end_time
    - begin_date
    - status_code
    
2. for each of those files, for a given _**begin_date**_ range and _**machine_nr**_ pattern,
retrieve all matching entries and store them in separate CSV files

3. for each of those files, extract all unique _**machine_nr**_s and store them in separate CSV
files after filtering only those entries, whose _**status_code**_ is _**2**_, indicating error-free
operation

4. for each of those files, generate one-dimensional line graphs indicating the periods of time in which
machines were not operating error free

5. compare those graphs to determine to what percentage they match

