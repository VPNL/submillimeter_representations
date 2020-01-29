#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "slopes", "regressors")

  df$partitions[df$partitions == 0] = "VTC_lateral"
  df$partitions[df$partitions == 1] = "VTC_medial"

  df$regressors[df$regressors == 0] = "Domains"
  df$regressors[df$regressors == 1] = "Categories"

  model <- aov(slopes~ 
	      factor(partitions) +
	      factor(regressors) +
	      factor(partitions)*factor(regressors) + 
	      (1 | subjects), data=df)
  print(summary(model))
  multcomp_results <- TukeyHSD(model)
  print(multcomp_results, digits=6)
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))
}

main()
