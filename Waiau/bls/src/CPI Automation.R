#Automate CPI data nationwide
require(tidyverse)
require(blscrapeR)


df <- bls_api("CUSR0000SA0") #get CPI data 
df_flat <- data.frame(matrix(unlist(df), nrow=6, byrow=T),stringsAsFactors=FALSE) #unlist, flatten df
rownames(df_flat) <- c("Year", "M_ID", "Month", "Value", "Blank", "Series_ID") #set rownames
df_flat_t <- t(df_flat) #transpose
df_flat_t <- as.data.frame(df_flat_t) 
colnames(df_flat_t) <- c("Year", "M_ID", "Month", "Value", "Blank", "Series_ID") #set colnames
df_flat_t  <- df_flat_t %>% select(Year:Value, Series_ID) #select relevant cols
df_update <- df_flat_t[1, ] #select only most recent line


cpi_data <- read.csv("outputs/cpi_data.csv", stringsAsFactors = FALSE) #read in cpi data
cpi_data_update <- rbind(df_update, cpi_data) #add new line to old file
write.csv(cpi_data_update, row.names = FALSE, "outputs/cpi_data.csv") #create new cpi_data file
write.csv(df_update, file=paste0("outputs/cpi_df_", Sys.Date(), ".csv")) #output only new data