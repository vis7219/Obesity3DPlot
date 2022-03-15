#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 11:38:51 2022

@author: vishak
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import pandas as pd
import itertools
import getopt
import sys
import gc
import math


genotype = {'HO' : '0', 'HET' : '1', 'HE' : '2'} # Just for reference. Not used anywhere

# Changes to the Normal graph can be done in this function
def normal_plot(df, variants, output_type, output):
    
    # Creating the main figure
    fig, main_ax = plt.subplots(dpi = 1500, figsize = (22,17))
    main_ax.set_title('2 -> Homozygous Effect Allele (HE) \n1 -> Heterozygous (HET) \n0 -> Homozygous Other Allele (HO)', loc = 'left', fontsize = 16)

    # Creating the legends for the subplot graphs
    # These lines are not important as they are not visible in the graph. It is only for creating legends
    line1 = main_ax.plot(range(3), color = 'royalblue', alpha = 0.001, label = 'Case ' + str(variants[0]), marker = 'o', markersize = 15)
    line2 = main_ax.plot(range(3), color = 'mediumpurple', alpha = 0.001, label = 'Case ' + str(variants[1]), marker = 'o', markersize = 15)
    line3 = main_ax.plot(range(3), color = 'maroon', alpha = 0.001, label = 'Control ' + str(variants[0]), marker = 'o', markersize = 15)
    line4 = main_ax.plot(range(3), color = 'tomato', alpha = 0.001, label = 'Control ' + str(variants[1]), marker = 'o', markersize = 15)
    
    # Changing the location of the legend box
    leg = main_ax.legend(loc = 'upper right', bbox_to_anchor = (1.0, 1.15), fontsize = 14)
    for lh in leg.legendHandles:
        lh.set_alpha(1)
    
    # Changing the axis setting for main graph
    main_ax.xaxis.tick_top()
    main_ax.xaxis.set_label_position('top')
    main_ax.set_xlabel(str(variants[1]))
    main_ax.set_ylabel(str(variants[0]))

    # Removing the axis spines for main graph
    main_ax.spines['right'].set_visible(False)
    main_ax.spines['bottom'].set_visible(False)
    
    # Changing the fontsize for main graph
    for item in ([main_ax.title, main_ax.xaxis.label, main_ax.yaxis.label] + main_ax.get_xticklabels() + main_ax.get_yticklabels()):
        item.set_fontsize(20)
    
    # Changing the tick value for main graph
    plt.xticks([0.25, 1, 1.75], ['0','1','2'])
    plt.yticks([1.75,1,0.25], ['0', '1', '2'])
    
    # Creating the subgraphs inside the main graph
    count = 0
    for i in [0 , 1 , 2]: # These two loops loops through the HE, HET & HO Genotypes for both variants
        for j in [0 , 1 , 2]:
            count += 1
            # Initiate Plot
            ax = fig.add_subplot(330+count,
                                 projection = '3d')
            
            # Slice main DataFrame based on Variant Name
            var_1 = df[df.iloc[:,0] == variants[0]]
            var_2 = df[df.iloc[:,0] == variants[1]]
            
            # Find the Control and Case Sample Number for both variants
            temp = var_1[var_1.iloc[:,1] == i] # 1st column contains Genotype
            sample_case_var_1 = temp.iloc[0,2] # 2nd column contains Case numbers
            sample_control_var_1 = temp.iloc[0,3] # 3rd column contains Control numbers
            case_value_var_1 = temp.iloc[0,4] # 4th column contains case Value
            control_value_var_1 = temp.iloc[0,5] # 5th column contains control value
            
            temp = var_2[var_2.iloc[:,1] == j] # Similarly for variant 2
            sample_case_var_2 = temp.iloc[0,2]
            sample_control_var_2 = temp.iloc[0,3]
            case_value_var_2 = temp.iloc[0,4]
            control_value_var_2 = temp.iloc[0,5]
            
            max_value = max([control_value_var_1, control_value_var_2, case_value_var_1, case_value_var_2])
            min_value = min([control_value_var_1, control_value_var_2, case_value_var_1, case_value_var_2])
            
            # Creating values for plotting 3D Bar Graph
            x = [0, sample_case_var_1,
                 sample_case_var_1+sample_case_var_2+100,
                 sample_case_var_1+sample_case_var_2+100+sample_control_var_1] # Position of bars in X-axis
            y = [0,0,2,2] # position of bars in Y-axis
            z = [0,0,0,0]
            
            dx = [sample_case_var_1 , sample_case_var_2 ,
                  sample_control_var_1 , sample_control_var_2] # Length of bars in X-axis
            dy = [1,1,1,1] # Length of bars in Y-axis
            dz = [case_value_var_1, case_value_var_2,
                  control_value_var_1, control_value_var_2] # Length of bar in Z-axis
            
            # Creating the plot
            ax.bar3d(x, y, z,
                     dx, dy, dz,
                     color = ['royalblue', 'mediumpurple' ,'maroon', 'tomato'])
            ax.set_box_aspect((9,4,12))
            
            
            # Change the X & Y Tick Values
            ticksx = [0,
                      (sample_case_var_1/2),
                      sample_case_var_1 + (sample_case_var_2/2),
                      sample_case_var_1+(sample_case_var_2+100/2),
                      sample_case_var_1+sample_case_var_2+100+(sample_control_var_1/2),
                      sample_case_var_1+sample_case_var_2+100+sample_control_var_1+(sample_control_var_2/2  )]
            plt.xticks(ticksx, ['',
                                str(sample_case_var_1),
                                str(sample_case_var_2),
                                '',
                                str(sample_control_var_1),
                                str(sample_control_var_2)],
                       rotation = 5,
                       fontsize = 8)
            
            ticksy = [0.5, 2.5]
            plt.yticks(ticksy, ['Case', 'Control'],
                       fontsize = 10)
            
            ax.set_zlim([0, max_value + 2])
            ax.set_zticks(list(np.arange(0,max_value + 2, 2)))
            
            
            # Aesthetic Changes to Graph
            ax.set_xlabel("Number of Samples")
            ax.set_zlabel("BMI (KG/m$^2$)")
        
    plt.savefig(str(output) + '_Normal_' + str(variants[0]) + '_vs_' + str(variants[1]) + str(output_type))
    
    del fig
    del ax
    gc.collect()

