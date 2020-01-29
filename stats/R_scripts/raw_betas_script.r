#!/usr/bin/env Rscript

rm(list=ls())
library(nlme)
library(sjstats)

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  filename <- args[1]
  dat <- read.csv(file = filename, header = TRUE)

  df = as.data.frame(dat)

  names(df) <- c("idx", "partitions", "categories", "depths", "subjects", "betas")

  df$partitions[df$partitions == 0] = "lateral"
  df$partitions[df$partitions == 1] = "medial"
  df$partitions = as.factor(df$partitions)

  df$categories[df$categories == 0] = "numbers"
  df$categories[df$categories == 1] = "words"
  df$categories[df$categories == 2] = "limbs"
  df$categories[df$categories == 3] = "bodies"
  df$categories[df$categories == 4] = "adult"
  df$categories[df$categories == 5] = "child"
  df$categories[df$categories == 6] = "cars"
  df$categories[df$categories == 7] = "instruments"
  df$categories[df$categories == 8] = "houses"
  df$categories[df$categories == 9] = "corridors"
  df$categories = as.factor(df$categories)

  model = aov(betas~
	      partitions + 
	      categories +
	      depths +
	      partitions*categories +
	      partitions*depths +
	      categories*depths +
	      partitions*categories*depths +
	      (1 | subjects), data=df
	    )
  print(summary(model))
  multcomp_results <- TukeyHSD(model)
  print(multcomp_results, digits=4)
  
  print(summary(model)[[1]][["Pr(>F)"]])
  print(eta_sq(model))
}

main()
