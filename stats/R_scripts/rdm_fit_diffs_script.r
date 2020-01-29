#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "subjects", "diffs")

  df$partitions[df$partitions == 0] = "VTC_lateral"
  df$partitions[df$partitions == 1] = "VTC_medial"
  df$partitions[df$partitions == 2] = "hOc1"

  df$partitions = as.factor(df$partitions)

  model <- lme(diffs ~ partitions, random = ~ 1 | subjects / partitions, df)
  anova_model = aov(diffs~
	      factor(partitions) + 
	      (1 | subjects), data=df)
  print(summary(anova_model))
  require(multcomp)
  summary(glht(model, linfct = mcp(partitions = "Tukey")), test = adjusted(type = "bonferroni"))
}

main()
