args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("usage: run_cluster_sensitivity.R input.csv output.csv")

suppressPackageStartupMessages(library(clubSandwich))
suppressPackageStartupMessages(library(sandwich))

data <- read.csv(
  args[[1]], stringsAsFactors = FALSE, check.names = FALSE,
  na.strings = c("", "NA")
)
data <- data[data$wave == "janeiro_2026", ]
data$interface <- factor(data$interface, levels = c("evento", "porta_a_porta"))
data$territory <- factor(data$territory)
data$interviewer <- factor(data$interviewer)

outcomes <- c(
  "septic", "sewer_network", "benefit_or_retirement",
  "social_transfer", "low_income", "unemployed"
)

analyze_outcome <- function(outcome) {
  required <- c(outcome, "interface", "territory", "interviewer", "submission_hour")
  model_data <- data[complete.cases(data[, required]), ]
  model_data$submission_hour_centered <-
    model_data$submission_hour - mean(model_data$submission_hour)
  model <- glm(
    reformulate(
      c("interface", "territory", "interviewer", "submission_hour_centered"),
      response = outcome
    ),
    family = binomial(), data = model_data
  )
  coefficient <- "interfaceporta_a_porta"
  estimate <- unname(coef(model)[[coefficient]])
  clusters <- length(unique(model_data$interviewer))

  clustered <- vcovCL(model, cluster = model_data$interviewer, type = "HC1")
  clustered_se <- sqrt(clustered[coefficient, coefficient])
  t_df <- clusters - 1
  t_stat <- estimate / clustered_se
  t_p <- 2 * pt(abs(t_stat), df = t_df, lower.tail = FALSE)
  t_critical <- qt(0.975, df = t_df)

  cr2 <- vcovCR(model, cluster = model_data$interviewer, type = "CR2")
  test <- coef_test(model, vcov = cr2, test = "Satterthwaite", coefs = coefficient)
  interval <- conf_int(
    model, vcov = cr2, test = "Satterthwaite",
    coefs = coefficient, level = 0.95
  )

  data.frame(
    outcome = outcome,
    n = nrow(model_data),
    clusters = clusters,
    odds_ratio = exp(estimate),
    t17_se = clustered_se,
    t17_p = t_p,
    t17_ci_low = exp(estimate - t_critical * clustered_se),
    t17_ci_high = exp(estimate + t_critical * clustered_se),
    cr2_se = test$SE,
    satt_df = test$df_Satt,
    satt_p = test$p_Satt,
    cr2_ci_low = exp(interval$CI_L),
    cr2_ci_high = exp(interval$CI_U)
  )
}

results <- do.call(rbind, lapply(outcomes, analyze_outcome))
results$satt_q_bh <- p.adjust(results$satt_p, method = "BH")
write.csv(results, args[[2]], row.names = FALSE)
print(results, digits = 10)
