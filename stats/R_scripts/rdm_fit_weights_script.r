#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "regressors", "weights")

  df$partitions[df$partitions == 0] = "VTC_lateral"
  df$partitions[df$partitions == 1] = "VTC_medial"
  df$partitions[df$partitions == 2] = "hOc1"

  df$partitions = as.factor(df$partitions)

  df$regressors[df$regressors == 0] = "Domain"
  df$regressors[df$regressors == 1] = "Category"
  df$regressors[df$regressors == 2] = "Depth"
  df$regressors[df$regressors == 3] = "Intercept"

  df$regressors = as.factor(df$regressors)

  model <- aov(weights~ 
	      factor(partitions) +
	      factor(regressors) +
	      factor(partitions)*factor(regressors) + 
	      (1 | subjects), data=df)
  print(summary(model))
  multcomp_results <- TukeyHSD(model)
  print(multcomp_results, digits=12)
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))

}

main()
