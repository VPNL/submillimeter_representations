#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "domains", "wb_membership", "depth", "values")

  df$partitions[df$partitions == 0] = "VTC_lateral"
  df$partitions[df$partitions == 1] = "VTC_medial"

  df$domains[df$domains == 0] = "characters"
  df$domains[df$domains == 1] = "bodies"
  df$domains[df$domains == 2] = "faces"
  df$domains[df$domains == 3] = "objects"
  df$domains[df$domains == 4] = "places"

  df$wb_membership[df$wb_membership == 0] = "withincat"
  df$wb_membership[df$wb_membership == 1] = "betweencat"

  df$partitions = as.factor(df$partitions)
  df$domains = as.factor(df$domains)
  df$wb_membership = as.factor(df$wb_membership)

  model <- aov(values~ 
	      partitions +
	      domains +
	      wb_membership + 
	      depth + 
	      partitions*domains + 
	      partitions*wb_membership + 
	      partitions*depth + 
	      domains*wb_membership + 
	      domains*depth + 
	      wb_membership*depth+ 
	      partitions*wb_membership*domains + 
	      partitions*domains*depth + 
	      domains*wb_membership*depth + 
	      partitions*domains*wb_membership*depth + 
	      (1 | subjects), data=df)
  print(summary(model))
  # print(summary.lm(model)) # uncomment this for huge output of estimated coefficients
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))
}

main()
