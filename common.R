# See ft1_plot_time_series.Rmd for more details
split_adjust <- function(prices, symbol) {
  len = length(prices)
  original_final_price <- prices[len]
  for(j in 2:len) {
    split <- 0  # Initial split is 0
    
    if (prices[j-1] >= 1.4*prices[j]) {
      split = 1.5  # 3 for 2 use 3 shares in exchanged for 2 shares
      if (prices[j-1] >= 1.8*prices[j]) split = 2    # 2 for 1
      if (prices[j-1] >= 2.9*prices[j]) split = 3    # 3 for 1
      if (prices[j-1] >= 3.9*prices[j]) split = 4    # 4 for 1
      if (prices[j=1] >= 4.9*prices[j]) stop(paste(symbol, 'detected more than 4:1 split'))
      print(paste('Split adjusting', symbol, j, split, prices[j-1], prices[j]))
    }
    
    if (prices[j-1] <= prices[j]/1.4) {
      split = -1.5 
      if (prices[j-1] <= prices[j]/1.9 && prices[j-1] >= prices[j]/2.1) split = -2
      if (prices[j-1] <= prices[j]/2.9 && prices[j-1] >= prices[j]/3.1) split = -3
      if (prices[j-1] <= prices[j]/5.8 && prices[j-1] >= prices[j]/6.2) split = -6
      if (prices[j-1] <= prices[j]/7.7 && prices[j-1] >= prices[j]/8.3) split = -8
      if (prices[j-1] <= prices[j]/9.7 && prices[j-1] >= prices[j]/10.3) split = -10
      if ((split == 0) && (prices[j-1] <= prices[j]/2.9)) stop(paste(symbol, 'detected more than double reverse split'))
      print(paste('Reverse split adjusting', symbol, j, split, prices[j-1], prices[j])) 
    }
    
    if (split != 0) {
      for (k in j:len) {
       if (split > 0) prices[k] = prices[k] * split
       else prices[k] = prices[k] / abs(split)
      }
    }
  }
  
  final_price = prices[len]
  return(prices * original_final_price / final_price)
}


find_returns <- function(prices, split_adjusted=T) {
  len <- dim(prices)[1]
  total_stocks_num <- dim(prices)[2]
  log_returns <- matrix(nrow=(len-1), ncol=total_stocks_num)
  for (i in 1:total_stocks_num) {
    if (!split_adjusted) prices[, i] <<- split_adjust(prices[, i], lab[i])
    log_returns[, i] <- 100 * diff(log(prices[, i]))
  }
  return(log_returns)
}

find_covariance_matrix <- function (returns) {
  meanv <- apply(returns, 2, mean)
  covariance_matrix <- cov(returns)
  diag_cov_mat <- diag(covariance_matrix)
  sd <- sqrt(diag(covariance_matrix))
  list(meanv, covariance_matrix, diag_cov_mat, sd)
}
