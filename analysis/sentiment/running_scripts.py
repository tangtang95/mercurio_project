# -*- coding: utf-8 -*-
'''
Files used to run some temporary scripts regarding utilies, like files 
operation that need to be done only once
'''
import utilities.functions as fu

fu.lemmatize_file("resources/keywords.txt", "resources/lemmatized_vocabulary.txt")
