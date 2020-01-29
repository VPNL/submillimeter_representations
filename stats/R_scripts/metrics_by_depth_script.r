#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "depths", "values")

  df$partitions[df$partitions == 0] = "VTC_lateral"
  df$partitions[df$partitions == 1] = "VTC_medial"
  df$partitions = as.factor(df$partitions)

  model <- aov(values~ 
	      partitions +
	      depths +
	      partitions*depths+ 
	      (1 | subjects), data=df)
  print(summary(model))
  print(summary.lm(model))
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))
}

main()
