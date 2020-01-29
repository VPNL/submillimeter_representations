#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "regressors", "data_srcs", "values")

  df$partitions[df$partitions == 0] = "VTC_lateral"
  df$partitions[df$partitions == 1] = "VTC_medial"
  df$partitions[df$partitions == 2] = "hOc1"

  df$data_srcs[df$data_srcs == 0] = "hires"
  df$data_srcs[df$data_srcs == 1] = "lowres"

  df$regressors[df$regressors == 0] = "domain"
  df$regressors[df$regressors == 1] = "category"

  df$partitions = as.factor(df$partitions)
  df$data_srcs = as.factor(df$data_srcs)
  df$regressors = as.factor(df$regressors)

  model <- aov(values~ 
	      partitions +
	      data_srcs +
	      regressors + 
	      partitions*data_srcs + 
	      partitions*regressors+ 
	      data_srcs*regressors+ 
	      partitions*data_srcs*regressors+ 
	      (1 | subjects), data=df)
  print(summary(model))
  # multcomp_results <- TukeyHSD(model)
  # print(multcomp_results, digits=6)
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))
}

main()