# Changes to the Ratio graph can be done in this function
def ratio_plot(df, variants, output_type, output):
    # Creating the main figure
    fig, main_ax = plt.subplots(dpi = 1200, figsize = (22,17))

    # Creating the legends for the subplot graphs
    line1 = main_ax.plot(range(3), color = 'royalblue', alpha = 0.001, label = str(variants[0]), marker = 'o', markersize = 15)
    #line2 = main_ax.plot(range(3), color = 'mediumpurple', alpha = 0.001, label = 'Case ' + str(variants[1]), marker = 'o', markersize = 15)
    line3 = main_ax.plot(range(3), color = 'maroon', alpha = 0.001, label = str(variants[1]), marker = 'o', markersize = 15)
    #line4 = main_ax.plot(range(3), color = 'tomato', alpha = 0.001, label = 'Control ' + str(variants[1]), marker = 'o', markersize = 15)
    
    # Changing the location of the legend box
    leg = main_ax.legend(loc = 'upper right', bbox_to_anchor = (1.0, 1.15), fontsize = 14)
    for lh in leg.legendHandles:
        lh.set_alpha(1)
    
    # Changing the axis setting for main graph
    main_ax.xaxis.tick_top()
    main_ax.xaxis.set_label_position('top')
    main_ax.set_xlabel(str(variants[0]))
    main_ax.set_ylabel(str(variants[1]))

    # Removing the axis spines for main graph
    main_ax.spines['right'].set_visible(False)
    main_ax.spines['bottom'].set_visible(False)
    
    # Changing the fontsize for main graph
    for item in ([main_ax.title, main_ax.xaxis.label, main_ax.yaxis.label] + main_ax.get_xticklabels() + main_ax.get_yticklabels()):
        item.set_fontsize(20)
    
    # Changing the tick value for main graph
    plt.xticks([0.25, 1, 1.75], ['0','1','2'])
    plt.yticks([1.75,1,0.25], ['0', '1', '2'])
    
    count = 0
    for i in [0 , 1 , 2]:
        for j in [0 , 1 , 2]:
            count += 1
            # Initiate Plot
            ax = fig.add_subplot(330+count,
                                 projection = '3d')
            
            # Slice main DataFrame based on Variant Name
            var_1 = df[df.iloc[:,0] == variants[0]]
            var_2 = df[df.iloc[:,0] == variants[1]]
            
            # Find the Obesity value, Control and Case Sample Number for both variants
            temp = var_1[var_1.iloc[:,1] == i] 
            sample_case_var_1 = temp.iloc[0,2]
            sample_control_var_1 = temp.iloc[0,3]
            case_value_var_1 = temp.iloc[0,4]
            control_value_var_1 = temp.iloc[0,5]
            
            temp = var_2[var_2.iloc[:,1] == j]
            sample_case_var_2 = temp.iloc[0,2]
            sample_control_var_2 = temp.iloc[0,3]
            case_value_var_2 = temp.iloc[0,4]
            control_value_var_2 = temp.iloc[0,5]
            
            max_value = max(case_value_var_1/control_value_var_1, case_value_var_2/control_value_var_2)
            
            # Creating values for plotting 3D Bar Graph
            x = [0, ((sample_case_var_1/sample_control_var_1)+2)]
            y = [0,2]
            z = [0,0]
            
            dx = [sample_case_var_1/sample_control_var_1 ,
                  sample_case_var_2/sample_control_var_2]
            dy = [1,1]
            dz = [case_value_var_1/control_value_var_1 ,
                  case_value_var_2/control_value_var_2]
            
            # Creating the plot
            ax.bar3d(x, y, z,
                     dx, dy, dz,
                     color = ['royalblue' ,'maroon'])
            ax.set_box_aspect((2,6,6))
            
            ticksx = [(sample_case_var_1/sample_control_var_1)/2,
                      (((sample_case_var_1/(sample_control_var_1))+2+(sample_case_var_2/sample_control_var_2)/2))]
            plt.xticks(ticksx, [str(round(sample_case_var_1/sample_control_var_1,2)),
                                str(round(sample_case_var_2/sample_control_var_2,2))])
            
            ticksy = [0.5, 2.5]
            plt.yticks(ticksy, variants,rotation = 20, fontsize = 8)
            
            # Aesthetic Changes to Graph
            #ax.set_title(str(i) + ' vs ' + str(j))
            ax.set_xlabel("Case to Control Ratio")
            ax.set_zlim([0,max_value+0.4])
            ax.set_zticks(list(np.arange(0.0,max_value+0.4,0.2)))
            ax.set_zlabel("Case to Control BMI Value Ratio")
            
    #plt.suptitle(str(variants[0]) + 'Ratio' + ' vs ' + str(variants[1]) + 'Ratio',
    #                 fontsize = 30)
            
    plt.savefig(str(output) + '_Ratio_' + str(variants[0]) + '_vs_' + str(variants[1]) + str(output_type))
    
    del fig
    del ax
    gc.collect()

