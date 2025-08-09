# install packages
if (!require(remotes)) {
  install.packages("remotes")
}
remotes::install_github('jorvlan/raincloudplots')

library(raincloudplots)
library(tidyverse)
library(ggplot2) 
library(rlist)
setwd("/Users/jinke/Desktop/spontaneous_thoughts")

# load data
null_ratings = read.csv('./results/CPMs/r_null.csv')
null_ratings$Group <- factor(null_ratings$Group, levels = c("a_awake", "b_external", "c_future", "d_past","e_other", "f_valence", "g_image", "h_word","i_detail"))
actual_ratings <- read.csv('./results/CPMs/r_actual.csv')

#plot
ggplot(null_ratings, aes(x = Group, y = vals))+
  theme_bw()+
  scale_fill_manual(values=c("#58C9B9","#9DC8C8","#84B1ED","#D1B6E1","#9055A2","#EE7785","#EC7357","#FDD692","#FBFFB9"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  ggdist::stat_halfeye(
    # fill="lightgray",
    fill="gray80",
    ## custom bandwidth
    adjust = .8, 
    ## adjust height
    width = .4, 
    ## move geom to the right
    justification = -0.5, 
    ## remove slab interval
    .width = 0, 
    point_colour = NA
  )+
  geom_boxplot(
    data=actual_ratings,
    aes(x = Group, y = vals, fill=Group, middle = 0.9),
    width = .16,
    outlier.shape = NA,
    fatten = NULL
  )+
  ggforce::geom_sina(
    data=actual_ratings,
    aes(x = Group, y = vals),
    ## draw bigger points
    size = 1.2,
    ## add some transparency
    alpha =0.6,
    # color = "gray",
    maxwidth = .01,
    ## add some jittering
    position = position_jitter(
      ## control randomness and range of jitter
      seed = 10, width = 0
    )
  )+
  # ylim(-0.25, 1)
  scale_y_continuous(limits = c(-0.3, 1), breaks = c(-.25, 0, 0.25, 0.5, 0.75))

ggsave(filename = '/ratings.png', path = '/Users/jinke/Desktop', plot = last_plot(),dpi=1000)

