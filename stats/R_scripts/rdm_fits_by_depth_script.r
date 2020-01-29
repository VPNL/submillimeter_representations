#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "betas", "depths", "regressors")

  df$partitions[df$partitions == 0] = "VTC_lateral"
  df$partitions[df$partitions == 1] = "VTC_medial"
  df$partitions[df$partitions == 2] = "hOc1"

  df$regressors[df$regressors == 0] = "Domain"
  df$regressors[df$regressors == 1] = "Category"

  df$partitions = as.factor(df$partitions)
  df$regressors = as.factor(df$regressors)

  # note depth is NOT a "factor"
  model <- aov(betas~
	       partitions + regressors + depths + 
	       partitions * regressors + 
	       partitions * depths + 
	       regressors * depths + 
	       partitions * regressors * depths + 
	      (1 | subjects), data=df)
  print(summary(model))
  print(summary.lm((model)))
  multcomp_results <- TukeyHSD(model)
  print(multcomp_results, digits=8)
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))
}

main()
