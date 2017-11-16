require(tidyverse)
require(blscrapeR)

df <- bls_api("CUSR0000SA0")
df_flat <- data.frame(matrix(unlist(df), nrow=6, byrow=T),stringsAsFactors=FALSE)
rownames(df_flat) <- c("Year", "M_ID", "Month", "Value", "Blank", "Series_ID")

df_flat %>% glimpse()


df_flat_t <- t(df_flat)
df_flat_t <- as.data.frame(df_flat_t) 
colnames(df_flat_t) <- c("Year", "M_ID", "Month", "Value", "Blank", "Series_ID")
df_flat_t %>% glimpse()
df_flat_t  <- df_flat_t %>% select(Year:Value, Series_ID)


write.csv(df_flat_t, row.names = FALSE, "outputs/cpi_data.csv") #create cpi_data file
