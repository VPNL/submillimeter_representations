#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "data_srcs", "values")

  df$partitions[df$partitions == 0] = "lateral"
  df$partitions[df$partitions == 1] = "medial"
  df$partitions = as.factor(df$partitions)

  df$data_srcs[df$data_srcs == 0] = "hires"
  df$data_srcs[df$data_srcs == 1] = "lowres"
  df$data_srcs = as.factor(df$data_srcs)

  model = aov(values~
	      partitions + 
	      data_srcs +
	      partitions*data_srcs +
	      (1 | subjects), data=df)
  print(summary(model))
  multcomp_results <- TukeyHSD(model)
  print(multcomp_results, digits=15)
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))
}

main()
