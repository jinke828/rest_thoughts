# Load the necessary library
library(ggplot2)

# Assuming the data is saved as "df"
df <- read.csv("/Users/jinke/Desktop/rest_thoughts/results/CCA/Compare_Ke-Smith.csv")

# Perform the Spearman correlation
result <- cor.test(df[['Smith']], df[['Ke_new']], method = "spearman")

# Extract r and p-value
r_value <- round(result$estimate, 2)  # Spearman's rho
p_value <- signif(result$p.value, 3) # p-value

# Create the scatter plot and annotate the correlation results
ggplot(df, aes(x = Smith, y = Ke, color = favorable)) +
  geom_point(alpha = 1, size = 2) +
  scale_color_gradient2(low = "#1b5e20", mid = "gray96", high = "#7d017d", 
                        midpoint = median(df$favorable, na.rm = TRUE)) + 
  labs(title = "Scatter Plot of Smith vs. Ke",
       x = "Smith",
       y = "Ke") +
  theme_minimal() +
  theme(panel.background = element_blank(),
        panel.grid = element_blank(),
        axis.line = element_line(colour = "black")) +
  coord_fixed(ratio = 1.2)+
  # Annotate with r and p-value
  annotate("text", x = min(df$Smith, na.rm = TRUE), 
           y = max(df$Ke, na.rm = TRUE), 
           label = paste("Spearman's r =", r_value, "\nP =", p_value), 
           hjust = 0, size = 4, color = "black")

# Save the plot
ggsave("/Users/jinke/Desktop/plot.png", dpi = 800)
