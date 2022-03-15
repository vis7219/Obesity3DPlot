# Obesity3DPlot

## About

This script is used to create a 3D Bar plot for Case/Control type of data between 2 variants

## Requirements
An **excel** file containing the columns
  1 Variant ID
  2 Genotype (HO -> 0   HET -> 1    HE -> 2)
  3 Case Sample Number
  4 Control Sample Number
  5 Case Value
  6 Control Value

## Start
The following options are required when creating the graph
1. --input <Excel File>
2. --normal <True/False> (If True, a normal graph is created)
3. --ratio <True/False> (If True, a graph is plotted using the Case/Control ratio of Samples and Value)
4. --output <str> (Gives a prefix to graph file name)
5. --output_type <jpg, jpeg, png, pdf> (Type of output)

The following options are optional
1. --z_max <int/float> (To be used if all the graphs require standard z-axis)
  
## How To Use
python Graphing.py --input input.xlsx  --normal True --ratio True --output TRIAL --output_type pdf --z_max 30
  
If the input excel sheet has 2 variant information, the output will be 2 graphs - Normal & Ratio
If the input excel sheet has 3 or more variant information, the number of output graphs will be the toal number of pair combinations
  
  Ex. If No. of input variants = 4,
      No. of graphs = 