def variant_combinations(variants): # Finds all possible combination pairs of variants
    variant_subset = []
    for L in range(0, len(variants)+1):
        for subset in itertools.combinations(variants, L):
            if len(subset) == 2:
                variant_subset.append(list(subset))
            else:
                continue
            
    return(variant_subset)

def parseopts(opts):
    params = {}

    for opt, arg in opts:
        
        params['z_max'] = 0
        if opt in ["--input"]:
            params['inputfile'] = arg
        
        elif opt in ["-I"]:
            params['I'] = int(arg)

        elif opt in ["--normal"]:
            params['normal'] = arg

        elif opt in ["--ratio"]:
            params['ratio'] = arg
            
        elif opt in ['--output_type']:
            params['output_type'] = arg
            
        elif opt in ['--output']:
            params['output'] = arg
            
        elif opt in ['--z_max']:
            params['z_max'] = arg

    return params

def usage():

    """
    brief description of various flags and options for this script
    """

    print("\nHere is how you can use this script\n")
    print("Usage: python %s"%sys.argv[0])
    print("\t --input=<excel file>  (/path/to/input/file)")
    print("\t \t The input excel file must have columns in this order. The column names need not be the same")
    print("\t \t \t 1.SNP_ID")
    print("\t \t \t 2.Genotype (HO -> 0   HET -> 1   HE -> 2)")
    print("\t \t \t 3.Case Sample Number")
    print("\t \t \t 4.Control Sample Number")
    print("\t \t \t 5. Case Value")
    print("\t \t \t 6. Control Value")
    print("\t --normal=<Normal figure> (True/False) (To get normal graphs)")
    print("\t --ratio=<Ratio figure> (False/True) (To get figures in which the graph values are Case/Control ratios)")
    print("\t --output=<Prefix for the graph files>")
    print("\t --output_type=<jpg, jpeg, png, pdf")
    print("\t --z_max=<int> To be used if all graphs are supposed to have the same z-axis limit (Optional)")

if __name__=="__main__":

    # parse command-line options
    argv = sys.argv[1:]
    smallflags = "I:"
    bigflags = ["input=", "normal=", "ratio=", 'output=', 'output_type=', 'z_max=']
    try:
        opts, args = getopt.getopt(argv,smallflags, bigflags)
        if not opts:
            usage()
            sys.exit(2)
    except getopt.GetoptError:
        print("Incorrect options passed")
        usage()
        sys.exit(2)

    params = parseopts(opts)
    
    
    # Actual function of the script
    df = pd.read_excel(params['inputfile'])
    variants = list(set(df.iloc[:,0]))
    
    output_type = '.' + str(params['output_type'])
    
    try:
        if len(variants) > 2:
            variant_subset = variant_combinations(variants)
            
            for i in range(len(variant_subset)):
                new_df = df[df.iloc[:,0].isin(variant_subset[i])]
                
                if params['normal'] == 'True':
                    normal_plot(new_df, variant_subset[i], output_type, params['output'])
                
                if params['ratio'] == 'True':
                    ratio_plot(new_df, variant_subset[i], output_type, params['output'])
        
        else:
            if params['normal'] == 'True':
                normal_plot(df, variants, output_type, params['output'])
            if params['ratio'] == 'True':
                ratio_plot(df,variants, output_type, params['output'])
    except KeyError:
        print("Key Error")
        usage()
        sys.exit(2)
